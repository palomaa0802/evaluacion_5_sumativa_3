import re

MONEDAS_PERMITIDAS = ("USD", "EUR", "GBP", "BRL", "ARS", "PEN", "COP", "MXN", "UYU", "BOB", "JPY", "CNY", "CAD")


class ValidacionesServicios:
    """Se validan los datos del usuario antes de enviarlos a una API."""

    @staticmethod
    def sanear_ciudad(ciudad: str) -> str | None:
        ciudad = " ".join(str(ciudad).split())
        if len(ciudad) < 2 or len(ciudad) > 50:
            return None
        if not ciudad.replace(" ", "").replace("-", "").isalpha():
            return None
        return ciudad

    @staticmethod
    def sanear_moneda(moneda: str) -> str | None:
        # solo se aceptan códigos de la lista, nada de texto libre
        moneda = str(moneda).strip().upper()
        return moneda if moneda in MONEDAS_PERMITIDAS else None

    @staticmethod
    def sanear_email(email: str) -> str | None:
        email = str(email).strip().lower()
        if len(email) > 60 or not re.fullmatch(r"[\w\.-]+@[\w\.-]+\.\w+", email):
            return None
        return email
