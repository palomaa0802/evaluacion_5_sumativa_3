from models.registro_tiempo import RegistroTiempo
from models.registro_tiempo_dao import RegistroTiempoDAO
from models.empleado_dao import EmpleadoDAO
from models.proyecto_dao import ProyectoDAO
from views.registro_tiempo_view import RegistroTiempoView


class RegistroTiempoController:
    def __init__(self):
        self.view = RegistroTiempoView()

    def ejecutar(self) -> None:
        while True:
            opcion = self.view.mostrar_menu()
            if opcion == 1:
                self.agregar_registro()
            elif opcion == 2:
                self.editar_registro()
            elif opcion == 3:
                self.eliminar_registro()
            elif opcion == 4:
                self.imprimir_registro()
            elif opcion == 5:
                self.imprimir_registros()
            elif opcion == 0:
                self.view.mostrar_mensaje("Saliendo de la gestión de registros de tiempo.")
                break
            else:
                self.view.mostrar_mensaje("Opción no válida.")

    def agregar_registro(self) -> None:
        empleados = EmpleadoDAO.obtener_todos()
        if not empleados:
            self.view.mostrar_mensaje("Debe registrar al menos un empleado antes de ingresar horas trabajadas.")
            return

        proyectos = ProyectoDAO.obtener_todos()
        datos = self.view.formulario_nuevo_registro(empleados, proyectos)
        try:
            empleado = EmpleadoDAO.obtener_por_id(datos["id_empleado"])
            if not empleado:
                self.view.mostrar_mensaje("Error: El empleado seleccionado no existe.")
                return

            proyecto = None
            if datos.get("id_proyecto"):
                proyecto = ProyectoDAO.obtener_por_id(datos["id_proyecto"])

            nuevo_registro = RegistroTiempo(
                fecha=datos["fecha"],
                horas_trabajadas=datos["horas_trabajadas"],
                descripcion_tarea=datos["descripcion_tarea"],
                empleado=empleado,
                proyecto=proyecto
            )
            empleado.registrarHoras(nuevo_registro)

            exito = RegistroTiempoDAO.crear(nuevo_registro)
            if exito:
                self.view.mostrar_mensaje(
                    f"Registro de tiempo guardado exitosamente con ID {nuevo_registro.id_registro}."
                )
            else:
                self.view.mostrar_mensaje("Error al guardar en la base de datos.")
        except (ValueError, TypeError) as e:
            self.view.mostrar_mensaje(f"Error en los datos ingresados: {e}")

    def editar_registro(self) -> None:
        id_registro = self.view.solicitar_id()
        registro = RegistroTiempoDAO.obtener_por_id(id_registro)
        if not registro:
            self.view.mostrar_mensaje("Registro de tiempo no encontrado.")
            return

        empleados = EmpleadoDAO.obtener_todos()
        proyectos = ProyectoDAO.obtener_todos()
        datos_nuevos = self.view.formulario_editar_registro(registro, empleados, proyectos)
        try:
            empleado = EmpleadoDAO.obtener_por_id(datos_nuevos["id_empleado"])
            if not empleado:
                self.view.mostrar_mensaje("Error: El empleado indicado no existe.")
                return

            proyecto = None
            if datos_nuevos.get("id_proyecto"):
                proyecto = ProyectoDAO.obtener_por_id(datos_nuevos["id_proyecto"])

            registro.fecha = datos_nuevos["fecha"]
            registro.horas_trabajadas = datos_nuevos["horas_trabajadas"]
            registro.descripcion_tarea = datos_nuevos["descripcion_tarea"]
            registro.empleado = empleado
            registro.proyecto = proyecto

            exito = RegistroTiempoDAO.actualizar(registro)
            if exito:
                self.view.mostrar_mensaje("Registro de tiempo actualizado exitosamente.")
            else:
                self.view.mostrar_mensaje("Error al actualizar en la base de datos.")
        except (ValueError, TypeError) as e:
            self.view.mostrar_mensaje(f"Error en los datos modificados: {e}")

    def eliminar_registro(self) -> None:
        id_registro = self.view.solicitar_id()
        registro = RegistroTiempoDAO.obtener_por_id(id_registro)
        if not registro:
            self.view.mostrar_mensaje("Registro de tiempo no encontrado.")
            return

        if self.view.confirmar_eliminacion(id_registro):
            exito = RegistroTiempoDAO.eliminar(id_registro)
            if exito:
                self.view.mostrar_mensaje("Registro de tiempo eliminado exitosamente.")
            else:
                self.view.mostrar_mensaje("Error al eliminar en la base de datos.")
        else:
            self.view.mostrar_mensaje("Operación cancelada.")

    def imprimir_registro(self) -> None:
        id_registro = self.view.solicitar_id()
        registro = RegistroTiempoDAO.obtener_por_id(id_registro)
        if registro:
            self.view.mostrar_registro(registro)
        else:
            self.view.mostrar_mensaje("Registro de tiempo no encontrado.")

    def imprimir_registros(self) -> None:
        registros = RegistroTiempoDAO.obtener_todos()
        self.view.mostrar_lista_registros(registros)

    def registrar_horas_propias(self, id_empleado: int) -> None:
        """Un empleado registra horas solo a su propio nombre."""
        empleado = EmpleadoDAO.obtener_por_id(id_empleado)
        if not empleado:
            self.view.mostrar_mensaje("Empleado no encontrado.")
            return

        datos = self.view.formulario_registro_propio(ProyectoDAO.obtener_todos())
        try:
            proyecto = ProyectoDAO.obtener_por_id(datos["id_proyecto"]) if datos["id_proyecto"] else None
            nuevo_registro = RegistroTiempo(
                fecha=datos["fecha"],
                horas_trabajadas=datos["horas_trabajadas"],
                descripcion_tarea=datos["descripcion_tarea"],
                empleado=empleado,
                proyecto=proyecto
            )
            if RegistroTiempoDAO.crear(nuevo_registro):
                self.view.mostrar_mensaje(f"Registro guardado con ID {nuevo_registro.id_registro}.")
            else:
                self.view.mostrar_mensaje("Error al guardar en la base de datos.")
        except (ValueError, TypeError) as e:
            self.view.mostrar_mensaje(f"Error en los datos ingresados: {e}")

    def imprimir_registros_de(self, id_empleado: int) -> None:
        """Muestra solo los registros de un empleado."""
        propios = [r for r in RegistroTiempoDAO.obtener_todos() if r.empleado and r.empleado.id_usuario == id_empleado]
        self.view.mostrar_lista_registros(propios)
