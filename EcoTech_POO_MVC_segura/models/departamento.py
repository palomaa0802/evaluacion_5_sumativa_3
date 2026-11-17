from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.empleado import Empleado


class Departamento:
    """
    Modelo (DTO) para la entidad Departamento según el diagrama UML.
    Atributos privados (-):
    - __id_departamento (int | None): Identificador único del departamento en BD.
    - __nombreDepto (str): Nombre del departamento.
    - __gerente (Empleado | None): Empleado que dirige el departamento.
    Relación:
    - Agregación de Departamento a Empleado (1 a 0..*).
    """

    def __init__(
        self,
        nombre_depto: str,
        gerente: Empleado | None = None,
        id_departamento: int | None = None
    ):
        self.__id_departamento = id_departamento
        self.setNombreDepto(nombre_depto)
        self.setGerente(gerente)
        self.__empleados: list[Empleado] = []

    # --- Métodos públicos (+) del Diagrama UML ---

    def agregarEmpleado(self, e: Empleado) -> None:
        """
        Agrega un empleado a la lista del departamento (Agregación).
        """
        if e is None or e.__class__.__name__ != "Empleado":
            raise TypeError("Se debe proporcionar una instancia válida de Empleado.")
        if all(emp.getIdUsuario() != e.getIdUsuario() or e.getIdUsuario() is None for emp in self.__empleados):
            self.__empleados.append(e)
            e.departamento = self

    def eliminarEmpleado(self, e: Empleado) -> None:
        """
        Elimina un empleado del departamento sin destruir la instancia de Empleado (Agregación).
        """
        if e is None or e.__class__.__name__ != "Empleado":
            raise TypeError("Se debe proporcionar una instancia válida de Empleado.")
        self.__empleados = [
            emp for emp in self.__empleados
            if emp != e and (emp.getIdUsuario() != e.getIdUsuario() or e.getIdUsuario() is None)
        ]
        if e.departamento == self:
            e.departamento = None

    def getNombreDepto(self) -> str:
        return self.__nombreDepto

    def setNombreDepto(self, nombre_depto: str) -> None:
        if not isinstance(nombre_depto, str) or len(nombre_depto.strip()) < 3:
            raise ValueError("El nombre del departamento debe tener al menos 3 caracteres.")
        self.__nombreDepto = nombre_depto.strip().title()

    def getGerente(self) -> Empleado | None:
        return self.__gerente

    def setGerente(self, gerente: Empleado | None) -> None:
        if gerente is not None and gerente.__class__.__name__ != "Empleado":
            raise TypeError("El gerente debe ser una instancia de Empleado o None.")
        self.__gerente = gerente

    # --- Propiedades (@property) estilo Python MVC ---

    @property
    def id_departamento(self) -> int | None:
        return self.__id_departamento

    @id_departamento.setter
    def id_departamento(self, valor: int | None) -> None:
        self.__id_departamento = valor

    @property
    def nombre_depto(self) -> str:
        return self.getNombreDepto()

    @nombre_depto.setter
    def nombre_depto(self, valor: str) -> None:
        self.setNombreDepto(valor)

    @property
    def nombre(self) -> str:
        return self.getNombreDepto()

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.setNombreDepto(valor)

    @property
    def gerente(self) -> Empleado | None:
        return self.getGerente()

    @gerente.setter
    def gerente(self, valor: Empleado | None) -> None:
        self.setGerente(valor)

    @property
    def empleados(self) -> list[Empleado]:
        return list(self.__empleados)

    def __str__(self) -> str:
        id_str = self.__id_departamento if self.__id_departamento is not None else "Sin asignar"
        gerente_str = self.__gerente.getNombre() if self.__gerente else "Sin asignar"
        return f"Departamento [ID: {id_str}] | Nombre: {self.__nombreDepto} | Gerente: {gerente_str}"

    def __repr__(self) -> str:
        gerente_id = self.__gerente.getIdUsuario() if self.__gerente else None
        return (
            f"Departamento(id_departamento={self.__id_departamento}, "
            f"nombre_depto='{self.__nombreDepto}', id_gerente={gerente_id})"
        )
