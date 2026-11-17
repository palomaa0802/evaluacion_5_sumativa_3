from services.cliente_http import ClienteHTTP
from services.excepciones import ErrorFormato, ErrorDatos
from services.validaciones import ValidacionesServicios

URL_CAMBIO = "https://open.er-api.com/v6/latest/USD"


class CambioService:
    """Convierte el salario de un empleado (en pesos chilenos) a otra moneda."""

    def __init__(self):
        self._http = ClienteHTTP()

    def _obtener_tasas(self) -> dict:
        datos = self._http.obtener_json(URL_CAMBIO)
        if datos.get("result") != "success":
            raise ErrorFormato("El servicio de monedas no pudo entregar los valores.", "result distinto de success")
        tasas = datos.get("rates")
        if not isinstance(tasas, dict):
            raise ErrorFormato("El servicio de monedas entregó datos inesperados.", "Falta el campo rates")
        return tasas

    @staticmethod
    def _tasa_valida(tasas: dict, moneda: str) -> float:
        valor = tasas.get(moneda)
        if isinstance(valor, bool) or not isinstance(valor, (int, float)) or valor <= 0:
            raise ErrorDatos("No hay un tipo de cambio utilizable para " + moneda + ".", "Tasa inválida para " + moneda)
        return valor

    def convertir_salario(self, salario_clp: float, moneda: str) -> dict | None:
        """Devuelve el cálculo, o None si la moneda no es válida (no se llama a la API)."""
        moneda = ValidacionesServicios.sanear_moneda(moneda)
        if moneda is None:
            return None
        if isinstance(salario_clp, bool) or not isinstance(salario_clp, (int, float)) or salario_clp <= 0:
            raise ErrorDatos("El salario no es válido para calcular la conversión.", "Salario inválido")

        tasas = self._obtener_tasas()
        tasa_clp = self._tasa_valida(tasas, "CLP")
        tasa_destino = self._tasa_valida(tasas, moneda)
        # la API entrega todo respecto al dólar: CLP -> USD -> moneda destino
        valor_usd = salario_clp / tasa_clp
        return {
            "moneda": moneda,
            "salario_clp": salario_clp,
            "tipo_cambio": tasa_destino / tasa_clp,
            "monto": round(valor_usd * tasa_destino, 2)
        }
