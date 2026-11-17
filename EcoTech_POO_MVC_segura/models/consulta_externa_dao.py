import sqlite3
from datetime import datetime
from sqlite3 import Cursor

from config.database import Database
from config.errores import registrar_error


class ConsultaExternaDAO:
    """
    Guarda en la base de datos las consultas hechas a los servicios externos
    (clima y tipo de cambio), para poder revisarlas después.
    """

    @staticmethod
    def registrar(id_usuario: int, rol: str, tipo: str, detalle: str, resultado: str) -> bool:
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO consulta_externa (id_usuario, rol, tipo, detalle, resultado, fecha)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (id_usuario, rol, tipo, detalle, resultado, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            registrar_error("Error al guardar la consulta externa", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def obtener_ultimas(cantidad: int = 10) -> list[sqlite3.Row]:
        conn = Database().get_connection()
        filas: list[sqlite3.Row] = []
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                """
                SELECT fecha, id_usuario, rol, tipo, detalle, resultado
                FROM consulta_externa ORDER BY id_consulta DESC LIMIT ?
                """,
                (cantidad,)
            )
            filas = cursor.fetchall()
        except sqlite3.Error as e:
            registrar_error("Error al obtener las consultas externas", e)
        finally:
            conn.close()
        return filas
