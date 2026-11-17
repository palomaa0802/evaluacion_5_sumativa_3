from views.utils import leer_numero, leer_flotante, leer_fecha, confirmar
from models.registro_tiempo import RegistroTiempo
from models.empleado import Empleado
from models.proyecto import Proyecto


class RegistroTiempoView:
    @staticmethod
    def mostrar_menu() -> int:
        print("\n" + "-" * 38)
        print("    GESTIÓN DE REGISTROS DE TIEMPO")
        print("-" * 38)
        print("1.- Registrar horas trabajadas")
        print("2.- Editar registro de tiempo")
        print("3.- Eliminar registro de tiempo")
        print("4.- Imprimir un registro de tiempo")
        print("5.- Imprimir todos los registros y total de horas")
        print("0.- Volver al menú principal")
        print("-" * 38)
        return leer_numero("Seleccione una opción: ")

    @staticmethod
    def formulario_nuevo_registro(empleados: list[Empleado], proyectos: list[Proyecto]) -> dict:
        print("\n--- Nuevo Registro de Tiempo ---")
        fecha = leer_fecha("Ingrese la fecha del registro (YYYY-MM-DD): ")
        horas_trabajadas = leer_flotante("Ingrese las horas trabajadas (ej: 8.0): ")
        descripcion_tarea = input("Ingrese la descripción de la tarea realizada: ")

        print("\nEmpleados disponibles (Composición obligatoria):")
        for e in empleados:
            print(f"{e.id_usuario}.- {e.nombre} ({e.email})")
        id_empleado = leer_numero("Seleccione el ID del empleado: ")

        print("\nProyectos disponibles:")
        if proyectos:
            for p in proyectos:
                print(f"{p.id_proyecto}.- {p.nombre_proyecto}")
        else:
            print("No hay proyectos registrados.")
        opcion_proy = leer_numero("Seleccione el ID del proyecto (o 0 para ninguno): ")
        id_proyecto = opcion_proy if opcion_proy > 0 else None

        return {
            "fecha": fecha,
            "horas_trabajadas": horas_trabajadas,
            "descripcion_tarea": descripcion_tarea,
            "id_empleado": id_empleado,
            "id_proyecto": id_proyecto
        }

    @staticmethod
    def solicitar_id() -> int:
        return leer_numero("Ingrese el ID del registro de tiempo: ")

    @staticmethod
    def mostrar_registro(registro: RegistroTiempo) -> None:
        print("\n--- Datos del Registro de Tiempo ---")
        print(registro)
        print("-" * 38)

    @staticmethod
    def mostrar_lista_registros(registros: list[RegistroTiempo]) -> None:
        print("\n--- Lista de Registros de Tiempo ---")
        if not registros:
            print("No hay registros de tiempo ingresados.")
        else:
            for r in registros:
                print(r)
            total = registros[0].calcularTotalHoras(registros)
            print(f"\n-> Total acumulado (calcularTotalHoras): {total} horas")
        print("-" * 38)

    @staticmethod
    def formulario_editar_registro(
        registro: RegistroTiempo,
        empleados: list[Empleado],
        proyectos: list[Proyecto]
    ) -> dict:
        print(f"\n--- Editando Registro de Tiempo [ID: {registro.id_registro}] ---")
        print("Deje en blanco si no desea modificar el campo.")

        nueva_fecha = input(f"Fecha actual ({registro.fecha.isoformat()}): ")
        if not nueva_fecha.strip():
            nueva_fecha = registro.fecha.isoformat()

        nuevas_horas_input = input(f"Horas trabajadas actuales ({registro.horas_trabajadas}): ")
        try:
            nuevas_horas = float(nuevas_horas_input) if nuevas_horas_input.strip() else registro.horas_trabajadas
        except ValueError:
            nuevas_horas = registro.horas_trabajadas

        nueva_desc = input(f"Descripción tarea actual ({registro.descripcion_tarea}): ")
        if not nueva_desc.strip():
            nueva_desc = registro.descripcion_tarea

        emp_actual_id = registro.empleado.id_usuario if registro.empleado else None
        print("\nEmpleados disponibles:")
        for e in empleados:
            print(f"{e.id_usuario}.- {e.nombre}")
        emp_input = input(f"ID empleado actual ({emp_actual_id}, blanco para mantener): ")
        try:
            nuevo_id_emp = int(emp_input) if emp_input.strip() else emp_actual_id
        except ValueError:
            nuevo_id_emp = emp_actual_id

        proy_actual_id = registro.proyecto.id_proyecto if registro.proyecto else None
        proy_actual_str = proy_actual_id if proy_actual_id is not None else "Ninguno"
        print("\nProyectos disponibles:")
        if proyectos:
            for p in proyectos:
                print(f"{p.id_proyecto}.- {p.nombre_proyecto}")
        proy_input = input(f"ID proyecto actual ({proy_actual_str}, blanco para mantener, 0 para quitar): ")
        if not proy_input.strip():
            nuevo_id_proy = proy_actual_id
        else:
            try:
                op_p = int(proy_input)
                nuevo_id_proy = op_p if op_p > 0 else None
            except ValueError:
                nuevo_id_proy = proy_actual_id

        return {
            "id_registro": registro.id_registro,
            "fecha": nueva_fecha,
            "horas_trabajadas": nuevas_horas,
            "descripcion_tarea": nueva_desc,
            "id_empleado": nuevo_id_emp,
            "id_proyecto": nuevo_id_proy
        }

    @staticmethod
    def confirmar_eliminacion(id_registro: int) -> bool:
        return confirmar(f"¿Está seguro que desea eliminar el registro de tiempo ID {id_registro}?")

    @staticmethod
    def mostrar_mensaje(mensaje: str) -> None:
        print(f"[REGISTROS DE TIEMPO] {mensaje}")

    @staticmethod
    def formulario_registro_propio(proyectos: list[Proyecto]) -> dict:
        print("\n--- Registrar mis horas ---")
        fecha = leer_fecha("Ingrese la fecha del registro (YYYY-MM-DD): ")
        horas_trabajadas = leer_flotante("Ingrese las horas trabajadas (ej: 8.0): ")
        descripcion_tarea = input("Ingrese la descripción de la tarea realizada: ")

        print("\nProyectos disponibles:")
        if proyectos:
            for p in proyectos:
                print(f"{p.id_proyecto}.- {p.nombre_proyecto}")
        else:
            print("No hay proyectos registrados.")
        opcion_proy = leer_numero("Seleccione el ID del proyecto (o 0 para ninguno): ")

        return {
            "fecha": fecha,
            "horas_trabajadas": horas_trabajadas,
            "descripcion_tarea": descripcion_tarea,
            "id_proyecto": opcion_proy if opcion_proy > 0 else None
        }
