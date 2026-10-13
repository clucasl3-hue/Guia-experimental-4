from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import HuespedController, HabitacionController, ReservaController

huespedes = HuespedController()
habitaciones = HabitacionController()
reservas = ReservaController(huespedes, habitaciones)


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
# MENÚ HUÉSPEDES
# =====================================================================
def crear_huesped():
    imprimir_titulo("REGISTRAR HUÉSPED")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "pasaporte": input("Pasaporte: "),
        "pais": input("País de origen: ")
    }
    mostrar_resultado(*huespedes.crear(datos))
    pausa()

def listar_huespedes():
    imprimir_titulo("LISTA DE HUÉSPEDES")
    mostrar_lista(huespedes.leer(), "No hay huéspedes registrados.")
    pausa()

def buscar_huesped():
    imprimir_titulo("BUSCAR HUÉSPED")
    termino = input("Nombre, apellido o pasaporte: ")
    mostrar_lista(huespedes.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_huesped():
    imprimir_titulo("VER HUÉSPED POR ID")
    h = huespedes.obtener(pedir_entero("Id: "))
    if not h: imprimir_error("No encontrado")
    else: mostrar_detalle(h)
    pausa()

def actualizar_huesped():
    imprimir_titulo("ACTUALIZAR HUÉSPED")
    id_h = pedir_entero("Id: ")
    h = huespedes.obtener(id_h)
    if not h:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("nombre", "apellido", "email", "pasaporte", "pais"):
        actual = getattr(h, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*huespedes.actualizar(id_h, cambios))
    pausa()

def eliminar_huesped():
    imprimir_titulo("ELIMINAR HUÉSPED")
    id_h = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este huésped?"):
        mostrar_resultado(*huespedes.eliminar(id_h))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ HABITACIONES
# =====================================================================
def crear_habitacion():
    imprimir_titulo("REGISTRAR HABITACIÓN")
    datos = {
        "numero_habitacion": input("Número de habitación (ej. 101): "),
        "tipo": input("Tipo (Simple, Doble, Suite): "),
        "precio_noche": input("Precio por noche ($): ")
    }
    mostrar_resultado(*habitaciones.crear(datos))
    pausa()

def listar_habitaciones():
    imprimir_titulo("LISTA DE HABITACIONES")
    mostrar_lista(habitaciones.leer(), "No hay habitaciones registradas.")
    pausa()

def buscar_habitacion():
    imprimir_titulo("BUSCAR HABITACIÓN")
    termino = input("Número o tipo: ")
    mostrar_lista(habitaciones.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_habitacion():
    imprimir_titulo("VER HABITACIÓN POR ID")
    hab = habitaciones.obtener(pedir_entero("Id: "))
    if not hab: imprimir_error("No encontrado")
    else: mostrar_detalle(hab)
    pausa()

def actualizar_habitacion():
    imprimir_titulo("ACTUALIZAR HABITACIÓN")
    id_hab = pedir_entero("Id: ")
    hab = habitaciones.obtener(id_hab)
    if not hab:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("numero_habitacion", "tipo", "precio_noche"):
        actual = getattr(hab, campo)
        nuevo = input(f"{campo.replace('_', ' ').capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*habitaciones.actualizar(id_hab, cambios))
    pausa()

def eliminar_habitacion():
    imprimir_titulo("ELIMINAR HABITACIÓN")
    id_hab = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar esta habitación?"):
        mostrar_resultado(*habitaciones.eliminar(id_hab))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ RESERVAS
# =====================================================================
def crear_reserva():
    imprimir_titulo("REGISTRAR RESERVA DE HOTEL")
    imprimir_info("Huéspedes:")
    mostrar_lista(huespedes.leer())
    imprimir_info("Habitaciones Disponibles:")
    mostrar_lista(habitaciones.habitaciones_disponibles(), "No hay habitaciones libres.")

    hue_id = pedir_entero("\nId del huésped: ")
    hab_id = pedir_entero("Id de la habitación: ")
    noches = pedir_entero("Cantidad de noches: ")
    fecha = input("Fecha de inicio (ej. 2026-06-15): ")

    datos = {
        "huesped_id": hue_id,
        "habitacion_id": hab_id,
        "noches": noches,
        "fecha_inicio": fecha
    }
    mostrar_resultado(*reservas.crear(datos))
    pausa()

def listar_reservas():
    imprimir_titulo("LISTA DE RESERVAS")
    mostrar_lista(reservas.leer(), "No hay reservas registradas.")
    pausa()

def ver_comprobante_reserva():
    imprimir_titulo("COMPROBANTE DE RESERVA")
    texto = reservas.comprobante_reserva(pedir_entero("Id de la reserva: "))
    if not texto: imprimir_error("No existe esa reserva")
    else: print(texto)
    pausa()

def cancelar_reserva():
    imprimir_titulo("CANCELAR RESERVA")
    id_r = pedir_entero("Id de la reserva: ")
    if id_r and confirmar("¿Confirma cancelar esta reserva?"):
        mostrar_resultado(*reservas.eliminar(id_r))
    else:
        imprimir_info("Operación cancelada")
    pausa()

def resumen_hotel():
    imprimir_titulo("RESUMEN DE HOTEL")
    print(f"  Huéspedes registrados   : {len(huespedes.leer())}")
    print(f"  Habitaciones totales    : {len(habitaciones.leer())}")
    print(f"  Habitaciones libres     : {len(habitaciones.habitaciones_disponibles())}")
    print(f"  Reservas totales        : {len(reservas.leer())}")
    print(f"  Total recaudado (IVA)   : ${reservas.total_recaudado():.2f}")
    pausa()


# =====================================================================
# CONFIGURACIÓN DE MENÚS (Diccionarios)
# =====================================================================
MENU_HUESPEDES = {
    "1": ("Registrar huésped", crear_huesped),
    "2": ("Ver todos", listar_huespedes),
    "3": ("Buscar", buscar_huesped),
    "4": ("Ver por id", ver_huesped),
    "5": ("Actualizar", actualizar_huesped),
    "6": ("Eliminar", eliminar_huesped),
    "0": ("Volver", None),
}

MENU_HABITACIONES = {
    "1": ("Registrar habitación", crear_habitacion),
    "2": ("Ver todas", listar_habitaciones),
    "3": ("Buscar", buscar_habitacion),
    "4": ("Ver por id", ver_habitacion),
    "5": ("Actualizar", actualizar_habitacion),
    "6": ("Eliminar", eliminar_habitacion),
    "0": ("Volver", None),
}

MENU_RESERVAS = {
    "1": ("Crear reserva", crear_reserva),
    "2": ("Ver reservas", listar_reservas),
    "3": ("Ver comprobante", ver_comprobante_reserva),
    "4": ("Cancelar reserva", cancelar_reserva),
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
        imprimir_titulo("SISTEMA DE RESERVA DE HOTEL")
        print("  1. Huéspedes")
        print("  2. Habitaciones")
        print("  3. Reservas")
        print("  4. Resumen")
        print("  0. Salir\n")

        tecla = input("Opción: ").strip()
        if tecla == "1": ejecutar_menu("HUÉSPEDES", MENU_HUESPEDES)
        elif tecla == "2": ejecutar_menu("HABITACIONES", MENU_HABITACIONES)
        elif tecla == "3": ejecutar_menu("RESERVAS", MENU_RESERVAS)
        elif tecla == "4": resumen_hotel()
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