from abc import ABC, abstractmethod

from config.seguridad import Seguridad


class Usuario(ABC):
    """
    Clase base abstracta Usuario según el diagrama UML de EcoTech Solutions.
    Atributos privados (-):
    - __id_usuario (int | None): Identificador único del usuario.
    - __nombre (str): Nombre completo del usuario.
    - __email (str): Correo electrónico corporativo.
    - __clave_hash (str): Hash de la contraseña (la contraseña nunca se guarda tal cual).
    - __sal (str): Sal aleatoria propia de este usuario.
    """

    def __init__(
        self,
        nombre: str,
        email: str,
        contrasena: str | None = None,
        id_usuario: int | None = None,
        clave_hash: str | None = None,
        sal: str | None = None
    ):
        self.setIdUsuario(id_usuario)
        self.setNombre(nombre)
        self.setEmail(email)
        self.__clave_hash = None
        self.__sal = None
        if contrasena is not None:
            # usuario nuevo o con clave nueva: se valida y se guarda solo el hash
            self.setContrasena(contrasena)
        elif clave_hash and sal:
            # usuario que viene de la base de datos
            self.__clave_hash = clave_hash
            self.__sal = sal
        else:
            raise ValueError("Debe indicar una contraseña.")

    @abstractmethod
    def iniciarSesion(self, email: str = "", contrasena: str = "") -> bool:
        """
        Verifica las credenciales de inicio de sesión del usuario.
        """
        if not email or not contrasena:
            return False
        return self.__email == email.strip().lower() and self.verificarContrasena(contrasena)

    def verificarContrasena(self, contrasena: str) -> bool:
        """
        Compara la contraseña ingresada con el hash guardado.
        """
        if not isinstance(contrasena, str) or not self.__clave_hash or not self.__sal:
            return False
        return Seguridad.verificar(contrasena, self.__sal, self.__clave_hash)

    # --- Métodos Getter y Setter del Diagrama UML ---

    def getIdUsuario(self) -> int | None:
        return self.__id_usuario

    def setIdUsuario(self, id_usuario: int | None) -> None:
        if id_usuario is not None and (not isinstance(id_usuario, int) or id_usuario <= 0):
            raise ValueError("El ID de usuario debe ser un entero positivo o None.")
        self.__id_usuario = id_usuario

    def getNombre(self) -> str:
        return self.__nombre

    def setNombre(self, nombre: str) -> None:
        if not isinstance(nombre, str) or len(nombre.strip()) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres.")
        self.__nombre = nombre.strip().title()

    def getEmail(self) -> str:
        return self.__email

    def setEmail(self, email: str) -> None:
        if not isinstance(email, str) or "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError("El correo electrónico no tiene un formato válido (ej: usuario@ecotech.cl).")
        self.__email = email.strip().lower()

    def setContrasena(self, contrasena: str) -> None:
        """
        Valida que la contraseña sea fuerte y guarda solo su hash con una sal nueva.
        """
        Seguridad.validar_fortaleza(contrasena)
        sal = Seguridad.generar_sal()
        self.__sal = sal
        self.__clave_hash = Seguridad.cifrar(contrasena, sal)

    def getClaveHash(self) -> str | None:
        return self.__clave_hash

    def getSal(self) -> str | None:
        return self.__sal

    # --- Propiedades (@property) estilo Python MVC ---

    @property
    def id_usuario(self) -> int | None:
        return self.getIdUsuario()

    @id_usuario.setter
    def id_usuario(self, valor: int | None) -> None:
        self.setIdUsuario(valor)

    @property
    def nombre(self) -> str:
        return self.getNombre()

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.setNombre(valor)

    @property
    def email(self) -> str:
        return self.getEmail()

    @email.setter
    def email(self, valor: str) -> None:
        self.setEmail(valor)

    @property
    def clave_hash(self) -> str | None:
        return self.getClaveHash()

    @property
    def sal(self) -> str | None:
        return self.getSal()
