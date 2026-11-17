import logging

from config.errores import registrar_error
from models.consulta_externa_dao import ConsultaExternaDAO
from models.empleado import Empleado
from models.empleado_dao import EmpleadoDAO
from models.sesion import Sesion
from services.cambio_service import CambioService
from services.clima_service import ClimaService
from services.excepciones import ErrorServicio
from views.servicios_view import ServiciosView


class ServiciosController:
    """Clima y tipo de cambio. Solo se usa con una sesión iniciada y con límites de uso."""

    def __init__(self, sesion: Sesion):
        self.sesion = sesion
        self.view = ServiciosView()
        self.clima = ClimaService()
        self.cambio = CambioService()

    def ejecutar(self) -> None:
        while True:
            if not self.sesion.esta_activa():
                self.view.mostrar_mensaje("La sesión expiró por inactividad.")
                return
            opcion = self.view.mostrar_menu(self.sesion.es_admin)
            self.sesion.actividad()
            if opcion == 1:
                self.consultar_clima()
            elif opcion == 2:
                self.convertir_salario()
            elif opcion == 3 and self.sesion.es_admin:
                self.view.mostrar_historial(ConsultaExternaDAO.obtener_ultimas(10))
            elif opcion == 0:
                break
            else:
                self.view.mostrar_mensaje("Opción no válida.")

    def _permitido(self) -> bool:
        permitido, mensaje = self.sesion.permitir_consulta()
        if not permitido:
            self.view.mostrar_mensaje(mensaje)
        return permitido

    def _manejar_error(self, error: ErrorServicio) -> None:
        # el usuario ve un mensaje simple; el detalle técnico queda en errores.log
        self.view.mostrar_mensaje(error.mensaje_usuario)
        logging.warning(error.detalle_tecnico)

    def _guardar(self, tipo: str, detalle: str, resultado: str) -> None:
        ConsultaExternaDAO.registrar(self.sesion.usuario.id_usuario, self.sesion.rol, tipo, detalle, resultado)

    def consultar_clima(self) -> None:
        if not self._permitido():
            return
        ciudad = self.view.solicitar_ciudad()
        self.sesion.registrar_consulta()
        try:
            clima = self.clima.consultar(ciudad)
        except ErrorServicio as e:
            self._manejar_error(e)
            return
        except Exception as e:  # cualquier otro fallo inesperado no debe cerrar el programa
            registrar_error("consulta de clima", e)
            return

        if clima is None:
            self.view.mostrar_mensaje("Ciudad no válida. Use solo letras, espacios o guiones.")
            return
        if clima == {}:
            self.view.mostrar_mensaje("No se encontró esa ciudad.")
            return

        recomendacion = self.clima.evaluar_trabajo_en_terreno(clima)
        self.view.mostrar_clima(clima, recomendacion)
        resumen = f"{clima['temperatura']} C, {clima['estado']}, humedad {clima['humedad']}%"
        self._guardar("Clima", clima["ciudad"], resumen)

    def convertir_salario(self) -> None:
        if not self._permitido():
            return

        if self.sesion.es_admin:
            empleados = EmpleadoDAO.obtener_todos()
            if not empleados:
                self.view.mostrar_mensaje("No hay empleados registrados.")
                return
            empleado = EmpleadoDAO.obtener_por_id(self.view.solicitar_id_empleado(empleados))
        else:
            # un empleado solo puede convertir su propio salario
            empleado = EmpleadoDAO.obtener_por_id(self.sesion.usuario.id_usuario)
        if not isinstance(empleado, Empleado):
            self.view.mostrar_mensaje("Empleado no encontrado.")
            return

        moneda = self.view.solicitar_moneda()
        self.sesion.registrar_consulta()
        try:
            resultado = self.cambio.convertir_salario(empleado.salario, moneda)
        except ErrorServicio as e:
            self._manejar_error(e)
            return
        except Exception as e:
            registrar_error("conversión de salario", e)
            return

        if resultado is None:
            self.view.mostrar_mensaje("Moneda no válida. Elija una de la lista.")
            return

        self.view.mostrar_conversion(empleado.nombre, resultado)
        resumen = f"{resultado['monto']} {resultado['moneda']} por {resultado['salario_clp']:,.0f} CLP"
        self._guardar("Cambio", f"{empleado.nombre} a {resultado['moneda']}", resumen)
