from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import PasajeroController, VueloController, BoletoAvionController

pasajeros = PasajeroController()
vuelos = VueloController()
boletos_avion = BoletoAvionController(pasajeros, vuelos)


def pausa():
    input("\nPresione Enter para continuar...")


def pedir_entero(etiqueta):
    try:
        return int(input(etiqueta))
    except ValueError:
        return None


def mostrar_resultado(exito, mensaje):
    if exito: imprimir_exito(mensaje)
    else: imprimir_error(mensaje)


def mostrar_lista(objetos, vacio="No hay registros todavía."):
    if not objetos:
        imprimir_info(vacio)
        return
    for obj in objetos:
        print(f"  {obj}")
    imprimir_info(f"Total: {len(objetos)}")


def mostrar_detalle(objeto):
    for clave, valor in objeto.a_diccionario().items():
        print(f"  {str(clave).replace('_', ' ').capitalize():<16}: {valor}")


# =====================================================================
# MENÚ PASAJEROS
# =====================================================================
def crear_pasajero():
    imprimir_titulo("REGISTRAR PASAJERO")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "pasaporte": input("Pasaporte: "),
        "nacionalidad": input("Nacionalidad: ")
    }
    mostrar_resultado(*pasajeros.crear(datos))
    pausa()

def listar_pasajeros():
    imprimir_titulo("LISTA DE PASAJEROS")
    mostrar_lista(pasajeros.leer(), "No hay pasajeros registrados.")
    pausa()

