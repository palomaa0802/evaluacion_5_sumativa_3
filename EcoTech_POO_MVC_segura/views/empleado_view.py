from getpass import getpass
from views.utils import leer_numero, leer_flotante, leer_fecha, confirmar
from models.empleado import Empleado
from models.departamento import Departamento


class EmpleadoView:
    @staticmethod
    def mostrar_menu() -> int:
        print("\n" + "-" * 35)
        print("      GESTIÓN DE EMPLEADOS")
        print("-" * 35)
        print("1.- Agregar empleado")
        print("2.- Editar empleado")
        print("3.- Eliminar empleado")
        print("4.- Imprimir un empleado")
        print("5.- Imprimir todos los empleados")
        print("6.- Probar inicio de sesión (iniciarSesion)")
        print("0.- Volver al menú principal")
        print("-" * 35)
        return leer_numero("Seleccione una opción: ")

    @staticmethod
    def formulario_nuevo_empleado(departamentos: list[Departamento]) -> dict:
        print("\n--- Agregar Nuevo Empleado ---")
        nombre = input("Ingrese el nombre completo del empleado: ")
        email = input("Ingrese el correo electrónico (ej: ana@ecotech.cl): ")
        contrasena = getpass("Ingrese la contraseña (mín. 8, con mayúscula, minúscula y número): ")
        direccion = input("Ingrese la dirección del empleado: ")
        telefono = input("Ingrese el teléfono del empleado: ")
        fecha_inicio_contrato = leer_fecha("Ingrese la fecha de inicio de contrato (YYYY-MM-DD): ")
        salario = leer_flotante("Ingrese el salario mensual: ")

        print("\nDepartamentos disponibles:")
        if departamentos:
            for d in departamentos:
                print(f"{d.id_departamento}.- {d.nombre_depto}")
        else:
            print("No hay departamentos registrados.")

        opcion_depto = leer_numero("Seleccione el ID del departamento (o 0 para ninguno): ")
        id_departamento = opcion_depto if opcion_depto > 0 else None

        return {
            "nombre": nombre,
            "email": email,
            "contrasena": contrasena,
            "direccion": direccion,
            "telefono": telefono,
            "fecha_inicio_contrato": fecha_inicio_contrato,
            "salario": salario,
            "id_departamento": id_departamento
        }

    @staticmethod
    def solicitar_id() -> int:
        return leer_numero("Ingrese el ID del empleado: ")

    @staticmethod
    def solicitar_credenciales() -> dict:
        print("\n--- Inicio de Sesión de Empleado ---")
        email = input("Ingrese el email del empleado: ").strip()
        contrasena = getpass("Ingrese la contraseña: ")
        return {"email": email, "contrasena": contrasena}

    @staticmethod
    def mostrar_empleado(empleado: Empleado) -> None:
        print("\n--- Datos del Empleado ---")
        print(empleado)
        print("-" * 35)

    @staticmethod
    def mostrar_lista_empleados(empleados: list[Empleado]) -> None:
        print("\n--- Lista de Empleados ---")
        if not empleados:
            print("No hay empleados registrados.")
        else:
            for e in empleados:
                print(e)
        print("-" * 35)

    @staticmethod
    def formulario_editar_empleado(empleado: Empleado, departamentos: list[Departamento]) -> dict:
        print(f"\n--- Editando Empleado [ID: {empleado.id_usuario}] {empleado.nombre} ---")
        print("Deje en blanco si no desea modificar el campo.")

        nuevo_nombre = input(f"Nombre actual ({empleado.nombre}): ")
        if not nuevo_nombre.strip():
            nuevo_nombre = empleado.nombre

        nuevo_email = input(f"Email actual ({empleado.email}): ")
        if not nuevo_email.strip():
            nuevo_email = empleado.email

        nueva_contrasena = getpass("Nueva contraseña (dejar en blanco para mantener la actual): ")

        nueva_direccion = input(f"Dirección actual ({empleado.direccion}): ")
        if not nueva_direccion.strip():
            nueva_direccion = empleado.direccion

        nuevo_telefono = input(f"Teléfono actual ({empleado.telefono}): ")
        if not nuevo_telefono.strip():
            nuevo_telefono = empleado.telefono

        nueva_fecha = input(f"Fecha inicio contrato actual ({empleado.fecha_inicio_contrato.isoformat()}): ")
        if not nueva_fecha.strip():
            nueva_fecha = empleado.fecha_inicio_contrato.isoformat()

        nuevo_salario_input = input(f"Salario actual ({empleado.salario}): ")
        try:
            nuevo_salario = float(nuevo_salario_input) if nuevo_salario_input.strip() else empleado.salario
        except ValueError:
            nuevo_salario = empleado.salario

        print("\nDepartamentos disponibles:")
        if departamentos:
            for d in departamentos:
                print(f"{d.id_departamento}.- {d.nombre_depto}")
        else:
            print("No hay departamentos registrados.")

        depto_actual_id = empleado.departamento.id_departamento if empleado.departamento else None
        depto_actual_str = depto_actual_id if depto_actual_id is not None else "Ninguno"
        opcion_depto_input = input(
            f"Seleccione nuevo ID de departamento (Actual: {depto_actual_str}, blanco para mantener, 0 para quitar): "
        )

        if not opcion_depto_input.strip():
            nuevo_id_departamento = depto_actual_id
        else:
            try:
                op_d = int(opcion_depto_input)
                nuevo_id_departamento = op_d if op_d > 0 else None
            except ValueError:
                nuevo_id_departamento = depto_actual_id

        return {
            "id_usuario": empleado.id_usuario,
            "nombre": nuevo_nombre,
            "email": nuevo_email,
            "contrasena": nueva_contrasena,
            "direccion": nueva_direccion,
            "telefono": nuevo_telefono,
            "fecha_inicio_contrato": nueva_fecha,
            "salario": nuevo_salario,
            "id_departamento": nuevo_id_departamento
        }

    @staticmethod
    def confirmar_eliminacion(nombre: str) -> bool:
        return confirmar(f"¿Está seguro que desea eliminar al empleado '{nombre}'?")

    @staticmethod
    def mostrar_mensaje(mensaje: str) -> None:
        print(f"[EMPLEADOS] {mensaje}")
