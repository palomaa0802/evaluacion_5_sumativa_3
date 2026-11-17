import logging
import time

import requests

from services.excepciones import ErrorConexion, ErrorTiempoEspera, ErrorHTTP, ErrorFormato

TIEMPO_ESPERA = 10
INTENTOS = 3
ESPERA_ENTRE_INTENTOS = 1


class ClienteHTTP:
    """Hace los GET a las APIs con timeout, reintentos y revisión del código HTTP."""

    def obtener_json(self, url: str, parametros: dict | None = None) -> dict:
        ultimo_error = None

        for intento in range(1, INTENTOS + 1):
            try:
                respuesta = requests.get(url, params=parametros, timeout=TIEMPO_ESPERA)
            except requests.exceptions.Timeout:
                ultimo_error = ErrorTiempoEspera(
                    "El servicio externo se demoró demasiado en responder.", "Timeout en " + url)
            except requests.exceptions.ConnectionError:
                ultimo_error = ErrorConexion(
                    "No hay conexión con el servicio externo. Revisa tu internet.", "ConnectionError en " + url)
            except requests.exceptions.RequestException as error:
                ultimo_error = ErrorConexion(
                    "No se pudo completar la consulta al servicio externo.",
                    "RequestException en " + url + ": " + type(error).__name__)
            else:
                codigo = respuesta.status_code
                if codigo == 200:
                    return self._leer_json(respuesta, url)
                error_http = self._error_por_codigo(codigo, url)
                # 400, 401, 403 y 404 no se arreglan reintentando
                if codigo < 500 and codigo != 429:
                    raise error_http
                ultimo_error = error_http

            logging.warning("Intento %s de %s fallido: %s", intento, INTENTOS, ultimo_error.detalle_tecnico)
            if intento < INTENTOS:
                time.sleep(ESPERA_ENTRE_INTENTOS)

        raise ultimo_error

    @staticmethod
    def _leer_json(respuesta, url: str) -> dict:
        try:
            datos = respuesta.json()
        except ValueError:
            raise ErrorFormato("El servicio externo entregó una respuesta que no se puede leer.",
                               "JSON inválido desde " + url)
        if not isinstance(datos, dict):
            raise ErrorFormato("El servicio externo entregó una respuesta inesperada.",
                               "El JSON de " + url + " no es un objeto")
        return datos

    @staticmethod
    def _error_por_codigo(codigo: int, url: str) -> ErrorHTTP:
        detalle = "Código HTTP " + str(codigo) + " en " + url
        if codigo == 400:
            return ErrorHTTP("La consulta no fue aceptada por el servicio (datos incorrectos).", detalle)
        if codigo in (401, 403):
            return ErrorHTTP("No hay autorización para usar este servicio externo.", detalle)
        if codigo == 404:
            return ErrorHTTP("El servicio externo no encontró lo que se pidió.", detalle)
        if codigo == 429:
            return ErrorHTTP("Se hicieron demasiadas consultas. Intenta de nuevo en un rato.", detalle)
        if codigo >= 500:
            return ErrorHTTP("El servicio externo está con problemas en este momento.", detalle)
        return ErrorHTTP("El servicio externo respondió algo inesperado.", detalle)
