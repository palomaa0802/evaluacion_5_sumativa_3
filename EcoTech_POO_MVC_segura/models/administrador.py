from datetime import date
from models.usuario import Usuario
from models.informe import Informe


class Administrador(Usuario):
    """
    Modelo (DTO) para la entidad Administrador que hereda de Usuario.
    Atributos privados (-):
    - __nivelPermiso (str): Nivel de acceso (Alto, Medio, SuperAdmin).
    Relaciones:
    - Herencia de Usuario.
    - Dependencia hacia Informe (generarInforme(): Informe).
    """
    NIVELES_PERMITIDOS: set[str] = {"Basico", "Medio", "Alto", "Superadmin"}

    def __init__(
        self,
        nombre: str,
        email: str,
        contrasena: str | None,
        nivel_permiso: str = "Alto",
        id_usuario: int | None = None,
        clave_hash: str | None = None,
        sal: str | None = None
    ):
        super().__init__(nombre, email, contrasena, id_usuario, clave_hash, sal)
        self.setNivelPermiso(nivel_permiso)

    # --- Métodos públicos (+) del Diagrama UML ---

    def iniciarSesion(self, email: str = "", contrasena: str = "") -> bool:
        """
        Implementación polimórfica de inicio de sesión para Administrador.
        """
        return super().iniciarSesion(email, contrasena)

    def gestionarUsuarios(self) -> str:
        """
        Retorna el estado de habilitación para la gestión de usuarios según su nivel de permiso.
        """
        return (
            f"Administrador '{self.getNombre()}' (Nivel: {self.__nivelPermiso}) "
            f"autorizado para gestionar usuarios del sistema."
        )

    def generarInforme(self, tipo_informe: str = "General", contenido: str = "") -> Informe:
        """
        Relación de dependencia: instancia y retorna un objeto Informe.
        """
        resumen = contenido if contenido.strip() else f"Informe de {tipo_informe} generado por {self.getNombre()}."
        return Informe(
            tipo_informe=tipo_informe,
            fecha_generacion=date.today(),
            contenido=resumen,
            id_administrador=self.getIdUsuario()
        )

    def getNivelPermiso(self) -> str:
        return self.__nivelPermiso

    def setNivelPermiso(self, nivel_permiso: str) -> None:
        if not isinstance(nivel_permiso, str) or not nivel_permiso.strip():
            raise ValueError("El nivel de permiso no puede estar vacío.")
        nivel_limpio = nivel_permiso.strip().capitalize()
        if nivel_limpio not in self.NIVELES_PERMITIDOS:
            opciones = ", ".join(sorted(self.NIVELES_PERMITIDOS))
            raise ValueError(f"Nivel de permiso '{nivel_permiso}' no válido. Opciones: {opciones}.")
        self.__nivelPermiso = nivel_limpio

    # --- Propiedades (@property) estilo Python MVC ---

    @property
    def nivel_permiso(self) -> str:
        return self.getNivelPermiso()

    @nivel_permiso.setter
    def nivel_permiso(self, valor: str) -> None:
        self.setNivelPermiso(valor)

    def __str__(self) -> str:
        id_str = self.getIdUsuario() if self.getIdUsuario() is not None else "Sin asignar"
        return (
            f"Administrador [ID: {id_str}] | Nombre: {self.getNombre()} | "
            f"Email: {self.getEmail()} | Nivel Permiso: {self.__nivelPermiso}"
        )

    def __repr__(self) -> str:
        return (
            f"Administrador(id_usuario={self.getIdUsuario()}, nombre='{self.getNombre()}', "
            f"email='{self.getEmail()}', nivel_permiso='{self.__nivelPermiso}')"
        )
