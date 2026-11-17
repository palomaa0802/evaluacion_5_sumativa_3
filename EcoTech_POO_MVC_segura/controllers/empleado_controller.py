from models.empleado import Empleado
from models.empleado_dao import EmpleadoDAO
from models.departamento_dao import DepartamentoDAO
from views.empleado_view import EmpleadoView


class EmpleadoController:
    def __init__(self):
        self.view = EmpleadoView()

    def ejecutar(self) -> None:
        while True:
            opcion = self.view.mostrar_menu()
            if opcion == 1:
                self.agregar_empleado()
            elif opcion == 2:
                self.editar_empleado()
            elif opcion == 3:
                self.eliminar_empleado()
            elif opcion == 4:
                self.imprimir_empleado()
            elif opcion == 5:
                self.imprimir_empleados()
            elif opcion == 6:
                self.probar_inicio_sesion()
            elif opcion == 0:
                self.view.mostrar_mensaje("Saliendo de la gestión de empleados.")
                break
            else:
                self.view.mostrar_mensaje("Opción no válida.")

    def agregar_empleado(self) -> None:
        departamentos = DepartamentoDAO.obtener_todos()
        datos = self.view.formulario_nuevo_empleado(departamentos)
        try:
            departamento_seleccionado = None
            if datos.get("id_departamento"):
                departamento_seleccionado = DepartamentoDAO.obtener_por_id(datos["id_departamento"])

            nuevo_empleado = Empleado(
                nombre=datos["nombre"],
                email=datos["email"],
                contrasena=datos["contrasena"],
                direccion=datos["direccion"],
                telefono=datos["telefono"],
                fecha_inicio_contrato=datos["fecha_inicio_contrato"],
                salario=datos["salario"],
                departamento=departamento_seleccionado
            )

            if EmpleadoDAO.obtener_por_email(nuevo_empleado.email):
                self.view.mostrar_mensaje(f"Error: Ya existe un empleado con el email '{nuevo_empleado.email}'.")
                return

            exito = EmpleadoDAO.crear(nuevo_empleado)
            if exito:
                if departamento_seleccionado:
                    departamento_seleccionado.agregarEmpleado(nuevo_empleado)
                self.view.mostrar_mensaje(f"Empleado agregado exitosamente con ID {nuevo_empleado.id_usuario}.")
            else:
                self.view.mostrar_mensaje("Error al guardar en la base de datos.")
        except (ValueError, TypeError) as e:
            self.view.mostrar_mensaje(f"Error en los datos ingresados: {e}")

    def editar_empleado(self) -> None:
        id_usuario = self.view.solicitar_id()
        empleado = EmpleadoDAO.obtener_por_id(id_usuario)
        if not empleado:
            self.view.mostrar_mensaje("Empleado no encontrado.")
            return

        departamentos = DepartamentoDAO.obtener_todos()
        datos_nuevos = self.view.formulario_editar_empleado(empleado, departamentos)
        try:
            empleado.nombre = datos_nuevos["nombre"]
            empleado.email = datos_nuevos["email"]
            if datos_nuevos["contrasena"]:
                empleado.setContrasena(datos_nuevos["contrasena"])
            empleado.direccion = datos_nuevos["direccion"]
            empleado.setTelefono(datos_nuevos["telefono"])
            empleado.fecha_inicio_contrato = datos_nuevos["fecha_inicio_contrato"]
            empleado.setSalario(datos_nuevos["salario"])

            departamento_seleccionado = None
            if datos_nuevos.get("id_departamento"):
                departamento_seleccionado = DepartamentoDAO.obtener_por_id(datos_nuevos["id_departamento"])
            empleado.departamento = departamento_seleccionado

            exito = EmpleadoDAO.actualizar(empleado)
            if exito:
                self.view.mostrar_mensaje("Empleado actualizado exitosamente.")
            else:
                self.view.mostrar_mensaje("Error al actualizar en la base de datos.")
        except (ValueError, TypeError) as e:
            self.view.mostrar_mensaje(f"Error en los datos modificados: {e}")

    def eliminar_empleado(self) -> None:
        id_usuario = self.view.solicitar_id()
        empleado = EmpleadoDAO.obtener_por_id(id_usuario)
        if not empleado:
            self.view.mostrar_mensaje("Empleado no encontrado.")
            return

        if self.view.confirmar_eliminacion(empleado.nombre):
            exito = EmpleadoDAO.eliminar(id_usuario)
            if exito:
                self.view.mostrar_mensaje("Empleado eliminado exitosamente.")
            else:
                self.view.mostrar_mensaje("Error al eliminar en la base de datos.")
        else:
            self.view.mostrar_mensaje("Operación cancelada.")

    def imprimir_empleado(self) -> None:
        id_usuario = self.view.solicitar_id()
        empleado = EmpleadoDAO.obtener_por_id(id_usuario)
        if empleado:
            self.view.mostrar_empleado(empleado)
        else:
            self.view.mostrar_mensaje("Empleado no encontrado.")

    def imprimir_empleados(self) -> None:
        empleados = EmpleadoDAO.obtener_todos()
        self.view.mostrar_lista_empleados(empleados)

    def probar_inicio_sesion(self) -> None:
        credenciales = self.view.solicitar_credenciales()
        empleado = EmpleadoDAO.obtener_por_email(credenciales["email"])
        if not empleado:
            self.view.mostrar_mensaje("No se encontró un empleado con ese correo.")
            return
        if empleado.iniciarSesion(credenciales["email"], credenciales["contrasena"]):
            self.view.mostrar_mensaje(f"¡Inicio de sesión exitoso! Bienvenido/a, {empleado.getNombre()}.")
        else:
            self.view.mostrar_mensaje("Contraseña incorrecta. Acceso denegado.")
