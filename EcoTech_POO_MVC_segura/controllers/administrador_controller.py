from models.administrador import Administrador
from models.administrador_dao import AdministradorDAO
from views.administrador_view import AdministradorView


class AdministradorController:
    def __init__(self):
        self.view = AdministradorView()

    def ejecutar(self) -> None:
        while True:
            opcion = self.view.mostrar_menu()
            if opcion == 1:
                self.agregar_administrador()
            elif opcion == 2:
                self.editar_administrador()
            elif opcion == 3:
                self.eliminar_administrador()
            elif opcion == 4:
                self.imprimir_administrador()
            elif opcion == 5:
                self.imprimir_administradores()
            elif opcion == 6:
                self.probar_inicio_sesion()
            elif opcion == 0:
                self.view.mostrar_mensaje("Saliendo de la gestión de administradores.")
                break
            else:
                self.view.mostrar_mensaje("Opción no válida.")

    def agregar_administrador(self) -> None:
        datos = self.view.formulario_nuevo_administrador()
        try:
            nuevo_admin = Administrador(
                nombre=datos["nombre"],
                email=datos["email"],
                contrasena=datos["contrasena"],
                nivel_permiso=datos["nivel_permiso"]
            )
            if AdministradorDAO.obtener_por_email(nuevo_admin.email):
                self.view.mostrar_mensaje(f"Error: Ya existe un administrador con el email '{nuevo_admin.email}'.")
                return

            exito = AdministradorDAO.crear(nuevo_admin)
            if exito:
                self.view.mostrar_mensaje(f"Administrador agregado exitosamente con ID {nuevo_admin.id_usuario}.")
            else:
                self.view.mostrar_mensaje("Error al guardar en la base de datos.")
        except (ValueError, TypeError) as e:
            self.view.mostrar_mensaje(f"Error en los datos ingresados: {e}")

    def editar_administrador(self) -> None:
        id_usuario = self.view.solicitar_id()
        administrador = AdministradorDAO.obtener_por_id(id_usuario)
        if not administrador:
            self.view.mostrar_mensaje("Administrador no encontrado.")
            return

        datos_nuevos = self.view.formulario_editar_administrador(administrador)
        try:
            administrador.nombre = datos_nuevos["nombre"]
            administrador.email = datos_nuevos["email"]
            if datos_nuevos["contrasena"]:
                administrador.setContrasena(datos_nuevos["contrasena"])
            administrador.nivel_permiso = datos_nuevos["nivel_permiso"]

            exito = AdministradorDAO.actualizar(administrador)
            if exito:
                self.view.mostrar_mensaje("Administrador actualizado exitosamente.")
            else:
                self.view.mostrar_mensaje("Error al actualizar en la base de datos.")
        except (ValueError, TypeError) as e:
            self.view.mostrar_mensaje(f"Error en los datos modificados: {e}")

    def eliminar_administrador(self) -> None:
        id_usuario = self.view.solicitar_id()
        administrador = AdministradorDAO.obtener_por_id(id_usuario)
        if not administrador:
            self.view.mostrar_mensaje("Administrador no encontrado.")
            return

        if self.view.confirmar_eliminacion(administrador.nombre):
            exito = AdministradorDAO.eliminar(id_usuario)
            if exito:
                self.view.mostrar_mensaje("Administrador eliminado exitosamente.")
            else:
                self.view.mostrar_mensaje("Error al eliminar en la base de datos.")
        else:
            self.view.mostrar_mensaje("Operación cancelada.")

    def imprimir_administrador(self) -> None:
        id_usuario = self.view.solicitar_id()
        administrador = AdministradorDAO.obtener_por_id(id_usuario)
        if administrador:
            self.view.mostrar_administrador(administrador)
        else:
            self.view.mostrar_mensaje("Administrador no encontrado.")

    def imprimir_administradores(self) -> None:
        administradores = AdministradorDAO.obtener_todos()
        self.view.mostrar_lista_administradores(administradores)

    def probar_inicio_sesion(self) -> None:
        credenciales = self.view.solicitar_credenciales()
        administrador = AdministradorDAO.obtener_por_email(credenciales["email"])
        if not administrador:
            self.view.mostrar_mensaje("No se encontró un administrador con ese correo.")
            return
        if administrador.iniciarSesion(credenciales["email"], credenciales["contrasena"]):
            self.view.mostrar_mensaje(f"¡Inicio de sesión exitoso! {administrador.gestionarUsuarios()}")
        else:
            self.view.mostrar_mensaje("Contraseña incorrecta. Acceso denegado.")
