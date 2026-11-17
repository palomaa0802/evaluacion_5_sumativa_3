from views.utils import leer_numero
from services.validaciones import MONEDAS_PERMITIDAS


class ServiciosView:
    @staticmethod
    def mostrar_menu(es_admin: bool) -> int:
        print("\n" + "-" * 38)
        print("     SERVICIOS EXTERNOS")
        print("-" * 38)
        print("1.- Consultar clima de una ciudad (visita a terreno)")
        print("2.- Convertir salario a otra moneda")
        if es_admin:
            print("3.- Ver historial de consultas")
        print("0.- Volver")
        print("-" * 38)
        return leer_numero("Seleccione una opción: ")

    @staticmethod
    def solicitar_ciudad() -> str:
        return input("Ciudad donde se hará la visita: ")

    @staticmethod
    def solicitar_moneda() -> str:
        print("Monedas disponibles:", ", ".join(MONEDAS_PERMITIDAS))
        return input("Moneda a la que quiere convertir: ")

    @staticmethod
    def solicitar_id_empleado(empleados: list) -> int:
        print("\nEmpleados disponibles:")
        for e in empleados:
            print(f"{e.id_usuario}.- {e.nombre} (${e.salario:,.0f} CLP)")
        return leer_numero("Seleccione el ID del empleado: ")

    @staticmethod
    def mostrar_clima(clima: dict, recomendacion: str) -> None:
        print(f"\nClima actual en {clima['ciudad']} - {clima['pais']}")
        print(f"Temperatura: {clima['temperatura']} °C")
        print(f"Estado del tiempo: {clima['estado']}")
        print(f"Humedad: {clima['humedad']} %")
        print(f"Viento: {clima['viento']} km/h")
        print(recomendacion)

    @staticmethod
    def mostrar_conversion(nombre: str, resultado: dict) -> None:
        print(f"\nSalario de {nombre}: {resultado['salario_clp']:,.0f} CLP")
        print(f"Tipo de cambio: 1 CLP = {resultado['tipo_cambio']:.6f} {resultado['moneda']}")
        print(f"Equivale a: {resultado['monto']:,.2f} {resultado['moneda']}")
        print("Fuente de los tipos de cambio: ExchangeRate-API (exchangerate-api.com)")

    @staticmethod
    def mostrar_historial(filas: list) -> None:
        print("\n--- Últimas consultas ---")
        if not filas:
            print("Todavía no hay consultas guardadas.")
        for f in filas:
            print(f"{f['fecha']} | usuario {f['id_usuario']} ({f['rol']}) | {f['tipo']} | {f['detalle']} | {f['resultado']}")
        print("-" * 38)

    @staticmethod
    def mostrar_mensaje(mensaje: str) -> None:
        print(f"[SERVICIOS] {mensaje}")
