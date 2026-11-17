from views.utils import leer_numero, confirmar
from models.informe import Informe
from models.administrador import Administrador


class InformeView:
    @staticmethod
    def mostrar_menu() -> int:
        print("\n" + "-" * 38)
        print("         GESTIÓN DE INFORMES")
        print("-" * 38)
        print("1.- Generar nuevo informe (vía Administrador)")
        print("2.- Editar informe")
        print("3.- Eliminar informe")
        print("4.- Imprimir un informe")
        print("5.- Imprimir todos los informes")
        print("6.- Exportar informe (TXT / CSV / CONSOLA)")
        print("0.- Volver al menú principal")
        print("-" * 38)
        return leer_numero("Seleccione una opción: ")

    @staticmethod
    def formulario_nuevo_informe(administradores: list[Administrador]) -> dict:
        print("\n--- Generar Nuevo Informe ---")
        print("Tipos de informe sugeridos: 1.- Empleados, 2.- Proyectos, 3.- Horas, 4.- Departamentos, 5.- General")
        opcion_tipo = leer_numero("Seleccione el tipo de informe (1-5): ")
        mapa_tipo = {
            1: "Empleados",
            2: "Proyectos",
            3: "Horas",
            4: "Departamentos",
            5: "General"
        }
        tipo_informe = mapa_tipo.get(opcion_tipo, "General")
        contenido = input("Ingrese observaciones adicionales (o deje en blanco para resumen automático): ")

        id_administrador = None
        if administradores:
            print("\nAdministradores disponibles para firmar el informe:")
            for a in administradores:
                print(f"{a.id_usuario}.- {a.nombre} (Permiso: {a.nivel_permiso})")
            op_adm = leer_numero("Seleccione el ID del administrador (o 0 para ninguno): ")
            id_administrador = op_adm if op_adm > 0 else None

        return {
            "tipo_informe": tipo_informe,
            "contenido": contenido,
            "id_administrador": id_administrador
        }

    @staticmethod
    def solicitar_id() -> int:
        return leer_numero("Ingrese el ID del informe: ")

    @staticmethod
    def solicitar_formato_exportacion() -> str:
        print("Formatos disponibles: 1.- TXT, 2.- CSV, 3.- CONSOLA")
        op = leer_numero("Seleccione formato (1-3): ")
        mapa = {1: "TXT", 2: "CSV", 3: "CONSOLA"}
        return mapa.get(op, "")

    @staticmethod
    def mostrar_informe(informe: Informe) -> None:
        print("\n--- Datos del Informe ---")
        print(informe)
        print("-" * 38)

    @staticmethod
    def mostrar_lista_informes(informes: list[Informe]) -> None:
        print("\n--- Lista de Informes ---")
        if not informes:
            print("No hay informes registrados.")
        else:
            for inf in informes:
                print(inf)
        print("-" * 38)

    @staticmethod
    def formulario_editar_informe(informe: Informe) -> dict:
        print(f"\n--- Editando Informe [ID: {informe.id_informe}] ---")
        print("Deje en blanco si no desea modificar el campo.")

        nuevo_tipo = input(f"Tipo de informe actual ({informe.tipo_informe}): ")
        if not nuevo_tipo.strip():
            nuevo_tipo = informe.tipo_informe

        nueva_fecha = input(f"Fecha de generación actual ({informe.fecha_generacion.isoformat()}): ")
        if not nueva_fecha.strip():
            nueva_fecha = informe.fecha_generacion.isoformat()

        nuevo_contenido = input(f"Contenido actual ({informe.contenido}): ")
        if not nuevo_contenido.strip():
            nuevo_contenido = informe.contenido

        return {
            "id_informe": informe.id_informe,
            "tipo_informe": nuevo_tipo,
            "fecha_generacion": nueva_fecha,
            "contenido": nuevo_contenido
        }

    @staticmethod
    def confirmar_eliminacion(id_informe: int) -> bool:
        return confirmar(f"¿Está seguro que desea eliminar el informe ID {id_informe}?")

    @staticmethod
    def mostrar_mensaje(mensaje: str) -> None:
        print(f"[INFORMES] {mensaje}")
