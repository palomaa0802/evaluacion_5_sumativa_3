from __future__ import annotations
from datetime import date, datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.empleado import Empleado
    from models.proyecto import Proyecto


class RegistroTiempo:
    """
    Modelo (DTO) para la entidad RegistroTiempo según el diagrama UML.
    Atributos privados (-):
    - __id_registro (int | None): Identificador único del registro en BD.
    - __fecha (date): Fecha del registro de tiempo.
    - __horasTrabajadas (float): Cantidad de horas trabajadas.
    - __descripcionTarea (str): Descripción de las tareas realizadas.
    Relaciones:
    - Composición con Empleado (1 a 0..*).
    - Asociación con Proyecto (1 a 0..*).
    """

    def __init__(
        self,
        fecha: date | str,
        horas_trabajadas: float,
        descripcion_tarea: str,
        empleado: Empleado | None = None,
        proyecto: Proyecto | None = None,
        id_registro: int | None = None
    ):
        self.__id_registro = id_registro
        self.setFecha(fecha)
        self.setHorasTrabajadas(horas_trabajadas)
        self.setDescripcionTarea(descripcion_tarea)
        self.empleado = empleado
        self.proyecto = proyecto

    # --- Métodos públicos (+) del Diagrama UML ---

    def calcularTotalHoras(self, registros: list[RegistroTiempo] | None = None) -> float:
        """
        Calcula el total de horas trabajadas. Si se pasa una lista de registros,
        suma las horas de todos ellos; de lo contrario retorna las horas de este registro.
        """
        if registros is not None:
            return round(sum(r.getHorasTrabajadas() for r in registros), 2)
        return self.__horasTrabajadas

    def getFecha(self) -> date:
        return self.__fecha

    def setFecha(self, fecha: date | str) -> None:
        if isinstance(fecha, date) and not isinstance(fecha, datetime):
            self.__fecha = fecha
        elif isinstance(fecha, str):
            try:
                self.__fecha = datetime.strptime(fecha.strip(), "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("La fecha del registro debe tener el formato YYYY-MM-DD.")
        else:
            raise TypeError("La fecha debe ser un objeto date o string 'YYYY-MM-DD'.")

    def getHorasTrabajadas(self) -> float:
        return self.__horasTrabajadas

    def setHorasTrabajadas(self, horas_trabajadas: float | int) -> None:
        if not isinstance(horas_trabajadas, (int, float)):
            raise TypeError("Las horas trabajadas deben ser un valor numérico.")
        horas_float = float(horas_trabajadas)
        if horas_float <= 0 or horas_float > 24:
            raise ValueError("Las horas trabajadas deben estar entre 0.1 y 24.0 horas por jornada.")
        self.__horasTrabajadas = round(horas_float, 2)

    def getDescripcionTarea(self) -> str:
        return self.__descripcionTarea

    def setDescripcionTarea(self, descripcion_tarea: str) -> None:
        if not isinstance(descripcion_tarea, str) or len(descripcion_tarea.strip()) < 3:
            raise ValueError("La descripción de la tarea debe tener al menos 3 caracteres.")
        self.__descripcionTarea = descripcion_tarea.strip()

    # --- Propiedades (@property) estilo Python MVC ---

    @property
    def id_registro(self) -> int | None:
        return self.__id_registro

    @id_registro.setter
    def id_registro(self, valor: int | None) -> None:
        self.__id_registro = valor

    @property
    def fecha(self) -> date:
        return self.getFecha()

    @fecha.setter
    def fecha(self, valor: date | str) -> None:
        self.setFecha(valor)

    @property
    def horas_trabajadas(self) -> float:
        return self.getHorasTrabajadas()

    @horas_trabajadas.setter
    def horas_trabajadas(self, valor: float | int) -> None:
        self.setHorasTrabajadas(valor)

    @property
    def descripcion_tarea(self) -> str:
        return self.getDescripcionTarea()

    @descripcion_tarea.setter
    def descripcion_tarea(self, valor: str) -> None:
        self.setDescripcionTarea(valor)

    @property
    def empleado(self) -> Empleado | None:
        return self.__empleado

    @empleado.setter
    def empleado(self, emp: Empleado | None) -> None:
        if emp is not None and emp.__class__.__name__ != "Empleado":
            raise TypeError("El empleado debe ser una instancia de Empleado o None.")
        self.__empleado = emp

    @property
    def proyecto(self) -> Proyecto | None:
        return self.__proyecto

    @proyecto.setter
    def proyecto(self, proy: Proyecto | None) -> None:
        if proy is not None and proy.__class__.__name__ != "Proyecto":
            raise TypeError("El proyecto debe ser una instancia de Proyecto o None.")
        self.__proyecto = proy

    def __str__(self) -> str:
        id_str = self.__id_registro if self.__id_registro is not None else "Sin asignar"
        emp_str = self.__empleado.getNombre() if self.__empleado else "No asignado"
        proy_str = self.__proyecto.getNombreProyecto() if self.__proyecto else "General / Sin proyecto"
        return (
            f"RegistroTiempo [ID: {id_str}] | Fecha: {self.__fecha.isoformat()} | "
            f"Horas: {self.__horasTrabajadas}h | Empleado: {emp_str} | "
            f"Proyecto: {proy_str} | Tarea: {self.__descripcionTarea}"
        )

    def __repr__(self) -> str:
        return (
            f"RegistroTiempo(id_registro={self.__id_registro}, fecha='{self.__fecha.isoformat()}', "
            f"horas_trabajadas={self.__horasTrabajadas}, descripcion_tarea='{self.__descripcionTarea}')"
        )
