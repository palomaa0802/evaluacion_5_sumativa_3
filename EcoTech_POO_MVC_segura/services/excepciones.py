class ErrorServicio(Exception):
    """Error general al usar un servicio externo."""

    def __init__(self, mensaje_usuario: str, detalle_tecnico: str = ""):
        super().__init__(mensaje_usuario)
        self.mensaje_usuario = mensaje_usuario
        # el detalle técnico solo va al log, nunca a la pantalla
        self.detalle_tecnico = detalle_tecnico


class ErrorConexion(ErrorServicio):
    """No hay internet o no se pudo llegar al servidor."""


class ErrorTiempoEspera(ErrorServicio):
    """El servidor se demoró demasiado en responder."""


class ErrorHTTP(ErrorServicio):
    """El servidor respondió con un código de error."""


class ErrorFormato(ErrorServicio):
    """La respuesta no es un JSON válido o le faltan campos."""


class ErrorDatos(ErrorServicio):
    """Los datos llegaron pero no son utilizables (valores fuera de rango)."""
