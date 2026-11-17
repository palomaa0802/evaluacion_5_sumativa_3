import sqlite3
from sqlite3 import Cursor

from config.database import Database
from config.errores import registrar_error
from models.empleado import Empleado
from models.departamento_dao import DepartamentoDAO


class EmpleadoDAO:
    """
    Data Access Object para la entidad Empleado.
    Maneja todas las operaciones CRUD en la base de datos.
    """

    @staticmethod
    def _construir(fila) -> Empleado:
        departamento = None
        if fila["id_departamento"] is not None:
            departamento = DepartamentoDAO.obtener_por_id(fila["id_departamento"])
        return Empleado(
            nombre=fila["nombre"],
            email=fila["email"],
            contrasena=None,
            direccion=fila["direccion"],
            telefono=fila["telefono"],
            fecha_inicio_contrato=fila["fecha_inicio_contrato"],
            salario=fila["salario"],
            departamento=departamento,
            id_usuario=fila["id_usuario"],
            clave_hash=fila["clave_hash"],
            sal=fila["sal"]
        )

    @staticmethod
    def crear(empleado: Empleado) -> bool:
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            id_depto = empleado.departamento.id_departamento if empleado.departamento else None
            cursor.execute(
                """
                INSERT INTO empleado (
                    nombre, email, clave_hash, sal, direccion,
                    telefono, fecha_inicio_contrato, salario, id_departamento
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    empleado.nombre,
                    empleado.email,
                    empleado.clave_hash,
                    empleado.sal,
                    empleado.direccion,
                    empleado.telefono,
                    empleado.fecha_inicio_contrato.isoformat(),
                    empleado.salario,
                    id_depto
                )
            )
            conn.commit()
            empleado.id_usuario = cursor.lastrowid
            return True
        except (sqlite3.Error, ValueError, TypeError) as e:
            registrar_error("Error al crear empleado en BD", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def obtener_todos() -> list[Empleado]:
        conn = Database().get_connection()
        empleados: list[Empleado] = []
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id_usuario, nombre, email, clave_hash, sal, direccion,
                       telefono, fecha_inicio_contrato, salario, id_departamento
                FROM empleado
                """
            )
            for fila in cursor.fetchall():
                empleados.append(EmpleadoDAO._construir(fila))
        except (sqlite3.Error, ValueError, TypeError) as e:
            registrar_error("Error al obtener empleados", e)
        finally:
            conn.close()
        return empleados

    @staticmethod
    def obtener_por_id(id_usuario: int) -> Empleado | None:
        conn = Database().get_connection()
        empleado = None
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id_usuario, nombre, email, clave_hash, sal, direccion,
                       telefono, fecha_inicio_contrato, salario, id_departamento
                FROM empleado WHERE id_usuario = ?
                """,
                (id_usuario,)
            )
            fila = cursor.fetchone()
            if fila:
                empleado = EmpleadoDAO._construir(fila)
        except (sqlite3.Error, ValueError, TypeError) as e:
            registrar_error("Error al obtener el empleado", e)
        finally:
            conn.close()
        return empleado

    @staticmethod
    def obtener_por_email(email: str) -> Empleado | None:
        conn = Database().get_connection()
        empleado = None
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id_usuario, nombre, email, clave_hash, sal, direccion,
                       telefono, fecha_inicio_contrato, salario, id_departamento
                FROM empleado WHERE email = ?
                """,
                (email.strip().lower(),)
            )
            fila = cursor.fetchone()
            if fila:
                empleado = EmpleadoDAO._construir(fila)
        except (sqlite3.Error, ValueError, TypeError) as e:
            registrar_error("Error al obtener el empleado por email", e)
        finally:
            conn.close()
        return empleado

    @staticmethod
    def actualizar(empleado: Empleado) -> bool:
        if empleado.id_usuario is None:
            return False
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            id_depto = empleado.departamento.id_departamento if empleado.departamento else None
            cursor.execute(
                """
                UPDATE empleado
                SET nombre = ?, email = ?, clave_hash = ?, sal = ?, direccion = ?,
                    telefono = ?, fecha_inicio_contrato = ?, salario = ?, id_departamento = ?
                WHERE id_usuario = ?
                """,
                (
                    empleado.nombre,
                    empleado.email,
                    empleado.clave_hash,
                    empleado.sal,
                    empleado.direccion,
                    empleado.telefono,
                    empleado.fecha_inicio_contrato.isoformat(),
                    empleado.salario,
                    id_depto,
                    empleado.id_usuario
                )
            )
            conn.commit()
            return cursor.rowcount > 0
        except (sqlite3.Error, ValueError, TypeError) as e:
            registrar_error("Error al actualizar empleado", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_usuario: int) -> bool:
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute("UPDATE departamento SET id_gerente = NULL WHERE id_gerente = ?", (id_usuario,))
            cursor.execute("DELETE FROM empleado WHERE id_usuario = ?", (id_usuario,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            registrar_error("Error al eliminar empleado", e)
            return False
        finally:
            conn.close()
