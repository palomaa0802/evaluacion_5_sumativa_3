import time

from models.usuario import Usuario
from models.administrador import Administrador


class Sesion:
    """
    Controla la sesión de un usuario ya autenticado: cuánto tiempo puede estar
    inactivo y cuántas consultas a servicios externos puede hacer.
    """
    TIEMPO_MAXIMO_INACTIVIDAD = 300   # 5 minutos sin actividad y la sesión se cierra
    MAXIMO_CONSULTAS = 10             # consultas a APIs permitidas por sesión
    ESPERA_MINIMA = 2                 # segundos entre una consulta y otra

    def __init__(self, usuario: Usuario):
        self.__usuario = usuario
        self.__ultima_actividad = time.time()
        self.__ultima_consulta = 0.0
        self.__consultas = 0

    @property
    def usuario(self) -> Usuario:
        return self.__usuario

    @property
    def es_admin(self) -> bool:
        return isinstance(self.__usuario, Administrador)

    @property
    def rol(self) -> str:
        return "Administrador" if self.es_admin else "Empleado"

    @property
    def es_superadmin(self) -> bool:
        return self.es_admin and self.__usuario.nivel_permiso == "Superadmin"

    def esta_activa(self) -> bool:
        return time.time() - self.__ultima_actividad < self.TIEMPO_MAXIMO_INACTIVIDAD

    def actividad(self) -> None:
        self.__ultima_actividad = time.time()

    def permitir_consulta(self) -> tuple[bool, str]:
        if not self.esta_activa():
            return (False, "La sesión expiró por inactividad. Inicie sesión de nuevo.")
        if self.__consultas >= self.MAXIMO_CONSULTAS:
            return (False, "Llegó al máximo de consultas de esta sesión. Cierre sesión y vuelva a entrar.")
        espera = self.ESPERA_MINIMA - (time.time() - self.__ultima_consulta)
        if espera > 0:
            return (False, f"Espere {int(espera) + 1} segundo(s) antes de hacer otra consulta.")
        return (True, "")

    def registrar_consulta(self) -> None:
        self.__consultas += 1
        self.__ultima_consulta = time.time()
        self.__ultima_actividad = time.time()
