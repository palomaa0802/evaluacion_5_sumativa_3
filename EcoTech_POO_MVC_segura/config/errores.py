import logging
import os

from config.entorno import RAIZ

RUTA_LOG = os.path.join(RAIZ, "errores.log")


def configurar_log() -> None:
    """Los detalles técnicos se guardan en errores.log, no se muestran al usuario."""
    logging.basicConfig(
        filename=RUTA_LOG,
        level=logging.WARNING,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8"
    )


def registrar_error(contexto: str, error: Exception) -> None:
    """Guarda el detalle técnico en el log y muestra un mensaje simple."""
    logging.getLogger("ecotech").error("%s: %s: %s", contexto, type(error).__name__, error)
    print(f"[ERROR] No se pudo completar la operación ({contexto}). Intente nuevamente.")
