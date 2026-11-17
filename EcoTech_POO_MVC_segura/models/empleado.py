from __future__ import annotations
from datetime import date, datetime
from typing import TYPE_CHECKING
from models.usuario import Usuario

if TYPE_CHECKING:
    from models.departamento import Departamento
    from models.proyecto import Proyecto
    from models.registro_tiempo import RegistroTiempo


class Empleado(Usuario):
    """
    Modelo (DTO) para la entidad Empleado que hereda de Usuario.
    Atributos privados (-):
    - __direccion (str): Dirección residencial del empleado.
    - __telefono (str): Teléfono de contacto.
    - __fechaInicioContrato (date): Fecha de inicio en EcoTech Solutions.
    - __salario (float): Salario mensual del empleado.
    Relaciones:
    - Herencia de Usuario.
    - Pertenece a un Departamento (Agregación).
    - Composición con RegistroTiempo (1 a 0..*).
    - Asociación con Proyecto (0..* a 0..*).
    """

    def __init__(
        self,
        nombre: str,
        email: str,
        contrasena: str | None,
        direccion: str,
        telefono: str,
        fecha_inicio_contrato: date | str,
        salario: float,
        departamento: Departamento | None = None,
        id_usuario: int | None = None,
        clave_hash: str | None = None,
        sal: str | None = None
    ):
        super().__init__(nombre, email, contrasena, id_usuario, clave_hash, sal)
        self.setDireccion(direccion)
        self.setTelefono(telefono)
        self.setFechaInicioContrato(fecha_inicio_contrato)
        self.setSalario(salario)
        self.departamento = departamento
        self.__registros_tiempo: list[RegistroTiempo] = []
        self.__proyectos: list[Proyecto] = []

    # --- Métodos públicos (+) del Diagrama UML ---

    def iniciarSesion(self, email: str = "", contrasena: str = "") -> bool:
        """
        Implementación polimórfica de inicio de sesión para Empleado.
        """
        return super().iniciarSesion(email, contrasena)

    def registrarHoras(self, r: RegistroTiempo) -> None:
        """
        Registra un objeto RegistroTiempo asociado por composición al empleado.
        """
        if r is None or r.__class__.__name__ != "RegistroTiempo":
            raise TypeError("Debe proporcionar una instancia válida de RegistroTiempo.")
        if r not in self.__registros_tiempo:
            self.__registros_tiempo.append(r)

    def getSalario(self) -> float:
        return self.__salario

    def setSalario(self, salario: float | int) -> None:
        if not isinstance(salario, (int, float)):
            raise TypeError("El salario debe ser un valor numérico.")
        if float(salario) < 0:
            raise ValueError("El salario no puede ser negativo.")
        self.__salario = float(salario)

    def getTelefono(self) -> str:
        return self.__telefono

    def setTelefono(self, telefono: str) -> None:
        if not isinstance(telefono, str) or len(telefono.strip()) < 6:
            raise ValueError("El teléfono debe contener al menos 6 caracteres.")
        self.__telefono = telefono.strip()

    def getDireccion(self) -> str:
        return self.__direccion

    def setDireccion(self, direccion: str) -> None:
        if not isinstance(direccion, str) or len(direccion.strip()) < 3:
            raise ValueError("La dirección debe tener al menos 3 caracteres.")
        self.__direccion = direccion.strip()

    def getFechaInicioContrato(self) -> date:
        return self.__fechaInicioContrato

    def setFechaInicioContrato(self, fecha: date | str) -> None:
        if isinstance(fecha, date) and not isinstance(fecha, datetime):
            self.__fechaInicioContrato = fecha
        elif isinstance(fecha, str):
            try:
                self.__fechaInicioContrato = datetime.strptime(fecha.strip(), "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("La fecha de inicio de contrato debe tener el formato YYYY-MM-DD.")
        else:
            raise TypeError("La fecha de inicio de contrato debe ser un objeto date o string 'YYYY-MM-DD'.")

    # --- Propiedades (@property) estilo Python MVC ---

    @property
    def direccion(self) -> str:
        return self.getDireccion()

    @direccion.setter
    def direccion(self, valor: str) -> None:
        self.setDireccion(valor)

    @property
    def telefono(self) -> str:
        return self.getTelefono()

    @telefono.setter
    def telefono(self, valor: str) -> None:
        self.setTelefono(valor)

    @property
    def fecha_inicio_contrato(self) -> date:
        return self.getFechaInicioContrato()

    @fecha_inicio_contrato.setter
    def fecha_inicio_contrato(self, valor: date | str) -> None:
        self.setFechaInicioContrato(valor)

    @property
    def salario(self) -> float:
        return self.getSalario()

    @salario.setter
    def salario(self, valor: float | int) -> None:
        self.setSalario(valor)

    @property
    def departamento(self) -> Departamento | None:
        return self.__departamento

    @departamento.setter
    def departamento(self, depto: Departamento | None) -> None:
        if depto is not None and depto.__class__.__name__ != "Departamento":
            raise TypeError("El departamento debe ser una instancia de la clase Departamento o None.")
        self.__departamento = depto

    @property
    def registros_tiempo(self) -> list[RegistroTiempo]:
        return list(self.__registros_tiempo)

    @property
    def proyectos(self) -> list[Proyecto]:
        return list(self.__proyectos)

    def __str__(self) -> str:
        id_str = self.getIdUsuario() if self.getIdUsuario() is not None else "Sin asignar"
        depto_str = self.__departamento.getNombreDepto() if self.__departamento else "Sin departamento"
        return (
            f"Empleado [ID: {id_str}] | Nombre: {self.getNombre()} | Email: {self.getEmail()} | "
            f"Tel: {self.__telefono} | Dirección: {self.__direccion} | "
            f"Inicio: {self.__fechaInicioContrato.isoformat()} | Salario: ${self.__salario:,.2f} | "
            f"Departamento: {depto_str}"
        )

    def __repr__(self) -> str:
        return (
            f"Empleado(id_usuario={self.getIdUsuario()}, nombre='{self.getNombre()}', "
            f"email='{self.getEmail()}', salario={self.__salario})"
        )
