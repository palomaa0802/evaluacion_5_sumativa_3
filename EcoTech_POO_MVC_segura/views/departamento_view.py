from views.utils import leer_numero, confirmar
from models.departamento import Departamento
from models.empleado import Empleado


class DepartamentoView:
    @staticmethod
    def mostrar_menu() -> int:
        print("\n" + "-" * 35)
        print("    GESTIÓN DE DEPARTAMENTOS")
        print("-" * 35)
        print("1.- Agregar departamento")
        print("2.- Editar departamento")
        print("3.- Eliminar departamento")
        print("4.- Imprimir un departamento")
        print("5.- Imprimir todos los departamentos")
        print("0.- Volver al menú principal")
        print("-" * 35)
        return leer_numero("Seleccione una opción: ")

    @staticmethod
    def formulario_nuevo_departamento(empleados: list[Empleado]) -> dict:
        print("\n--- Agregar Nuevo Departamento ---")
        nombre_depto = input("Ingrese el nombre del departamento: ")

        print("\nEmpleados disponibles para asignar como Gerente:")
        if empleados:
            for e in empleados:
                print(f"{e.id_usuario}.- {e.nombre} ({e.email})")
        else:
            print("No hay empleados registrados.")

        opcion_gerente = leer_numero("Seleccione el ID del empleado gerente (o 0 para ninguno): ")
        id_gerente = opcion_gerente if opcion_gerente > 0 else None

        return {
            "nombre_depto": nombre_depto,
            "id_gerente": id_gerente
        }

    @staticmethod
    def solicitar_id() -> int:
        return leer_numero("Ingrese el ID del departamento: ")

    @staticmethod
    def mostrar_departamento(departamento: Departamento) -> None:
        print("\n--- Datos del Departamento ---")
        print(departamento)
        print("-" * 35)

    @staticmethod
    def mostrar_lista_departamentos(departamentos: list[Departamento]) -> None:
        print("\n--- Lista de Departamentos ---")
        if not departamentos:
            print("No hay departamentos registrados.")
        else:
            for d in departamentos:
                print(d)
        print("-" * 35)

    @staticmethod
    def formulario_editar_departamento(departamento: Departamento, empleados: list[Empleado]) -> dict:
        print(f"\n--- Editando Departamento [ID: {departamento.id_departamento}] ---")
        print("Deje en blanco si no desea modificar el campo.")

        nuevo_nombre = input(f"Nombre actual ({departamento.nombre_depto}): ")
        if not nuevo_nombre.strip():
            nuevo_nombre = departamento.nombre_depto

        print("\nEmpleados disponibles para Gerente:")
        if empleados:
            for e in empleados:
                print(f"{e.id_usuario}.- {e.nombre} ({e.email})")
        else:
            print("No hay empleados registrados.")

        gerente_actual_id = departamento.gerente.id_usuario if departamento.gerente else None
        gerente_actual_str = gerente_actual_id if gerente_actual_id is not None else "Ninguno"
        opcion_gerente_input = input(
            f"Seleccione nuevo ID de gerente (Actual: {gerente_actual_str}, blanco para mantener, 0 para quitar): "
        )

        if not opcion_gerente_input.strip():
            nuevo_id_gerente = gerente_actual_id
        else:
            try:
                op_g = int(opcion_gerente_input)
                nuevo_id_gerente = op_g if op_g > 0 else None
            except ValueError:
                nuevo_id_gerente = gerente_actual_id

        return {
            "id_departamento": departamento.id_departamento,
            "nombre_depto": nuevo_nombre,
            "id_gerente": nuevo_id_gerente
        }

    @staticmethod
    def confirmar_eliminacion(nombre: str) -> bool:
        return confirmar(f"¿Está seguro que desea eliminar el departamento '{nombre}'?")

    @staticmethod
    def mostrar_mensaje(mensaje: str) -> None:
        print(f"[DEPARTAMENTOS] {mensaje}")
