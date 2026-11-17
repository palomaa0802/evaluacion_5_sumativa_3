import sqlite3
from sqlite3 import Cursor
from config.database import Database
from config.errores import registrar_error
from models.departamento import Departamento
from models.empleado import Empleado


class DepartamentoDAO:
    """
    Data Access Object para la entidad Departamento.
    Maneja las operaciones CRUD en la base de datos.
    """

    @staticmethod
    def _cargar_gerente_basico(cursor: Cursor, id_gerente: int | None) -> Empleado | None:
        if id_gerente is None:
            return None
        cursor.execute(
            """
            SELECT id_usuario, nombre, email, clave_hash, sal, direccion,
                   telefono, fecha_inicio_contrato, salario
            FROM empleado WHERE id_usuario = ?
            """,
            (id_gerente,)
        )
        fila_emp = cursor.fetchone()
        if not fila_emp:
            return None
        return Empleado(
            nombre=fila_emp["nombre"],
            email=fila_emp["email"],
            contrasena=None,
            direccion=fila_emp["direccion"],
            telefono=fila_emp["telefono"],
            fecha_inicio_contrato=fila_emp["fecha_inicio_contrato"],
            salario=fila_emp["salario"],
            departamento=None,
            id_usuario=fila_emp["id_usuario"],
            clave_hash=fila_emp["clave_hash"],
            sal=fila_emp["sal"]
        )

    @staticmethod
    def crear(departamento: Departamento) -> bool:
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            id_gerente = departamento.gerente.getIdUsuario() if departamento.gerente else None
            cursor.execute(
                "INSERT INTO departamento (nombre_depto, id_gerente) VALUES (?, ?)",
                (departamento.nombre_depto, id_gerente)
            )
            conn.commit()
            departamento.id_departamento = cursor.lastrowid
            return True
        except (sqlite3.Error, ValueError, TypeError) as e:
            registrar_error("Error al crear departamento en BD", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def obtener_todos() -> list[Departamento]:
        conn = Database().get_connection()
        departamentos: list[Departamento] = []
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute("SELECT id_departamento, nombre_depto, id_gerente FROM departamento")
            filas = cursor.fetchall()
            for fila in filas:
                gerente = DepartamentoDAO._cargar_gerente_basico(cursor, fila["id_gerente"])
                departamentos.append(
                    Departamento(
                        nombre_depto=fila["nombre_depto"],
                        gerente=gerente,
                        id_departamento=fila["id_departamento"]
                    )
                )
        except (sqlite3.Error, ValueError, TypeError) as e:
            registrar_error("Error al obtener departamentos", e)
        finally:
            conn.close()
        return departamentos

    @staticmethod
    def obtener_por_id(id_departamento: int) -> Departamento | None:
        conn = Database().get_connection()
        departamento = None
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                "SELECT id_departamento, nombre_depto, id_gerente FROM departamento WHERE id_departamento = ?",
                (id_departamento,)
            )
            fila = cursor.fetchone()
            if fila:
                gerente = DepartamentoDAO._cargar_gerente_basico(cursor, fila["id_gerente"])
                departamento = Departamento(
                    nombre_depto=fila["nombre_depto"],
                    gerente=gerente,
                    id_departamento=fila["id_departamento"]
                )
        except (sqlite3.Error, ValueError, TypeError) as e:
            registrar_error("Error al obtener el departamento", e)
        finally:
            conn.close()
        return departamento

    @staticmethod
    def actualizar(departamento: Departamento) -> bool:
        if departamento.id_departamento is None:
            return False
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            id_gerente = departamento.gerente.getIdUsuario() if departamento.gerente else None
            cursor.execute(
                "UPDATE departamento SET nombre_depto = ?, id_gerente = ? WHERE id_departamento = ?",
                (departamento.nombre_depto, id_gerente, departamento.id_departamento)
            )
            conn.commit()
            return cursor.rowcount > 0
        except (sqlite3.Error, ValueError, TypeError) as e:
            registrar_error("Error al actualizar departamento", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_departamento: int) -> bool:
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute("DELETE FROM departamento WHERE id_departamento = ?", (id_departamento,))
            conn.commit()
            return cursor.rowcount > 0
        except (sqlite3.Error, ValueError, TypeError) as e:
            registrar_error("Error al eliminar departamento", e)
            return False
        finally:
            conn.close()
