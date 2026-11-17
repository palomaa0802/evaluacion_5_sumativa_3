from getpass import getpass

from views.utils import leer_numero


class AuthView:
    @staticmethod
    def mostrar_menu_inicio() -> int:
        print("\n" + "=" * 42)
        print("   ECOTECH SOLUTIONS - ACCESO")
        print("=" * 42)
        print("1.- Iniciar sesión")
        print("0.- Salir")
        print("=" * 42)
        return leer_numero("Seleccione una opción: ")

    @staticmethod
    def solicitar_credenciales() -> dict | None:
        print("\n--- Inicio de Sesión (deje el correo vacío para volver) ---")
        email = input("Correo: ").strip()
        if not email:
            return None
        contrasena = getpass("Contraseña: ")
        return {"email": email, "contrasena": contrasena}

    @staticmethod
    def formulario_primer_administrador() -> dict:
        print("\nNo hay administradores registrados. Cree el primero para poder usar el sistema.")
        nombre = input("Nombre del administrador: ")
        email = input("Correo del administrador: ")
        contrasena = getpass("Contraseña (mín. 8, con mayúscula, minúscula y número): ")
        repetida = getpass("Repita la contraseña: ")
        return {"nombre": nombre, "email": email, "contrasena": contrasena, "repetida": repetida}

    @staticmethod
    def mostrar_mensaje(mensaje: str) -> None:
        print(f"[ACCESO] {mensaje}")
