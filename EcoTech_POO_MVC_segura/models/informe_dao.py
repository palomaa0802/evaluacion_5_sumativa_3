import sqlite3
from sqlite3 import Cursor
from config.database import Database
from config.errores import registrar_error
from models.informe import Informe


class InformeDAO:
    """
    Data Access Object para la entidad Informe.
    Maneja las operaciones CRUD en la base de datos.
    """

    @staticmethod
    def crear(informe: Informe) -> bool:
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO informe (tipo_informe, fecha_generacion, contenido, id_administrador)
                VALUES (?, ?, ?, ?)
                """,
                (
                    informe.tipo_informe,
                    informe.fecha_generacion.isoformat(),
                    informe.contenido,
                    informe.id_administrador
                )
            )
            conn.commit()
            informe.id_informe = cursor.lastrowid
            return True
        except (sqlite3.Error, ValueError, TypeError) as e:
            registrar_error("Error al crear informe en BD", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def obtener_todos() -> list[Informe]:
        conn = Database().get_connection()
        informes: list[Informe] = []
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                "SELECT id_informe, tipo_informe, fecha_generacion, contenido, id_administrador FROM informe"
            )
            filas = cursor.fetchall()
            for fila in filas:
                informes.append(
                    Informe(
                        tipo_informe=fila["tipo_informe"],
                        fecha_generacion=fila["fecha_generacion"],
                        contenido=fila["contenido"],
                        id_informe=fila["id_informe"],
                        id_administrador=fila["id_administrador"]
                    )
                )
        except (sqlite3.Error, ValueError, TypeError) as e:
            registrar_error("Error al obtener informes", e)
        finally:
            conn.close()
        return informes

    @staticmethod
    def obtener_por_id(id_informe: int) -> Informe | None:
        conn = Database().get_connection()
        informe = None
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id_informe, tipo_informe, fecha_generacion, contenido, id_administrador
                FROM informe WHERE id_informe = ?
                """,
                (id_informe,)
            )
            fila = cursor.fetchone()
            if fila:
                informe = Informe(
                    tipo_informe=fila["tipo_informe"],
                    fecha_generacion=fila["fecha_generacion"],
                    contenido=fila["contenido"],
                    id_informe=fila["id_informe"],
                    id_administrador=fila["id_administrador"]
                )
        except (sqlite3.Error, ValueError, TypeError) as e:
            registrar_error("Error al obtener el informe", e)
        finally:
            conn.close()
        return informe

    @staticmethod
    def actualizar(informe: Informe) -> bool:
        if informe.id_informe is None:
            return False
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE informe
                SET tipo_informe = ?, fecha_generacion = ?, contenido = ?, id_administrador = ?
                WHERE id_informe = ?
                """,
                (
                    informe.tipo_informe,
                    informe.fecha_generacion.isoformat(),
                    informe.contenido,
                    informe.id_administrador,
                    informe.id_informe
                )
            )
            conn.commit()
            return cursor.rowcount > 0
        except (sqlite3.Error, ValueError, TypeError) as e:
            registrar_error("Error al actualizar informe", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_informe: int) -> bool:
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute("DELETE FROM informe WHERE id_informe = ?", (id_informe,))
            conn.commit()
            return cursor.rowcount > 0
        except (sqlite3.Error, ValueError, TypeError) as e:
            registrar_error("Error al eliminar informe", e)
            return False
        finally:
            conn.close()
