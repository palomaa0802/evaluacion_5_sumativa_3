from views.main_view import MainView
from views.empleado_view import EmpleadoView
from controllers.auth_controller import AuthController
from controllers.empleado_controller import EmpleadoController
from controllers.departamento_controller import DepartamentoController
from controllers.proyecto_controller import ProyectoController
from controllers.registro_tiempo_controller import RegistroTiempoController
from controllers.administrador_controller import AdministradorController
from controllers.informe_controller import InformeController
from controllers.servicios_controller import ServiciosController
from models.empleado_dao import EmpleadoDAO
from models.sesion import Sesion


class MainController:
    def __init__(self):
        self.view = MainView()
        self.auth_controller = AuthController()
        self.empleado_controller = EmpleadoController()
        self.departamento_controller = DepartamentoController()
        self.proyecto_controller = ProyectoController()
        self.registro_tiempo_controller = RegistroTiempoController()
        self.administrador_controller = AdministradorController()
        self.informe_controller = InformeController()

    def ejecutar(self) -> None:
        self.auth_controller.crear_primer_administrador()
        while True:
            opcion = self.auth_controller.view.mostrar_menu_inicio()
            if opcion == 1:
                sesion = self.auth_controller.iniciar_sesion()
                if sesion is not None:
                    self._menu_sesion(sesion)
            elif opcion == 0:
                self.view.mostrar_mensaje("Gracias por usar el sistema de EcoTech Solutions. ¡Hasta luego!")
                break
            else:
                self.view.mostrar_mensaje("Opción no válida. Por favor, intente nuevamente.")

    def _menu_sesion(self, sesion: Sesion) -> None:
        servicios = ServiciosController(sesion)
        while True:
            if not sesion.esta_activa():
                self.view.mostrar_mensaje("La sesión expiró por inactividad. Inicie sesión de nuevo.")
                return
            if sesion.es_admin:
                opcion = self.view.mostrar_menu_admin(sesion.usuario.nombre, sesion.usuario.nivel_permiso)
            else:
                opcion = self.view.mostrar_menu_empleado(sesion.usuario.nombre)
            if not sesion.esta_activa():
                self.view.mostrar_mensaje("La sesión expiró por inactividad. Inicie sesión de nuevo.")
                return
            sesion.actividad()

            if opcion == 0:
                self.view.mostrar_mensaje("Sesión cerrada.")
                return
            if sesion.es_admin:
                self._opcion_admin(opcion, sesion, servicios)
            else:
                self._opcion_empleado(opcion, sesion, servicios)

    def _opcion_admin(self, opcion: int, sesion: Sesion, servicios: ServiciosController) -> None:
        if opcion == 1:
            self.empleado_controller.ejecutar()
        elif opcion == 2:
            self.departamento_controller.ejecutar()
        elif opcion == 3:
            self.proyecto_controller.ejecutar()
        elif opcion == 4:
            self.registro_tiempo_controller.ejecutar()
        elif opcion == 5:
            # solo el Superadmin puede crear, editar o eliminar administradores
            if sesion.es_superadmin:
                self.administrador_controller.ejecutar()
            else:
                self.view.mostrar_mensaje("Acceso denegado: solo un Superadmin gestiona administradores.")
        elif opcion == 6:
            self.informe_controller.ejecutar()
        elif opcion == 7:
            servicios.ejecutar()
        else:
            self.view.mostrar_mensaje("Opción no válida. Por favor, intente nuevamente.")

    def _opcion_empleado(self, opcion: int, sesion: Sesion, servicios: ServiciosController) -> None:
        id_empleado = sesion.usuario.id_usuario
        if opcion == 1:
            empleado = EmpleadoDAO.obtener_por_id(id_empleado)
            if empleado:
                EmpleadoView.mostrar_empleado(empleado)
        elif opcion == 2:
            self.registro_tiempo_controller.registrar_horas_propias(id_empleado)
        elif opcion == 3:
            self.registro_tiempo_controller.imprimir_registros_de(id_empleado)
        elif opcion == 4:
            servicios.ejecutar()
        else:
            self.view.mostrar_mensaje("Opción no válida. Por favor, intente nuevamente.")
