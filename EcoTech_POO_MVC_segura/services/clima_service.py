from services.cliente_http import ClienteHTTP
from services.excepciones import ErrorFormato, ErrorDatos
from services.validaciones import ValidacionesServicios

URL_CIUDAD = "https://geocoding-api.open-meteo.com/v1/search"
URL_CLIMA = "https://api.open-meteo.com/v1/forecast"

# códigos WMO que entrega Open-Meteo
ESTADOS = {
    0: "Despejado", 1: "Mayormente despejado", 2: "Parcialmente nublado", 3: "Nublado",
    45: "Niebla", 48: "Niebla con escarcha",
    51: "Llovizna ligera", 53: "Llovizna", 55: "Llovizna intensa",
    56: "Llovizna helada", 57: "Llovizna helada intensa",
    61: "Lluvia ligera", 63: "Lluvia", 65: "Lluvia intensa",
    66: "Lluvia helada", 67: "Lluvia helada intensa",
    71: "Nevada ligera", 73: "Nevada", 75: "Nevada intensa", 77: "Granizo fino",
    80: "Chubascos ligeros", 81: "Chubascos", 82: "Chubascos fuertes",
    85: "Chubascos de nieve", 86: "Chubascos de nieve fuertes",
    95: "Tormenta eléctrica", 96: "Tormenta con granizo", 99: "Tormenta fuerte con granizo"
}


class ClimaService:
    """Consulta el clima actual de una ciudad (Open-Meteo, no pide llave)."""

    def __init__(self):
        self._http = ClienteHTTP()

    def _buscar_ciudad(self, ciudad: str) -> dict | None:
        datos = self._http.obtener_json(URL_CIUDAD, {"name": ciudad, "count": 1, "language": "es"})
        resultados = datos.get("results")
        return resultados[0] if resultados else None

    def _obtener_clima(self, latitud: float, longitud: float) -> dict:
        parametros = {
            "latitude": latitud,
            "longitude": longitud,
            "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
        }
        actual = self._http.obtener_json(URL_CLIMA, parametros).get("current")
        if not isinstance(actual, dict):
            raise ErrorFormato("El servicio de clima no entregó datos actuales.",
                               "Falta el campo current en la respuesta")
        return actual

    @staticmethod
    def _verificar(actual: dict) -> None:
        for campo in ("temperature_2m", "relative_humidity_2m", "weather_code", "wind_speed_10m"):
            valor = actual.get(campo)
            if isinstance(valor, bool) or not isinstance(valor, (int, float)):
                raise ErrorDatos("Los datos del clima llegaron incompletos.", "Campo inválido o faltante: " + campo)
        if not -90 <= actual["temperature_2m"] <= 60:
            raise ErrorDatos("La temperatura recibida no es creíble.", "Temperatura fuera de rango")
        if not 0 <= actual["relative_humidity_2m"] <= 100:
            raise ErrorDatos("La humedad recibida no es creíble.", "Humedad fuera de rango")
        if actual["wind_speed_10m"] < 0:
            raise ErrorDatos("El viento recibido no es creíble.", "Viento negativo")

    def consultar(self, ciudad: str) -> dict | None:
        """
        Devuelve un diccionario con el clima, {} si la ciudad no existe
        y None si el nombre de la ciudad no es válido (no se llama a la API).
        """
        ciudad = ValidacionesServicios.sanear_ciudad(ciudad)
        if ciudad is None:
            return None
        lugar = self._buscar_ciudad(ciudad)
        if lugar is None:
            return {}
        actual = self._obtener_clima(lugar["latitude"], lugar["longitude"])
        self._verificar(actual)
        codigo = int(actual["weather_code"])
        return {
            "ciudad": lugar.get("name", ciudad),
            "pais": lugar.get("country", ""),
            "temperatura": actual["temperature_2m"],
            "humedad": actual["relative_humidity_2m"],
            "viento": actual["wind_speed_10m"],
            "codigo": codigo,
            "estado": ESTADOS.get(codigo, "Condición no identificada")
        }

    @staticmethod
    def evaluar_trabajo_en_terreno(clima: dict) -> str:
        """Regla simple para planificar visitas a terreno de un proyecto."""
        motivos = []
        if clima["codigo"] >= 51:
            motivos.append("hay precipitaciones o tormenta")
        if clima["viento"] > 40:
            motivos.append("el viento es fuerte")
        if clima["temperatura"] > 35:
            motivos.append("hace demasiado calor")
        if clima["temperatura"] < 0:
            motivos.append("hay riesgo de heladas")
        if not motivos:
            return "Condiciones adecuadas para trabajar en terreno."
        return "Se recomienda reprogramar la visita a terreno porque " + " y ".join(motivos) + "."
