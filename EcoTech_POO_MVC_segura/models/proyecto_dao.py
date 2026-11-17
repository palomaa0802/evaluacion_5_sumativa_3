import sqlite3
from sqlite3 import Cursor
from config.database import Database
from config.errores import registrar_error
from models.proyecto import Proyecto
from models.empleado import Empleado
from models.empleado_dao import EmpleadoDAO


class ProyectoDAO:
    """
    Data Access Object para la entidad Proyecto.
    Maneja las operaciones CRUD y la asociación muchos a muchos con Empleado.
    """

    @staticmethod
    def crear(proyecto: Proyecto) -> bool:
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO proyecto (nombre_proyecto, descripcion, fecha_inicio) VALUES (?, ?, ?)",
                (proyecto.nombre_proyecto, proyecto.descripcion, proyecto.fecha_inicio.isoformat())
            )
            conn.commit()
            proyecto.id_proyecto = cursor.lastrowid
            return True
        except (sqlite3.Error, ValueError, TypeError) as e:
            registrar_error("Error al crear proyecto en BD", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def obtener_todos() -> list[Proyecto]:
        conn = Database().get_connection()
        proyectos: list[Proyecto] = []
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute("SELECT id_proyecto, nombre_proyecto, descripcion, fecha_inicio FROM proyecto")
            filas = cursor.fetchall()
            for fila in filas:
                proy = Proyecto(
                    nombre_proyecto=fila["nombre_proyecto"],
                    descripcion=fila["descripcion"],
                    fecha_inicio=fila["fecha_inicio"],
                    id_proyecto=fila["id_proyecto"]
                )
                empleados = ProyectoDAO.obtener_empleados_por_proyecto(fila["id_proyecto"])
                for emp in empleados:
                    proy.asignarEmpleado(emp)
                proyectos.append(proy)
        except (sqlite3.Error, ValueError, TypeError) as e:
            registrar_error("Error al obtener proyectos", e)
        finally:
            conn.close()
        return proyectos

    @staticmethod
    def obtener_por_id(id_proyecto: int) -> Proyecto | None:
        conn = Database().get_connection()
        proyecto = None
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                "SELECT id_proyecto, nombre_proyecto, descripcion, fecha_inicio FROM proyecto WHERE id_proyecto = ?",
                (id_proyecto,)
            )
            fila = cursor.fetchone()
            if fila:
                proyecto = Proyecto(
                    nombre_proyecto=fila["nombre_proyecto"],
                    descripcion=fila["descripcion"],
                    fecha_inicio=fila["fecha_inicio"],
                    id_proyecto=fila["id_proyecto"]
                )
                empleados = ProyectoDAO.obtener_empleados_por_proyecto(fila["id_proyecto"])
                for emp in empleados:
                    proyecto.asignarEmpleado(emp)
        except (sqlite3.Error, ValueError, TypeError) as e:
            registrar_error("Error al obtener el proyecto", e)
        finally:
            conn.close()
        return proyecto

    @staticmethod
    def actualizar(proyecto: Proyecto) -> bool:
        if proyecto.id_proyecto is None:
            return False
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                "UPDATE proyecto SET nombre_proyecto = ?, descripcion = ?, fecha_inicio = ? WHERE id_proyecto = ?",
                (
                    proyecto.nombre_proyecto,
                    proyecto.descripcion,
                    proyecto.fecha_inicio.isoformat(),
                    proyecto.id_proyecto
                )
            )
            conn.commit()
            return cursor.rowcount > 0
        except (sqlite3.Error, ValueError, TypeError) as e:
            registrar_error("Error al actualizar proyecto", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_proyecto: int) -> bool:
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute("DELETE FROM proyecto WHERE id_proyecto = ?", (id_proyecto,))
            conn.commit()
            return cursor.rowcount > 0
        except (sqlite3.Error, ValueError, TypeError) as e:
            registrar_error("Error al eliminar proyecto", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def asignar_empleado(id_proyecto: int, id_empleado: int) -> bool:
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO empleado_proyecto (id_empleado, id_proyecto) VALUES (?, ?)",
                (id_empleado, id_proyecto)
            )
            conn.commit()
            return True
        except (sqlite3.Error, ValueError, TypeError) as e:
            registrar_error("Error al asignar empleado al proyecto", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def obtener_empleados_por_proyecto(id_proyecto: int) -> list[Empleado]:
        conn = Database().get_connection()
        empleados: list[Empleado] = []
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                "SELECT id_empleado FROM empleado_proyecto WHERE id_proyecto = ?",
                (id_proyecto,)
            )
            filas = cursor.fetchall()
            for fila in filas:
                emp = EmpleadoDAO.obtener_por_id(fila["id_empleado"])
                if emp:
                    empleados.append(emp)
        except (sqlite3.Error, ValueError, TypeError) as e:
            registrar_error("Error al obtener empleados del proyecto", e)
        finally:
            conn.close()
        return empleados
