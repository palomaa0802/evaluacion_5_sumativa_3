from models.proyecto import Proyecto
from models.proyecto_dao import ProyectoDAO
from models.empleado_dao import EmpleadoDAO
from views.proyecto_view import ProyectoView


class ProyectoController:
    def __init__(self):
        self.view = ProyectoView()

    def ejecutar(self) -> None:
        while True:
            opcion = self.view.mostrar_menu()
            if opcion == 1:
                self.agregar_proyecto()
            elif opcion == 2:
                self.editar_proyecto()
            elif opcion == 3:
                self.eliminar_proyecto()
            elif opcion == 4:
                self.imprimir_proyecto()
            elif opcion == 5:
                self.imprimir_proyectos()
            elif opcion == 6:
                self.asignar_empleado_a_proyecto()
            elif opcion == 0:
                self.view.mostrar_mensaje("Saliendo de la gestión de proyectos.")
                break
            else:
                self.view.mostrar_mensaje("Opción no válida.")

    def agregar_proyecto(self) -> None:
        datos = self.view.formulario_nuevo_proyecto()
        try:
            nuevo_proyecto = Proyecto(
                nombre_proyecto=datos["nombre_proyecto"],
                descripcion=datos["descripcion"],
                fecha_inicio=datos["fecha_inicio"]
            )
            exito = ProyectoDAO.crear(nuevo_proyecto)
            if exito:
                self.view.mostrar_mensaje(f"Proyecto agregado exitosamente con ID {nuevo_proyecto.id_proyecto}.")
            else:
                self.view.mostrar_mensaje("Error al guardar en la base de datos.")
        except (ValueError, TypeError) as e:
            self.view.mostrar_mensaje(f"Error en los datos ingresados: {e}")

    def editar_proyecto(self) -> None:
        id_proyecto = self.view.solicitar_id()
        proyecto = ProyectoDAO.obtener_por_id(id_proyecto)
        if not proyecto:
            self.view.mostrar_mensaje("Proyecto no encontrado.")
            return

        datos_nuevos = self.view.formulario_editar_proyecto(proyecto)
        try:
            proyecto.nombre_proyecto = datos_nuevos["nombre_proyecto"]
            proyecto.descripcion = datos_nuevos["descripcion"]
            proyecto.fecha_inicio = datos_nuevos["fecha_inicio"]

            exito = ProyectoDAO.actualizar(proyecto)
            if exito:
                self.view.mostrar_mensaje("Proyecto actualizado exitosamente.")
            else:
                self.view.mostrar_mensaje("Error al actualizar en la base de datos.")
        except (ValueError, TypeError) as e:
            self.view.mostrar_mensaje(f"Error en los datos modificados: {e}")

    def eliminar_proyecto(self) -> None:
        id_proyecto = self.view.solicitar_id()
        proyecto = ProyectoDAO.obtener_por_id(id_proyecto)
        if not proyecto:
            self.view.mostrar_mensaje("Proyecto no encontrado.")
            return

        if self.view.confirmar_eliminacion(proyecto.getNombreProyecto()):
            exito = ProyectoDAO.eliminar(id_proyecto)
            if exito:
                self.view.mostrar_mensaje("Proyecto eliminado exitosamente.")
            else:
                self.view.mostrar_mensaje("Error al eliminar en la base de datos.")
        else:
            self.view.mostrar_mensaje("Operación cancelada.")

    def imprimir_proyecto(self) -> None:
        id_proyecto = self.view.solicitar_id()
        proyecto = ProyectoDAO.obtener_por_id(id_proyecto)
        if proyecto:
            self.view.mostrar_proyecto(proyecto)
        else:
            self.view.mostrar_mensaje("Proyecto no encontrado.")

    def imprimir_proyectos(self) -> None:
        proyectos = ProyectoDAO.obtener_todos()
        self.view.mostrar_lista_proyectos(proyectos)

    def asignar_empleado_a_proyecto(self) -> None:
        proyectos = ProyectoDAO.obtener_todos()
        empleados = EmpleadoDAO.obtener_todos()
        if not proyectos or not empleados:
            self.view.mostrar_mensaje("Debe existir al menos un proyecto y un empleado registrados.")
            return

        datos = self.view.formulario_asignar_empleado(proyectos, empleados)
        proyecto = ProyectoDAO.obtener_por_id(datos["id_proyecto"])
        empleado = EmpleadoDAO.obtener_por_id(datos["id_empleado"])
        if not proyecto or not empleado:
            self.view.mostrar_mensaje("Proyecto o Empleado no encontrado.")
            return

        try:
            proyecto.asignarEmpleado(empleado)
            exito = ProyectoDAO.asignar_empleado(proyecto.id_proyecto, empleado.id_usuario)
            if exito:
                self.view.mostrar_mensaje(
                    f"Empleado '{empleado.getNombre()}' asignado al proyecto '{proyecto.getNombreProyecto()}'."
                )
            else:
                self.view.mostrar_mensaje("El empleado ya está asignado a este proyecto o ocurrió un error.")
        except (ValueError, TypeError) as e:
            self.view.mostrar_mensaje(f"Error al asignar empleado: {e}")
