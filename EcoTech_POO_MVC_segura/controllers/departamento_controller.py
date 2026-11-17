from models.departamento import Departamento
from models.departamento_dao import DepartamentoDAO
from models.empleado_dao import EmpleadoDAO
from views.departamento_view import DepartamentoView


class DepartamentoController:
    def __init__(self):
        self.view = DepartamentoView()

    def ejecutar(self) -> None:
        while True:
            opcion = self.view.mostrar_menu()
            if opcion == 1:
                self.agregar_departamento()
            elif opcion == 2:
                self.editar_departamento()
            elif opcion == 3:
                self.eliminar_departamento()
            elif opcion == 4:
                self.imprimir_departamento()
            elif opcion == 5:
                self.imprimir_departamentos()
            elif opcion == 0:
                self.view.mostrar_mensaje("Saliendo de la gestión de departamentos.")
                break
            else:
                self.view.mostrar_mensaje("Opción no válida.")

    def agregar_departamento(self) -> None:
        empleados = EmpleadoDAO.obtener_todos()
        datos = self.view.formulario_nuevo_departamento(empleados)
        try:
            gerente = None
            if datos.get("id_gerente"):
                gerente = EmpleadoDAO.obtener_por_id(datos["id_gerente"])

            nuevo_departamento = Departamento(
                nombre_depto=datos["nombre_depto"],
                gerente=gerente
            )
            exito = DepartamentoDAO.crear(nuevo_departamento)
            if exito:
                self.view.mostrar_mensaje(
                    f"Departamento agregado exitosamente con ID {nuevo_departamento.id_departamento}."
                )
            else:
                self.view.mostrar_mensaje("Error al guardar en la base de datos.")
        except (ValueError, TypeError) as e:
            self.view.mostrar_mensaje(f"Error en los datos ingresados: {e}")

    def editar_departamento(self) -> None:
        id_depto = self.view.solicitar_id()
        departamento = DepartamentoDAO.obtener_por_id(id_depto)
        if not departamento:
            self.view.mostrar_mensaje("Departamento no encontrado.")
            return

        empleados = EmpleadoDAO.obtener_todos()
        datos_nuevos = self.view.formulario_editar_departamento(departamento, empleados)
        try:
            departamento.nombre_depto = datos_nuevos["nombre_depto"]
            gerente = None
            if datos_nuevos.get("id_gerente"):
                gerente = EmpleadoDAO.obtener_por_id(datos_nuevos["id_gerente"])
            departamento.gerente = gerente

            exito = DepartamentoDAO.actualizar(departamento)
            if exito:
                self.view.mostrar_mensaje("Departamento actualizado exitosamente.")
            else:
                self.view.mostrar_mensaje("Error al actualizar en la base de datos.")
        except (ValueError, TypeError) as e:
            self.view.mostrar_mensaje(f"Error en los datos modificados: {e}")

    def eliminar_departamento(self) -> None:
        id_depto = self.view.solicitar_id()
        departamento = DepartamentoDAO.obtener_por_id(id_depto)
        if not departamento:
            self.view.mostrar_mensaje("Departamento no encontrado.")
            return

        if self.view.confirmar_eliminacion(departamento.getNombreDepto()):
            exito = DepartamentoDAO.eliminar(id_depto)
            if exito:
                self.view.mostrar_mensaje("Departamento eliminado exitosamente.")
            else:
                self.view.mostrar_mensaje("Error al eliminar en la base de datos.")
        else:
            self.view.mostrar_mensaje("Operación cancelada.")

    def imprimir_departamento(self) -> None:
        id_depto = self.view.solicitar_id()
        departamento = DepartamentoDAO.obtener_por_id(id_depto)
        if departamento:
            self.view.mostrar_departamento(departamento)
        else:
            self.view.mostrar_mensaje("Departamento no encontrado.")

    def imprimir_departamentos(self) -> None:
        departamentos = DepartamentoDAO.obtener_todos()
        self.view.mostrar_lista_departamentos(departamentos)
