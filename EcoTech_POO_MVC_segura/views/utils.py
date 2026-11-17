from datetime import datetime


def leer_numero(mensaje: str) -> int:
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: Debe ingresar un número entero válido.")


def leer_flotante(mensaje: str) -> float:
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Error: Debe ingresar un número decimal válido.")


def leer_fecha(mensaje: str) -> str:
    while True:
        valor = input(mensaje).strip()
        try:
            datetime.strptime(valor, "%Y-%m-%d")
            return valor
        except ValueError:
            print("Error: Debe ingresar una fecha válida en formato YYYY-MM-DD (ej: 2026-03-15).")


def confirmar(mensaje: str) -> bool:
    while True:
        resp = input(f"{mensaje} (si/no): ").strip().lower()
        if resp in ("si", "no"):
            return resp == "si"
        print("Respuesta no válida. Por favor, ingrese 'si' o 'no'.")
