import sys

sys.dont_write_bytecode = True

from config.database import Database
from config.errores import configurar_log
from controllers.main_controller import MainController


def main() -> None:
    # 0. Los errores técnicos se guardan en errores.log
    configurar_log()

    # 1. Inicializar la base de datos (crear tablas si no existen)
    print("Inicializando sistema EcoTech Solutions...")
    db = Database()
    db.init_db()

    # 2. Iniciar el controlador principal que maneja el flujo de la aplicación
    app = MainController()
    app.ejecutar()


if __name__ == "__main__":
    main()
