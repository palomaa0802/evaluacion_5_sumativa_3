from views.utils import leer_numero


class MainView:
    @staticmethod
    def mostrar_menu_admin(nombre: str, nivel: str) -> int:
        print("\n" + "=" * 42)
        print("   ECOTECH SOLUTIONS - MENÚ ADMINISTRADOR")
        print(f"   Sesión: {nombre} ({nivel})")
        print("=" * 42)
        print("1.- Gestión de Empleados")
        print("2.- Gestión de Departamentos")
        print("3.- Gestión de Proyectos")
        print("4.- Gestión de Registros de Tiempo")
        print("5.- Gestión de Administradores (solo Superadmin)")
        print("6.- Gestión de Informes")
        print("7.- Servicios externos (clima y tipo de cambio)")
        print("0.- Cerrar sesión")
        print("=" * 42)
        return leer_numero("Seleccione una opción: ")

    @staticmethod
    def mostrar_menu_empleado(nombre: str) -> int:
        print("\n" + "=" * 42)
        print("   ECOTECH SOLUTIONS - MENÚ EMPLEADO")
        print(f"   Sesión: {nombre}")
        print("=" * 42)
        print("1.- Ver mis datos")
        print("2.- Registrar mis horas")
        print("3.- Ver mis registros y total de horas")
        print("4.- Servicios externos (clima y tipo de cambio)")
        print("0.- Cerrar sesión")
        print("=" * 42)
        return leer_numero("Seleccione una opción: ")

    @staticmethod
    def mostrar_mensaje(mensaje: str) -> None:
        print(f"\n[SISTEMA] {mensaje}")
