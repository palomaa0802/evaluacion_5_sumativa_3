import os
from datetime import date, datetime

CARPETA_EXPORTES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "exportes")


class Informe:
    """
    Modelo (DTO) para la entidad Informe según el diagrama UML.
    Atributos privados (-):
    - __id_informe (int | None): Identificador en BD.
    - __tipoInforme (str): Tipo de informe (Empleados, Proyectos, Horas, Departamentos).
    - __fechaGeneracion (date): Fecha de emisión del informe.
    - __contenido (str): Detalle o cuerpo del informe.
    """
    TIPOS_PERMITIDOS: set[str] = {"Empleados", "Proyectos", "Horas", "Departamentos", "General"}
    FORMATOS_PERMITIDOS: set[str] = {"TXT", "CSV", "CONSOLA"}

    def __init__(
        self,
        tipo_informe: str,
        fecha_generacion: date | str | None = None,
        contenido: str = "",
        id_informe: int | None = None,
        id_administrador: int | None = None
    ):
        self.__id_informe = id_informe
        self.setTipoInforme(tipo_informe)
        self.setFechaGeneracion(fecha_generacion if fecha_generacion is not None else date.today())
        self.contenido = contenido
        self.id_administrador = id_administrador

    # --- Métodos públicos (+) del Diagrama UML ---

    def getTipoInforme(self) -> str:
        return self.__tipoInforme

    def setTipoInforme(self, tipo_informe: str) -> None:
        if not isinstance(tipo_informe, str) or len(tipo_informe.strip()) < 3:
            raise ValueError("El tipo de informe debe tener al menos 3 caracteres.")
        tipo_limpio = tipo_informe.strip().title()
        # solo se aceptan los tipos de la lista (el tipo se usa para armar el nombre del archivo exportado)
        if tipo_limpio not in self.TIPOS_PERMITIDOS:
            opciones = ", ".join(sorted(self.TIPOS_PERMITIDOS))
            raise ValueError(f"Tipo de informe '{tipo_informe}' no válido. Opciones: {opciones}.")
        self.__tipoInforme = tipo_limpio

    def getFechaGeneracion(self) -> date:
        return self.__fechaGeneracion

    def setFechaGeneracion(self, fecha_generacion: date | str) -> None:
        if isinstance(fecha_generacion, date) and not isinstance(fecha_generacion, datetime):
            self.__fechaGeneracion = fecha_generacion
        elif isinstance(fecha_generacion, str):
            try:
                self.__fechaGeneracion = datetime.strptime(fecha_generacion.strip(), "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("La fecha de generación debe tener el formato YYYY-MM-DD.")
        else:
            raise TypeError("La fecha de generación debe ser un objeto date o string 'YYYY-MM-DD'.")

    def exportar(self, formato: str = "TXT") -> str:
        """
        Exporta el informe al formato solicitado (TXT, CSV o CONSOLA).
        """
        if not isinstance(formato, str):
            raise TypeError("El formato debe ser una cadena de texto.")
        fmt = formato.strip().upper()
        if fmt not in self.FORMATOS_PERMITIDOS:
            opciones = ", ".join(sorted(self.FORMATOS_PERMITIDOS))
            raise ValueError(f"Formato '{formato}' no válido. Opciones permitidas: {opciones}.")

        encabezado = (
            f"=== INFORME ECOTECH SOLUTIONS ===\n"
            f"ID: {self.__id_informe if self.__id_informe else 'N/A'}\n"
            f"Tipo: {self.__tipoInforme}\n"
            f"Fecha de Generación: {self.__fechaGeneracion.isoformat()}\n"
            f"Detalle:\n{self.__contenido}\n"
        )

        os.makedirs(CARPETA_EXPORTES, exist_ok=True)

        if fmt == "TXT":
            nombre_archivo = os.path.join(CARPETA_EXPORTES, f"informe_{self.__tipoInforme.lower()}_{self.__fechaGeneracion.isoformat()}.txt")
            with open(nombre_archivo, "w", encoding="utf-8") as archivo:
                archivo.write(encabezado)
            return f"Informe exportado exitosamente en la carpeta exportes, archivo '{os.path.basename(nombre_archivo)}'."
        elif fmt == "CSV":
            nombre_archivo = os.path.join(CARPETA_EXPORTES, f"informe_{self.__tipoInforme.lower()}_{self.__fechaGeneracion.isoformat()}.csv")
            contenido_limpio = self.__contenido.replace("\n", " | ").replace(";", ",")
            with open(nombre_archivo, "w", encoding="utf-8") as archivo:
                archivo.write("id_informe;tipo_informe;fecha_generacion;contenido\n")
                archivo.write(f"{self.__id_informe or ''};{self.__tipoInforme};{self.__fechaGeneracion.isoformat()};{contenido_limpio}\n")
            return f"Informe exportado exitosamente en la carpeta exportes, archivo '{os.path.basename(nombre_archivo)}'."
        else:
            return encabezado

    # --- Propiedades (@property) estilo Python MVC ---

    @property
    def id_informe(self) -> int | None:
        return self.__id_informe

    @id_informe.setter
    def id_informe(self, valor: int | None) -> None:
        self.__id_informe = valor

    @property
    def tipo_informe(self) -> str:
        return self.getTipoInforme()

    @tipo_informe.setter
    def tipo_informe(self, valor: str) -> None:
        self.setTipoInforme(valor)

    @property
    def fecha_generacion(self) -> date:
        return self.getFechaGeneracion()

    @fecha_generacion.setter
    def fecha_generacion(self, valor: date | str) -> None:
        self.setFechaGeneracion(valor)

    @property
    def contenido(self) -> str:
        return self.__contenido

    @contenido.setter
    def contenido(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise TypeError("El contenido del informe debe ser texto.")
        self.__contenido = valor.strip()

    def __str__(self) -> str:
        id_str = self.__id_informe if self.__id_informe is not None else "Sin asignar"
        return (
            f"Informe [ID: {id_str}] | Tipo: {self.__tipoInforme} | "
            f"Fecha: {self.__fechaGeneracion.isoformat()} | Resumen: {self.__contenido}"
        )

    def __repr__(self) -> str:
        return (
            f"Informe(id_informe={self.__id_informe}, tipo_informe='{self.__tipoInforme}', "
            f"fecha_generacion='{self.__fechaGeneracion.isoformat()}')"
        )
