import os
import re

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def imprimir_titulo(titulo):
    limpiar_pantalla()
    print("=" * 60)
    print(f"{titulo.center(60)}")
    print("=" * 60)
    print()

def imprimir_exito(mensaje):
    print(f"✔ {mensaje}")

def imprimir_error(mensaje):
    print(f"✖ {mensaje}")

def imprimir_info(mensaje):
    print(f"ℹ {mensaje}")

def confirmar(pregunta):
    respuesta = input(f"{pregunta} (s/n): ").strip().lower()
    return respuesta in ('s', 'si', 'sí', 'y', 'yes')

def es_email_valido(email):
    """Valida que el correo tenga un formato básico correcto."""
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(patron, email))