from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import ConductorParqueController, EspacioParqueoController, TicketEstacionamientoController

conductores = ConductorParqueController()
espacios = EspacioParqueoController()
tickets = TicketEstacionamientoController(conductores, espacios)


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
# FUNCIONES DE CONDUCTORES
# =====================================================================
def crear_conductor():
    imprimir_titulo("REGISTRAR CONDUCTOR")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "placa": input("Placa del vehículo (ej. ABC-1234): "),
        "telefono": input("Teléfono: ")
    }
    mostrar_resultado(*conductores.crear(datos))
    pausa()

def listar_conductores():
    imprimir_titulo("LISTA DE CONDUCTORES")
    mostrar_lista(conductores.leer(), "No hay conductores registrados.")
    pausa()

def buscar_conductor():
    imprimir_titulo("BUSCAR CONDUCTOR")
    termino = input("Nombre, apellido o placa: ")
    mostrar_lista(conductores.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_conductor():
    imprimir_titulo("VER CONDUCTOR POR ID")
    c = conductores.obtener(pedir_entero("Id: "))
    if not c: imprimir_error("No encontrado")
    else: mostrar_detalle(c)
    pausa()

def actualizar_conductor():
    imprimir_titulo("ACTUALIZAR CONDUCTOR")
    id_c = pedir_entero("Id: ")
    c = conductores.obtener(id_c)
    if not c:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("nombre", "apellido", "email", "placa", "telefono"):
        actual = getattr(c, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*conductores.actualizar(id_c, cambios))
    pausa()

def eliminar_conductor():
    imprimir_titulo("ELIMINAR CONDUCTOR")
    id_c = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este conductor?"):
        mostrar_resultado(*conductores.eliminar(id_c))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# FUNCIONES DE ESPACIOS
# =====================================================================
def crear_espacio():
    imprimir_titulo("REGISTRAR ESPACIO DE PARQUEO")
    datos = {
        "numero_espacio": input("Número de espacio (ej. A-01): "),
        "tipo_vehiculo": input("Tipo de vehículo (Automovil, Moto, SUV): ")
    }
    mostrar_resultado(*espacios.crear(datos))
    pausa()

def listar_espacios():
    imprimir_titulo("CATÁLOGO DE ESPACIOS")
    mostrar_lista(espacios.leer(), "No hay espacios registrados.")
    pausa()

def buscar_espacio():
    imprimir_titulo("BUSCAR ESPACIO")
    termino = input("Número o tipo de vehículo: ")
    mostrar_lista(espacios.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_espacio():
    imprimir_titulo("VER ESPACIO POR ID")
    e = espacios.obtener(pedir_entero("Id: "))
    if not e: imprimir_error("No encontrado")
    else: mostrar_detalle(e)
    pausa()

def actualizar_espacio():
    imprimir_titulo("ACTUALIZAR ESPACIO")
    id_e = pedir_entero("Id: ")
    e = espacios.obtener(id_e)
    if not e:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("numero_espacio", "tipo_vehiculo"):
        actual = getattr(e, campo)
        nuevo = input(f"{campo.replace('_', ' ').capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*espacios.actualizar(id_e, cambios))
    pausa()

def eliminar_espacio():
    imprimir_titulo("ELIMINAR ESPACIO")
    id_e = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este espacio?"):
        mostrar_resultado(*espacios.eliminar(id_e))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# FUNCIONES DE TICKETS
# =====================================================================
def registrar_ticket():
    imprimir_titulo("EMITIR TICKET DE ESTACIONAMIENTO")
    imprimir_info("Conductores:")
    mostrar_lista(conductores.leer())
    imprimir_info("Espacios disponibles:")
    mostrar_lista(espacios.espacios_disponibles(), "No hay espacios libres.")

    cond_id = pedir_entero("\nId del conductor: ")
    esp_id = pedir_entero("Id del espacio: ")
    horas = float(input("Horas estimadas de estadía: ") or 1.0)

    datos = {
        "conductor_id": cond_id,
        "espacio_id": esp_id,
        "horas_estadia": horas
    }
    mostrar_resultado(*tickets.crear(datos))
    pausa()

def listar_tickets():
    imprimir_titulo("LISTA DE TICKETS EMITIDOS")
    mostrar_lista(tickets.leer(), "No hay tickets registrados.")
    pausa()

def ver_comprobante_ticket():
    imprimir_titulo("COMPROBANTE DE TICKET")
    texto = tickets.comprobante_ticket(pedir_entero("Id del ticket: "))
    if not texto: imprimir_error("No existe ese ticket")
    else: print(texto)
    pausa()

def cerrar_ticket():
    imprimir_titulo("CERRAR TICKET Y LIBERAR ESPACIO")
    id_t = pedir_entero("Id del ticket: ")
    if id_t and confirmar("¿Confirma cobrar y cerrar este ticket?"):
        mostrar_resultado(*tickets.eliminar(id_t))
    else:
        imprimir_info("Operación cancelada")
    pausa()

def resumen_parqueadero():
    imprimir_titulo("RESUMEN SISTEMA DE PARQUEADERO")
    print(f"  Conductores registrados : {len(conductores.leer())}")
    print(f"  Espacios totales        : {len(espacios.leer())}")
    print(f"  Espacios libres         : {len(espacios.espacios_disponibles())}")
    print(f"  Tickets activos         : {len(tickets.leer())}")
    print(f"  Total recaudado         : ${tickets.total_recaudado():.2f}")
    pausa()


# =====================================================================
# CONFIGURACIÓN DE MENÚS
# =====================================================================
MENU_CONDUCTORES = {
    "1": ("Registrar conductor", crear_conductor),
    "2": ("Ver todos", listar_conductores),
    "3": ("Buscar", buscar_conductor),
    "4": ("Ver por id", ver_conductor),
    "5": ("Actualizar", actualizar_conductor),
    "6": ("Eliminar", eliminar_conductor),
    "0": ("Volver", None),
}

MENU_ESPACIOS = {
    "1": ("Registrar espacio", crear_espacio),
    "2": ("Ver todos", listar_espacios),
    "3": ("Buscar", buscar_espacio),
    "4": ("Ver por id", ver_espacio),
    "5": ("Actualizar", actualizar_espacio),
    "6": ("Eliminar", eliminar_espacio),
    "0": ("Volver", None),
}

MENU_TICKETS = {
    "1": ("Emitir ticket", registrar_ticket),
    "2": ("Ver tickets", listar_tickets),
    "3": ("Ver comprobante", ver_comprobante_ticket),
    "4": ("Cerrar ticket / Liberar", cerrar_ticket),
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
        imprimir_titulo("SISTEMA DE PARQUEADERO")
        print("  1. Conductores")
        print("  2. Espacios de Parqueo")
        print("  3. Tickets de Estacionamiento")
        print("  4. Resumen")
        print("  0. Salir\n")

        tecla = input("Opción: ").strip()
        if tecla == "1": ejecutar_menu("CONDUCTORES", MENU_CONDUCTORES)
        elif tecla == "2": ejecutar_menu("ESPACIOS", MENU_ESPACIOS)
        elif tecla == "3": ejecutar_menu("TICKETS", MENU_TICKETS)
        elif tecla == "4": resumen_parqueadero()
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