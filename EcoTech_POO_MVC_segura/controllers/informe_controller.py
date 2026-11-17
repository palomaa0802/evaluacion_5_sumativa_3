from models.informe import Informe
from models.informe_dao import InformeDAO
from models.administrador_dao import AdministradorDAO
from models.empleado_dao import EmpleadoDAO
from models.departamento_dao import DepartamentoDAO
from models.proyecto_dao import ProyectoDAO
from models.registro_tiempo_dao import RegistroTiempoDAO
from views.informe_view import InformeView


class InformeController:
    def __init__(self):
        self.view = InformeView()

    def ejecutar(self) -> None:
        while True:
            opcion = self.view.mostrar_menu()
            if opcion == 1:
                self.agregar_informe()
            elif opcion == 2:
                self.editar_informe()
            elif opcion == 3:
                self.eliminar_informe()
            elif opcion == 4:
                self.imprimir_informe()
            elif opcion == 5:
                self.imprimir_informes()
            elif opcion == 6:
                self.exportar_informe()
            elif opcion == 0:
                self.view.mostrar_mensaje("Saliendo de la gestión de informes.")
                break
            else:
                self.view.mostrar_mensaje("Opción no válida.")

    def _construir_resumen_automatico(self, tipo_informe: str) -> str:
        tipo = tipo_informe.capitalize()
        if tipo == "Empleados":
            empleados = EmpleadoDAO.obtener_todos()
            return f"Total empleados registrados: {len(empleados)}."
        elif tipo == "Proyectos":
            proyectos = ProyectoDAO.obtener_todos()
            return f"Total proyectos registrados: {len(proyectos)}."
        elif tipo == "Horas":
            registros = RegistroTiempoDAO.obtener_todos()
            total_horas = registros[0].calcularTotalHoras(registros) if registros else 0.0
            return f"Total registros: {len(registros)} | Horas acumuladas: {total_horas}h."
        elif tipo == "Departamentos":
            departamentos = DepartamentoDAO.obtener_todos()
            return f"Total departamentos activos: {len(departamentos)}."
        return "Informe consolidado del sistema EcoTech Solutions."

    def agregar_informe(self) -> None:
        administradores = AdministradorDAO.obtener_todos()
        datos = self.view.formulario_nuevo_informe(administradores)
        try:
            resumen_base = self._construir_resumen_automatico(datos["tipo_informe"])
            contenido_final = (
                f"{resumen_base} Observaciones: {datos['contenido']}"
                if datos["contenido"].strip()
                else resumen_base
            )

            admin = None
            if datos.get("id_administrador"):
                admin = AdministradorDAO.obtener_por_id(datos["id_administrador"])

            if admin:
                nuevo_informe = admin.generarInforme(datos["tipo_informe"], contenido_final)
            else:
                nuevo_informe = Informe(
                    tipo_informe=datos["tipo_informe"],
                    contenido=contenido_final
                )

            exito = InformeDAO.crear(nuevo_informe)
            if exito:
                self.view.mostrar_mensaje(f"Informe generado exitosamente con ID {nuevo_informe.id_informe}.")
            else:
                self.view.mostrar_mensaje("Error al guardar el informe en la base de datos.")
        except (ValueError, TypeError) as e:
            self.view.mostrar_mensaje(f"Error en los datos del informe: {e}")

    def editar_informe(self) -> None:
        id_informe = self.view.solicitar_id()
        informe = InformeDAO.obtener_por_id(id_informe)
        if not informe:
            self.view.mostrar_mensaje("Informe no encontrado.")
            return

        datos_nuevos = self.view.formulario_editar_informe(informe)
        try:
            informe.tipo_informe = datos_nuevos["tipo_informe"]
            informe.fecha_generacion = datos_nuevos["fecha_generacion"]
            informe.contenido = datos_nuevos["contenido"]

            exito = InformeDAO.actualizar(informe)
            if exito:
                self.view.mostrar_mensaje("Informe actualizado exitosamente.")
            else:
                self.view.mostrar_mensaje("Error al actualizar en la base de datos.")
        except (ValueError, TypeError) as e:
            self.view.mostrar_mensaje(f"Error en los datos modificados: {e}")

    def eliminar_informe(self) -> None:
        id_informe = self.view.solicitar_id()
        informe = InformeDAO.obtener_por_id(id_informe)
        if not informe:
            self.view.mostrar_mensaje("Informe no encontrado.")
            return

        if self.view.confirmar_eliminacion(id_informe):
            exito = InformeDAO.eliminar(id_informe)
            if exito:
                self.view.mostrar_mensaje("Informe eliminado exitosamente.")
            else:
                self.view.mostrar_mensaje("Error al eliminar en la base de datos.")
        else:
            self.view.mostrar_mensaje("Operación cancelada.")

    def imprimir_informe(self) -> None:
        id_informe = self.view.solicitar_id()
        informe = InformeDAO.obtener_por_id(id_informe)
        if informe:
            self.view.mostrar_informe(informe)
        else:
            self.view.mostrar_mensaje("Informe no encontrado.")

    def imprimir_informes(self) -> None:
        informes = InformeDAO.obtener_todos()
        self.view.mostrar_lista_informes(informes)

    def exportar_informe(self) -> None:
        id_informe = self.view.solicitar_id()
        informe = InformeDAO.obtener_por_id(id_informe)
        if not informe:
            self.view.mostrar_mensaje("Informe no encontrado.")
            return

        formato = self.view.solicitar_formato_exportacion()
        try:
            resultado = informe.exportar(formato)
            self.view.mostrar_mensaje(resultado)
        except (ValueError, TypeError, OSError) as e:
            self.view.mostrar_mensaje(f"Error al exportar el informe: {e}")
