import sqlite3
from sqlite3 import Cursor

from config.database import Database
from config.errores import registrar_error
from models.administrador import Administrador


class AdministradorDAO:
    """
    Data Access Object para la entidad Administrador.
    Maneja las operaciones CRUD en la base de datos.
    """

    @staticmethod
    def _construir(fila) -> Administrador:
        return Administrador(
            nombre=fila["nombre"],
            email=fila["email"],
            contrasena=None,
            nivel_permiso=fila["nivel_permiso"],
            id_usuario=fila["id_usuario"],
            clave_hash=fila["clave_hash"],
            sal=fila["sal"]
        )

    @staticmethod
    def crear(administrador: Administrador) -> bool:
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO administrador (nombre, email, clave_hash, sal, nivel_permiso)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    administrador.nombre,
                    administrador.email,
                    administrador.clave_hash,
                    administrador.sal,
                    administrador.nivel_permiso
                )
            )
            conn.commit()
            administrador.id_usuario = cursor.lastrowid
            return True
        except (sqlite3.Error, ValueError, TypeError) as e:
            registrar_error("Error al crear administrador en BD", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def obtener_todos() -> list[Administrador]:
        conn = Database().get_connection()
        administradores: list[Administrador] = []
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute("SELECT id_usuario, nombre, email, clave_hash, sal, nivel_permiso FROM administrador")
            for fila in cursor.fetchall():
                administradores.append(AdministradorDAO._construir(fila))
        except (sqlite3.Error, ValueError, TypeError) as e:
            registrar_error("Error al obtener administradores", e)
        finally:
            conn.close()
        return administradores

    @staticmethod
    def obtener_por_id(id_usuario: int) -> Administrador | None:
        conn = Database().get_connection()
        administrador = None
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                "SELECT id_usuario, nombre, email, clave_hash, sal, nivel_permiso FROM administrador WHERE id_usuario = ?",
                (id_usuario,)
            )
            fila = cursor.fetchone()
            if fila:
                administrador = AdministradorDAO._construir(fila)
        except (sqlite3.Error, ValueError, TypeError) as e:
            registrar_error("Error al obtener el administrador", e)
        finally:
            conn.close()
        return administrador

    @staticmethod
    def obtener_por_email(email: str) -> Administrador | None:
        conn = Database().get_connection()
        administrador = None
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                "SELECT id_usuario, nombre, email, clave_hash, sal, nivel_permiso FROM administrador WHERE email = ?",
                (email.strip().lower(),)
            )
            fila = cursor.fetchone()
            if fila:
                administrador = AdministradorDAO._construir(fila)
        except (sqlite3.Error, ValueError, TypeError) as e:
            registrar_error("Error al obtener el administrador por email", e)
        finally:
            conn.close()
        return administrador

    @staticmethod
    def actualizar(administrador: Administrador) -> bool:
        if administrador.id_usuario is None:
            return False
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE administrador
                SET nombre = ?, email = ?, clave_hash = ?, sal = ?, nivel_permiso = ?
                WHERE id_usuario = ?
                """,
                (
                    administrador.nombre,
                    administrador.email,
                    administrador.clave_hash,
                    administrador.sal,
                    administrador.nivel_permiso,
                    administrador.id_usuario
                )
            )
            conn.commit()
            return cursor.rowcount > 0
        except (sqlite3.Error, ValueError, TypeError) as e:
            registrar_error("Error al actualizar administrador", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_usuario: int) -> bool:
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute("DELETE FROM administrador WHERE id_usuario = ?", (id_usuario,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            registrar_error("Error al eliminar administrador", e)
            return False
        finally:
            conn.close()
