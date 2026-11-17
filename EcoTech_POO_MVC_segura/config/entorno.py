import os
import secrets

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_ENV = os.path.join(RAIZ, ".env")


class Entorno:
    """
    Lee los datos sensibles desde el archivo .env (no desde el código).
    Si el archivo no existe, se crea con un secreto aleatorio para este equipo.
    """
    _datos: dict[str, str] | None = None

    @staticmethod
    def _crear_env() -> None:
        with open(RUTA_ENV, "w", encoding="utf-8") as archivo:
            archivo.write("ECOTECH_PEPPER=" + secrets.token_hex(32) + "\n")

    @staticmethod
    def _cargar() -> dict[str, str]:
        if not os.path.exists(RUTA_ENV):
            Entorno._crear_env()
        datos: dict[str, str] = {}
        with open(RUTA_ENV, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea or linea.startswith("#") or "=" not in linea:
                    continue
                clave, valor = linea.split("=", 1)
                datos[clave.strip()] = valor.strip()
        return datos

    @staticmethod
    def obtener(clave: str) -> str | None:
        if Entorno._datos is None:
            Entorno._datos = Entorno._cargar()
        # una variable de entorno del sistema tiene prioridad sobre el .env
        return os.environ.get(clave, Entorno._datos.get(clave))