def buscar_pasajero():
    imprimir_titulo("BUSCAR PASAJERO")
    termino = input("Nombre, apellido o pasaporte: ")
    mostrar_lista(pasajeros.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_pasajero():
    imprimir_titulo("VER PASAJERO POR ID")
    p = pasajeros.obtener(pedir_entero("Id: "))
    if not p: imprimir_error("No encontrado")
    else: mostrar_detalle(p)
    pausa()

def actualizar_pasajero():
    imprimir_titulo("ACTUALIZAR PASAJERO")
    id_p = pedir_entero("Id: ")
    p = pasajeros.obtener(id_p)
    if not p:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("nombre", "apellido", "email", "pasaporte", "nacionalidad"):
        actual = getattr(p, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*pasajeros.actualizar(id_p, cambios))
    pausa()

def eliminar_pasajero():
    imprimir_titulo("ELIMINAR PASAJERO")
    id_p = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este pasajero?"):
        mostrar_resultado(*pasajeros.eliminar(id_p))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ VUELOS
# =====================================================================
def crear_vuelo():
    imprimir_titulo("REGISTRAR VUELO")
    datos = {
        "codigo_vuelo": input("Código de vuelo (ej. VUELO101): "),
        "origen": input("Origen: "),
        "destino": input("Destino: "),
        "asientos_disponibles": input("Asientos (Enter para 50): "),
        "precio_base": input("Precio base ($): ")
    }
    mostrar_resultado(*vuelos.crear(datos))
    pausa()

def listar_vuelos():
    imprimir_titulo("ITINERARIO DE VUELOS")
    mostrar_lista(vuelos.leer(), "No hay vuelos registrados.")
    pausa()

def buscar_vuelo():
    imprimir_titulo("BUSCAR VUELO")
    termino = input("Código, origen o destino: ")
    mostrar_lista(vuelos.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_vuelo():
    imprimir_titulo("VER VUELO POR ID")
    v = vuelos.obtener(pedir_entero("Id: "))
    if not v: imprimir_error("No encontrado")
    else: mostrar_detalle(v)
    pausa()

def actualizar_vuelo():
    imprimir_titulo("ACTUALIZAR VUELO")
    id_v = pedir_entero("Id: ")
    v = vuelos.obtener(id_v)
    if not v:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("codigo_vuelo", "origen", "destino", "asientos_disponibles", "precio_base"):
        actual = getattr(v, campo)
        nuevo = input(f"{campo.replace('_', ' ').capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*vuelos.actualizar(id_v, cambios))
    pausa()

def eliminar_vuelo():
    imprimir_titulo("ELIMINAR VUELO")
    id_v = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este vuelo?"):
        mostrar_resultado(*vuelos.eliminar(id_v))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ BOLETOS DE AVIÓN
# =====================================================================
def reservar_vuelo():
    imprimir_titulo("RESERVAR BOLETO DE AVIÓN")
    imprimir_info("Pasajeros:")
    mostrar_lista(pasajeros.leer())
    imprimir_info("Vuelos disponibles:")
    mostrar_lista(vuelos.vuelos_con_asientos(), "No hay vuelos con asientos.")

    pas_id = pedir_entero("\nId del pasajero: ")
    vue_id = pedir_entero("Id del vuelo: ")
    clase = input("Clase (Económica / VIP): ") or "Económica"

    datos = {
        "pasajero_id": pas_id,
        "vuelo_id": vue_id,
        "clase_asiento": clase
    }
    mostrar_resultado(*boletos_avion.crear(datos))
    pausa()

def listar_boletos_avion():
    imprimir_titulo("LISTA DE BOLETOS EMITIDOS")
    mostrar_lista(boletos_avion.leer(), "No hay boletos emitidos.")
    pausa()

def ver_comprobante_boleto_avion():
    imprimir_titulo("COMPROBANTE DE BOLETO")
    texto = boletos_avion.comprobante_boleto(pedir_entero("Id del boleto: "))
    if not texto: imprimir_error("No existe ese boleto")
    else: print(texto)
    pausa()

def cancelar_boleto_avion():
    imprimir_titulo("CANCELAR BOLETO")
    id_b = pedir_entero("Id del boleto: ")
    if id_b and confirmar("¿Confirma cancelar la reserva?"):
        mostrar_resultado(*boletos_avion.eliminar(id_b))
    else:
        imprimir_info("Operación cancelada")
    pausa()

def resumen_aerolinea():
    imprimir_titulo("RESUMEN DE AEROLÍNEA")
    print(f"  Pasajeros registrados   : {len(pasajeros.leer())}")
    print(f"  Vuelos en itinerario    : {len(vuelos.leer())}")
    print(f"  Boletos emitidos        : {len(boletos_avion.leer())}")
    print(f"  Total recaudado         : ${boletos_avion.total_recaudado():.2f}")
    pausa()


# =====================================================================
# CONFIGURACIÓN DE MENÚS (Diccionarios)
# =====================================================================
MENU_PASAJEROS = {
    "1": ("Registrar pasajero", crear_pasajero),
    "2": ("Ver todos", listar_pasajeros),
    "3": ("Buscar", buscar_pasajero),
    "4": ("Ver por id", ver_pasajero),
    "5": ("Actualizar", actualizar_pasajero),
    "6": ("Eliminar", eliminar_pasajero),
    "0": ("Volver", None),
}

MENU_VUELOS = {
    "1": ("Registrar vuelo", crear_vuelo),
    "2": ("Ver itinerario", listar_vuelos),
    "3": ("Buscar", buscar_vuelo),
    "4": ("Ver por id", ver_vuelo),
    "5": ("Actualizar", actualizar_vuelo),
    "6": ("Eliminar", eliminar_vuelo),
    "0": ("Volver", None),
}

MENU_BOLETOS = {
    "1": ("Reservar vuelo", reservar_vuelo),
    "2": ("Ver boletos", listar_boletos_avion),
    "3": ("Ver comprobante", ver_comprobante_boleto_avion),
    "4": ("Cancelar boleto", cancelar_boleto_avion),
    "0": ("Volver", None),
}


def ejecutar_menu(titulo, opciones):
    while True:
        imprimir_titulo(titulo)
        for tecla, (texto, _) in opciones.items():
            print(f"  {tecla}. {texto}")
        print()

        tecla = input("Opción: ").strip()
        if tecla not in opciones:
            imprimir_error("Opción no válida")
            pausa()
            continue

        _, funcion = opciones[tecla]
        if funcion is None: break
        funcion()


def main():
    while True:
        imprimir_titulo("SISTEMA DE AEROLÍNEA - VUELOS")
        print("  1. Pasajeros")
        print("  2. Vuelos")
        print("  3. Boletos / Reservas")
        print("  4. Resumen")
        print("  0. Salir\n")

        tecla = input("Opción: ").strip()
        if tecla == "1": ejecutar_menu("PASAJEROS", MENU_PASAJEROS)
        elif tecla == "2": ejecutar_menu("VUELOS", MENU_VUELOS)
        elif tecla == "3": ejecutar_menu("BOLETOS", MENU_BOLETOS)
        elif tecla == "4": resumen_aerolinea()
        elif tecla == "0":
            imprimir_info("¡Hasta luego! 👋")
            break
        else:
            imprimir_error("Opción no válida")
            pausa()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")