import sqlite3
from sqlite3 import Cursor
from config.database import Database
from config.errores import registrar_error
from models.registro_tiempo import RegistroTiempo
from models.empleado_dao import EmpleadoDAO
from models.proyecto_dao import ProyectoDAO


class RegistroTiempoDAO:
    """
    Data Access Object para la entidad RegistroTiempo.
    Maneja las operaciones CRUD en la base de datos.
    """

    @staticmethod
    def crear(registro: RegistroTiempo) -> bool:
        if registro.empleado is None or registro.empleado.id_usuario is None:
            print("Error: El registro de tiempo debe pertenecer obligatoriamente a un empleado válido (Composición).")
            return False
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            id_empleado = registro.empleado.id_usuario
            id_proyecto = registro.proyecto.id_proyecto if registro.proyecto else None
            cursor.execute(
                """
                INSERT INTO registro_tiempo (fecha, horas_trabajadas, descripcion_tarea, id_empleado, id_proyecto)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    registro.fecha.isoformat(),
                    registro.horas_trabajadas,
                    registro.descripcion_tarea,
                    id_empleado,
                    id_proyecto
                )
            )
            conn.commit()
            registro.id_registro = cursor.lastrowid
            return True
        except (sqlite3.Error, ValueError, TypeError) as e:
            registrar_error("Error al crear registro de tiempo en BD", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def obtener_todos() -> list[RegistroTiempo]:
        conn = Database().get_connection()
        registros: list[RegistroTiempo] = []
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id_registro, fecha, horas_trabajadas, descripcion_tarea, id_empleado, id_proyecto
                FROM registro_tiempo
                """
            )
            filas = cursor.fetchall()
            for fila in filas:
                empleado = EmpleadoDAO.obtener_por_id(fila["id_empleado"])
                proyecto = ProyectoDAO.obtener_por_id(fila["id_proyecto"]) if fila["id_proyecto"] is not None else None
                reg = RegistroTiempo(
                    fecha=fila["fecha"],
                    horas_trabajadas=fila["horas_trabajadas"],
                    descripcion_tarea=fila["descripcion_tarea"],
                    empleado=empleado,
                    proyecto=proyecto,
                    id_registro=fila["id_registro"]
                )
                if empleado:
                    empleado.registrarHoras(reg)
                registros.append(reg)
        except (sqlite3.Error, ValueError, TypeError) as e:
            registrar_error("Error al obtener registros de tiempo", e)
        finally:
            conn.close()
        return registros

    @staticmethod
    def obtener_por_id(id_registro: int) -> RegistroTiempo | None:
        conn = Database().get_connection()
        registro = None
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id_registro, fecha, horas_trabajadas, descripcion_tarea, id_empleado, id_proyecto
                FROM registro_tiempo WHERE id_registro = ?
                """,
                (id_registro,)
            )
            fila = cursor.fetchone()
            if fila:
                empleado = EmpleadoDAO.obtener_por_id(fila["id_empleado"])
                proyecto = ProyectoDAO.obtener_por_id(fila["id_proyecto"]) if fila["id_proyecto"] is not None else None
                registro = RegistroTiempo(
                    fecha=fila["fecha"],
                    horas_trabajadas=fila["horas_trabajadas"],
                    descripcion_tarea=fila["descripcion_tarea"],
                    empleado=empleado,
                    proyecto=proyecto,
                    id_registro=fila["id_registro"]
                )
        except (sqlite3.Error, ValueError, TypeError) as e:
            registrar_error("Error al obtener el registro de tiempo", e)
        finally:
            conn.close()
        return registro

    @staticmethod
    def actualizar(registro: RegistroTiempo) -> bool:
        if registro.id_registro is None or registro.empleado is None:
            return False
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            id_empleado = registro.empleado.id_usuario
            id_proyecto = registro.proyecto.id_proyecto if registro.proyecto else None
            cursor.execute(
                """
                UPDATE registro_tiempo
                SET fecha = ?, horas_trabajadas = ?, descripcion_tarea = ?, id_empleado = ?, id_proyecto = ?
                WHERE id_registro = ?
                """,
                (
                    registro.fecha.isoformat(),
                    registro.horas_trabajadas,
                    registro.descripcion_tarea,
                    id_empleado,
                    id_proyecto,
                    registro.id_registro
                )
            )
            conn.commit()
            return cursor.rowcount > 0
        except (sqlite3.Error, ValueError, TypeError) as e:
            registrar_error("Error al actualizar registro de tiempo", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_registro: int) -> bool:
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute("DELETE FROM registro_tiempo WHERE id_registro = ?", (id_registro,))
            conn.commit()
            return cursor.rowcount > 0
        except (sqlite3.Error, ValueError, TypeError) as e:
            registrar_error("Error al eliminar registro de tiempo", e)
            return False
        finally:
            conn.close()
