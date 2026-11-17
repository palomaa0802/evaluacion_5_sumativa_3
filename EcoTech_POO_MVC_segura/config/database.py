import os
import sqlite3
from sqlite3 import Connection, Cursor

from config.errores import registrar_error
from config.seguridad import Seguridad

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Database:
    """
    Clase que gestiona la conexión a la base de datos implementando
    el patrón Singleton para evitar múltiples instancias innecesarias.
    """
    _instance = None
    # ruta fija junto al proyecto, así no depende de desde dónde se ejecute
    _db_path = os.path.join(RAIZ, "ecotech.db")

    # Sentencias para migrar bases antiguas que guardaban la contraseña en texto plano
    _MIGRACIONES = {
        "empleado": (
            "ALTER TABLE empleado ADD COLUMN clave_hash TEXT",
            "ALTER TABLE empleado ADD COLUMN sal TEXT",
            "SELECT id_usuario, contrasena FROM empleado",
            "UPDATE empleado SET clave_hash = ?, sal = ? WHERE id_usuario = ?",
            "ALTER TABLE empleado DROP COLUMN contrasena",
        ),
        "administrador": (
            "ALTER TABLE administrador ADD COLUMN clave_hash TEXT",
            "ALTER TABLE administrador ADD COLUMN sal TEXT",
            "SELECT id_usuario, contrasena FROM administrador",
            "UPDATE administrador SET clave_hash = ?, sal = ? WHERE id_usuario = ?",
            "ALTER TABLE administrador DROP COLUMN contrasena",
        ),
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def get_connection(self) -> Connection:
        """
        Retorna una conexión a la base de datos SQLite con soporte para claves foráneas.
        """
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row  # Permite acceder a las columnas por nombre
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _migrar_claves(self, cursor: Cursor) -> None:
        """
        Si la base es antigua (columna contrasena), pasa las claves a hash con sal
        y elimina la columna en texto plano.
        """
        for tabla, (add_hash, add_sal, leer, actualizar, quitar) in self._MIGRACIONES.items():
            columnas = [
                f["name"] for f in cursor.execute("SELECT name FROM pragma_table_info(?)", (tabla,)).fetchall()
            ]
            if "contrasena" not in columnas:
                continue
            if "clave_hash" not in columnas:
                cursor.execute(add_hash)
                cursor.execute(add_sal)
            for fila in cursor.execute(leer).fetchall():
                sal = Seguridad.generar_sal()
                cursor.execute(actualizar, (Seguridad.cifrar(fila["contrasena"], sal), sal, fila["id_usuario"]))
            cursor.execute(quitar)

    def init_db(self) -> None:
        """
        Inicializa la base de datos creando las tablas necesarias si no existen,
        respetando las relaciones del diagrama de clases UML de EcoTech Solutions.
        """
        conn = self.get_connection()
        try:
            cursor: Cursor = conn.cursor()

            # 1. Tabla Departamento
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS departamento (
                    id_departamento INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre_depto TEXT NOT NULL,
                    id_gerente INTEGER NULL
                )
            """)

            # 2. Tabla Empleado (Hereda atributos de Usuario). La clave se guarda como hash + sal.
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS empleado (
                    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    clave_hash TEXT NOT NULL,
                    sal TEXT NOT NULL,
                    direccion TEXT NOT NULL,
                    telefono TEXT NOT NULL,
                    fecha_inicio_contrato TEXT NOT NULL,
                    salario REAL NOT NULL,
                    id_departamento INTEGER,
                    FOREIGN KEY(id_departamento) REFERENCES departamento(id_departamento) ON DELETE SET NULL
                )
            """)

            # 3. Tabla Administrador (Hereda atributos de Usuario)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS administrador (
                    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    clave_hash TEXT NOT NULL,
                    sal TEXT NOT NULL,
                    nivel_permiso TEXT NOT NULL
                )
            """)

            # 4. Tabla Proyecto
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS proyecto (
                    id_proyecto INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre_proyecto TEXT NOT NULL,
                    descripcion TEXT NOT NULL,
                    fecha_inicio TEXT NOT NULL
                )
            """)

            # 5. Tabla intermedia Empleado - Proyecto (Asociación 0..* a 0..*)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS empleado_proyecto (
                    id_empleado INTEGER NOT NULL,
                    id_proyecto INTEGER NOT NULL,
                    PRIMARY KEY (id_empleado, id_proyecto),
                    FOREIGN KEY(id_empleado) REFERENCES empleado(id_usuario) ON DELETE CASCADE,
                    FOREIGN KEY(id_proyecto) REFERENCES proyecto(id_proyecto) ON DELETE CASCADE
                )
            """)

            # 6. Tabla RegistroTiempo (Composición con Empleado 1 a 0..* y Asociación con Proyecto 1 a 0..*)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS registro_tiempo (
                    id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT NOT NULL,
                    horas_trabajadas REAL NOT NULL,
                    descripcion_tarea TEXT NOT NULL,
                    id_empleado INTEGER NOT NULL,
                    id_proyecto INTEGER,
                    FOREIGN KEY(id_empleado) REFERENCES empleado(id_usuario) ON DELETE CASCADE,
                    FOREIGN KEY(id_proyecto) REFERENCES proyecto(id_proyecto) ON DELETE SET NULL
                )
            """)

            # 7. Tabla Informe (Dependencia desde Administrador)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS informe (
                    id_informe INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo_informe TEXT NOT NULL,
                    fecha_generacion TEXT NOT NULL,
                    contenido TEXT NOT NULL,
                    id_administrador INTEGER,
                    FOREIGN KEY(id_administrador) REFERENCES administrador(id_usuario) ON DELETE SET NULL
                )
            """)

            # 8. Tabla de consultas a servicios externos (clima y tipo de cambio)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS consulta_externa (
                    id_consulta INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_usuario INTEGER NOT NULL,
                    rol TEXT NOT NULL,
                    tipo TEXT NOT NULL,
                    detalle TEXT NOT NULL,
                    resultado TEXT NOT NULL,
                    fecha TEXT NOT NULL
                )
            """)

            self._migrar_claves(cursor)
            conn.commit()
        except sqlite3.Error as e:
            registrar_error("inicializar la base de datos", e)
        finally:
            conn.close()


if __name__ == "__main__":
    db = Database()
    db.init_db()
    print("Base de datos EcoTech inicializada correctamente.")
