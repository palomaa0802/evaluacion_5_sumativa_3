from __future__ import annotations
from datetime import date, datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.empleado import Empleado
    from models.registro_tiempo import RegistroTiempo


class Proyecto:
    """
    Modelo (DTO) para la entidad Proyecto según el diagrama UML.
    Atributos privados (-):
    - __id_proyecto (int | None): Identificador único del proyecto en BD.
    - __nombreProyecto (str): Nombre del proyecto.
    - __descripcion (str): Descripción del proyecto.
    - __fechaInicio (date): Fecha de inicio del proyecto.
    Relaciones:
    - Asociación con Empleado (0..* a 0..*).
    - Asociación con RegistroTiempo (1 a 0..*).
    """

    def __init__(
        self,
        nombre_proyecto: str,
        descripcion: str,
        fecha_inicio: date | str,
        id_proyecto: int | None = None
    ):
        self.__id_proyecto = id_proyecto
        self.setNombreProyecto(nombre_proyecto)
        self.setDescripcion(descripcion)
        self.setFechaInicio(fecha_inicio)
        self.__empleados: list[Empleado] = []
        self.__registros_tiempo: list[RegistroTiempo] = []

    # --- Métodos públicos (+) del Diagrama UML ---

    def asignarEmpleado(self, e: Empleado) -> None:
        """
        Asigna un empleado al proyecto (Asociación 0..* a 0..*).
        """
        if e is None or e.__class__.__name__ != "Empleado":
            raise TypeError("Debe proporcionar una instancia válida de Empleado.")
        if all(emp.getIdUsuario() != e.getIdUsuario() or e.getIdUsuario() is None for emp in self.__empleados):
            self.__empleados.append(e)

    def getNombreProyecto(self) -> str:
        return self.__nombreProyecto

    def setNombreProyecto(self, nombre_proyecto: str) -> None:
        if not isinstance(nombre_proyecto, str) or len(nombre_proyecto.strip()) < 3:
            raise ValueError("El nombre del proyecto debe tener al menos 3 caracteres.")
        self.__nombreProyecto = nombre_proyecto.strip().title()

    def getDescripcion(self) -> str:
        return self.__descripcion

    def setDescripcion(self, descripcion: str) -> None:
        if not isinstance(descripcion, str) or len(descripcion.strip()) < 5:
            raise ValueError("La descripción del proyecto debe tener al menos 5 caracteres.")
        self.__descripcion = descripcion.strip()

    def getFechaInicio(self) -> date:
        return self.__fechaInicio

    def setFechaInicio(self, fecha_inicio: date | str) -> None:
        if isinstance(fecha_inicio, date) and not isinstance(fecha_inicio, datetime):
            self.__fechaInicio = fecha_inicio
        elif isinstance(fecha_inicio, str):
            try:
                self.__fechaInicio = datetime.strptime(fecha_inicio.strip(), "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("La fecha de inicio del proyecto debe tener el formato YYYY-MM-DD.")
        else:
            raise TypeError("La fecha de inicio debe ser un objeto date o string 'YYYY-MM-DD'.")

    # --- Propiedades (@property) estilo Python MVC ---

    @property
    def id_proyecto(self) -> int | None:
        return self.__id_proyecto

    @id_proyecto.setter
    def id_proyecto(self, valor: int | None) -> None:
        self.__id_proyecto = valor

    @property
    def nombre_proyecto(self) -> str:
        return self.getNombreProyecto()

    @nombre_proyecto.setter
    def nombre_proyecto(self, valor: str) -> None:
        self.setNombreProyecto(valor)

    @property
    def descripcion(self) -> str:
        return self.getDescripcion()

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        self.setDescripcion(valor)

    @property
    def fecha_inicio(self) -> date:
        return self.getFechaInicio()

    @fecha_inicio.setter
    def fecha_inicio(self, valor: date | str) -> None:
        self.setFechaInicio(valor)

    @property
    def empleados(self) -> list[Empleado]:
        return list(self.__empleados)

    @property
    def registros_tiempo(self) -> list[RegistroTiempo]:
        return list(self.__registros_tiempo)

    def __str__(self) -> str:
        id_str = self.__id_proyecto if self.__id_proyecto is not None else "Sin asignar"
        return (
            f"Proyecto [ID: {id_str}] | Nombre: {self.__nombreProyecto} | "
            f"Inicio: {self.__fechaInicio.isoformat()} | Descripción: {self.__descripcion}"
        )

    def __repr__(self) -> str:
        return (
            f"Proyecto(id_proyecto={self.__id_proyecto}, nombre_proyecto='{self.__nombreProyecto}', "
            f"fecha_inicio='{self.__fechaInicio.isoformat()}')"
        )
