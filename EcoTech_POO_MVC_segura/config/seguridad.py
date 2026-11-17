import hashlib
import hmac
import os
import re

from config.entorno import Entorno

ITERACIONES = 600000


class Seguridad:
    """
    Manejo de contraseñas: nunca se guardan tal cual, solo un hash (PBKDF2-SHA256)
    calculado con una sal distinta por usuario y un secreto (pepper) que viene del .env.
    """

    @staticmethod
    def generar_sal() -> str:
        return os.urandom(16).hex()

    @staticmethod
    def cifrar(clave: str, sal_hex: str) -> str:
        pepper = Entorno.obtener("ECOTECH_PEPPER") or ""
        texto = (pepper + clave).encode("utf-8")
        return hashlib.pbkdf2_hmac("sha256", texto, bytes.fromhex(sal_hex), ITERACIONES).hex()

    @staticmethod
    def verificar(clave: str, sal_hex: str, hash_guardado: str) -> bool:
        # compare_digest compara sin dar pistas por el tiempo de respuesta
        return hmac.compare_digest(Seguridad.cifrar(clave, sal_hex), hash_guardado)

    @staticmethod
    def validar_fortaleza(clave: str) -> None:
        if not isinstance(clave, str) or len(clave) < 8 or len(clave) > 64:
            raise ValueError("La contraseña debe tener entre 8 y 64 caracteres.")
        if " " in clave:
            raise ValueError("La contraseña no puede tener espacios.")
        if not re.search(r"[A-Z]", clave) or not re.search(r"[a-z]", clave) or not re.search(r"[0-9]", clave):
            raise ValueError("La contraseña debe incluir mayúscula, minúscula y número.")
