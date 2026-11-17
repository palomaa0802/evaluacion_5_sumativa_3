import time

from config.seguridad import Seguridad
from models.administrador import Administrador
from models.administrador_dao import AdministradorDAO
from models.empleado_dao import EmpleadoDAO
from models.sesion import Sesion
from services.validaciones import ValidacionesServicios
from views.auth_view import AuthView


class AuthController:
    MAX_FALLOS = 3
    SEGUNDOS_BLOQUEO = 60

    def __init__(self):
        self.view = AuthView()
        # correo -> (cantidad de fallos, momento del último fallo). Se reinicia al cerrar el programa.
        self.__fallos: dict[str, tuple[int, float]] = {}

    def crear_primer_administrador(self) -> None:
        """Si no hay ningún administrador, se crea el primero (Superadmin)."""
        if AdministradorDAO.obtener_todos():
            return
        datos = self.view.formulario_primer_administrador()
        if datos["contrasena"] != datos["repetida"]:
            self.view.mostrar_mensaje("Las contraseñas no coinciden.")
            return
        try:
            admin = Administrador(
                nombre=datos["nombre"],
                email=datos["email"],
                contrasena=datos["contrasena"],
                nivel_permiso="Superadmin"
            )
            if AdministradorDAO.crear(admin):
                self.view.mostrar_mensaje("Administrador creado. Ya puede iniciar sesión.")
        except (ValueError, TypeError) as e:
            self.view.mostrar_mensaje(f"Error en los datos ingresados: {e}")

    def _segundos_bloqueo(self, email: str) -> int:
        if email not in self.__fallos:
            return 0
        cantidad, ultimo = self.__fallos[email]
        if cantidad < self.MAX_FALLOS:
            return 0
        restante = self.SEGUNDOS_BLOQUEO - (time.time() - ultimo)
        if restante <= 0:
            del self.__fallos[email]
            return 0
        return int(restante) + 1

    def _anotar_fallo(self, email: str) -> None:
        cantidad = self.__fallos[email][0] if email in self.__fallos else 0
        self.__fallos[email] = (cantidad + 1, time.time())

    def iniciar_sesion(self) -> Sesion | None:
        """Pide las credenciales y devuelve una Sesión si son correctas."""
        while True:
            credenciales = self.view.solicitar_credenciales()
            if credenciales is None:
                return None

            email = ValidacionesServicios.sanear_email(credenciales["email"])
            if email is None:
                self.view.mostrar_mensaje("Correo o contraseña incorrectos.")
                continue

            espera = self._segundos_bloqueo(email)
            if espera > 0:
                self.view.mostrar_mensaje(f"Demasiados intentos. Espere {espera} segundos.")
                return None

            usuario = AdministradorDAO.obtener_por_email(email) or EmpleadoDAO.obtener_por_email(email)
            if usuario is not None and usuario.iniciarSesion(email, credenciales["contrasena"]):
                self.__fallos.pop(email, None)
                self.view.mostrar_mensaje(f"Bienvenido/a, {usuario.getNombre()}.")
                return Sesion(usuario)

            if usuario is None:
                # se calcula igual un hash para que no se note si el correo existe o no
                Seguridad.cifrar(credenciales["contrasena"], "00" * 16)
            self._anotar_fallo(email)
            # mismo mensaje exista o no el correo
            self.view.mostrar_mensaje("Correo o contraseña incorrectos.")
