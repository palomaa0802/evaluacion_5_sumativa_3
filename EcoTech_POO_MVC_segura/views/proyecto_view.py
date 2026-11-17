from views.utils import leer_numero, leer_fecha, confirmar
from models.proyecto import Proyecto
from models.empleado import Empleado


class ProyectoView:
    @staticmethod
    def mostrar_menu() -> int:
        print("\n" + "-" * 35)
        print("       GESTIÓN DE PROYECTOS")
        print("-" * 35)
        print("1.- Agregar proyecto")
        print("2.- Editar proyecto")
        print("3.- Eliminar proyecto")
        print("4.- Imprimir un proyecto")
        print("5.- Imprimir todos los proyectos")
        print("6.- Asignar empleado a proyecto (asignarEmpleado)")
        print("0.- Volver al menú principal")
        print("-" * 35)
        return leer_numero("Seleccione una opción: ")

    @staticmethod
    def formulario_nuevo_proyecto() -> dict:
        print("\n--- Agregar Nuevo Proyecto ---")
        nombre_proyecto = input("Ingrese el nombre del proyecto: ")
        descripcion = input("Ingrese la descripción del proyecto: ")
        fecha_inicio = leer_fecha("Ingrese la fecha de inicio (YYYY-MM-DD): ")

        return {
            "nombre_proyecto": nombre_proyecto,
            "descripcion": descripcion,
            "fecha_inicio": fecha_inicio
        }

    @staticmethod
    def solicitar_id() -> int:
        return leer_numero("Ingrese el ID del proyecto: ")

    @staticmethod
    def formulario_asignar_empleado(proyectos: list[Proyecto], empleados: list[Empleado]) -> dict:
        print("\n--- Asignar Empleado a Proyecto ---")
        print("Proyectos disponibles:")
        for p in proyectos:
            print(f"{p.id_proyecto}.- {p.nombre_proyecto}")
        id_proyecto = leer_numero("Seleccione el ID del proyecto: ")

        print("\nEmpleados disponibles:")
        for e in empleados:
            print(f"{e.id_usuario}.- {e.nombre} ({e.email})")
        id_empleado = leer_numero("Seleccione el ID del empleado: ")

        return {
            "id_proyecto": id_proyecto,
            "id_empleado": id_empleado
        }

    @staticmethod
    def mostrar_proyecto(proyecto: Proyecto) -> None:
        print("\n--- Datos del Proyecto ---")
        print(proyecto)
        if proyecto.empleados:
            nombres = ", ".join(f"{e.nombre} (ID {e.id_usuario})" for e in proyecto.empleados)
            print(f"Empleados asignados: {nombres}")
        else:
            print("Empleados asignados: Ninguno")
        print("-" * 35)

    @staticmethod
    def mostrar_lista_proyectos(proyectos: list[Proyecto]) -> None:
        print("\n--- Lista de Proyectos ---")
        if not proyectos:
            print("No hay proyectos registrados.")
        else:
            for p in proyectos:
                emp_count = len(p.empleados)
                print(f"{p} | Empleados asignados: {emp_count}")
        print("-" * 35)

    @staticmethod
    def formulario_editar_proyecto(proyecto: Proyecto) -> dict:
        print(f"\n--- Editando Proyecto [ID: {proyecto.id_proyecto}] ---")
        print("Deje en blanco si no desea modificar el campo.")

        nuevo_nombre = input(f"Nombre actual ({proyecto.nombre_proyecto}): ")
        if not nuevo_nombre.strip():
            nuevo_nombre = proyecto.nombre_proyecto

        nueva_descripcion = input(f"Descripción actual ({proyecto.descripcion}): ")
        if not nueva_descripcion.strip():
            nueva_descripcion = proyecto.descripcion

        nueva_fecha = input(f"Fecha inicio actual ({proyecto.fecha_inicio.isoformat()}): ")
        if not nueva_fecha.strip():
            nueva_fecha = proyecto.fecha_inicio.isoformat()

        return {
            "id_proyecto": proyecto.id_proyecto,
            "nombre_proyecto": nuevo_nombre,
            "descripcion": nueva_descripcion,
            "fecha_inicio": nueva_fecha
        }

    @staticmethod
    def confirmar_eliminacion(nombre: str) -> bool:
        return confirmar(f"¿Está seguro que desea eliminar el proyecto '{nombre}'?")

    @staticmethod
    def mostrar_mensaje(mensaje: str) -> None:
        print(f"[PROYECTOS] {mensaje}")
