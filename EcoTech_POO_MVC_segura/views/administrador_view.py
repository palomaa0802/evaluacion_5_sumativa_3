from getpass import getpass
from views.utils import leer_numero, confirmar
from models.administrador import Administrador


class AdministradorView:
    @staticmethod
    def mostrar_menu() -> int:
        print("\n" + "-" * 38)
        print("     GESTIÓN DE ADMINISTRADORES")
        print("-" * 38)
        print("1.- Agregar administrador")
        print("2.- Editar administrador")
        print("3.- Eliminar administrador")
        print("4.- Imprimir un administrador")
        print("5.- Imprimir todos los administradores")
        print("6.- Probar inicio de sesión y permisos (iniciarSesion / gestionarUsuarios)")
        print("0.- Volver al menú principal")
        print("-" * 38)
        return leer_numero("Seleccione una opción: ")

    @staticmethod
    def formulario_nuevo_administrador() -> dict:
        print("\n--- Agregar Nuevo Administrador ---")
        nombre = input("Ingrese el nombre del administrador: ")
        email = input("Ingrese el email del administrador: ")
        contrasena = getpass("Ingrese la contraseña (mín. 8, con mayúscula, minúscula y número): ")
        print("Niveles de permiso disponibles: 1.- Basico, 2.- Medio, 3.- Alto, 4.- Superadmin")
        opcion_nivel = leer_numero("Seleccione un nivel de permiso (1-4): ")
        mapa_nivel = {1: "Basico", 2: "Medio", 3: "Alto", 4: "Superadmin"}
        nivel_permiso = mapa_nivel.get(opcion_nivel, "")

        return {
            "nombre": nombre,
            "email": email,
            "contrasena": contrasena,
            "nivel_permiso": nivel_permiso
        }

    @staticmethod
    def solicitar_id() -> int:
        return leer_numero("Ingrese el ID del administrador: ")

    @staticmethod
    def solicitar_credenciales() -> dict:
        print("\n--- Inicio de Sesión de Administrador ---")
        email = input("Ingrese el email del administrador: ").strip()
        contrasena = getpass("Ingrese la contraseña: ")
        return {"email": email, "contrasena": contrasena}

    @staticmethod
    def mostrar_administrador(administrador: Administrador) -> None:
        print("\n--- Datos del Administrador ---")
        print(administrador)
        print("-" * 38)

    @staticmethod
    def mostrar_lista_administradores(administradores: list[Administrador]) -> None:
        print("\n--- Lista de Administradores ---")
        if not administradores:
            print("No hay administradores registrados.")
        else:
            for a in administradores:
                print(a)
        print("-" * 38)

    @staticmethod
    def formulario_editar_administrador(administrador: Administrador) -> dict:
        print(f"\n--- Editando Administrador [ID: {administrador.id_usuario}] {administrador.nombre} ---")
        print("Deje en blanco si no desea modificar el campo.")

        nuevo_nombre = input(f"Nombre actual ({administrador.nombre}): ")
        if not nuevo_nombre.strip():
            nuevo_nombre = administrador.nombre

        nuevo_email = input(f"Email actual ({administrador.email}): ")
        if not nuevo_email.strip():
            nuevo_email = administrador.email

        nueva_contrasena = getpass("Nueva contraseña (dejar en blanco para mantener la actual): ")

        print(f"Nivel de permiso actual ({administrador.nivel_permiso})")
        print("Niveles disponibles: 1.- Basico, 2.- Medio, 3.- Alto, 4.- Superadmin (0 para mantener actual)")
        opcion_nivel = leer_numero("Seleccione un nivel: ")
        mapa_nivel = {1: "Basico", 2: "Medio", 3: "Alto", 4: "Superadmin"}
        nuevo_nivel = mapa_nivel.get(opcion_nivel, administrador.nivel_permiso)

        return {
            "id_usuario": administrador.id_usuario,
            "nombre": nuevo_nombre,
            "email": nuevo_email,
            "contrasena": nueva_contrasena,
            "nivel_permiso": nuevo_nivel
        }

    @staticmethod
    def confirmar_eliminacion(nombre: str) -> bool:
        return confirmar(f"¿Está seguro que desea eliminar al administrador '{nombre}'?")

    @staticmethod
    def mostrar_mensaje(mensaje: str) -> None:
        print(f"[ADMINISTRADORES] {mensaje}")
