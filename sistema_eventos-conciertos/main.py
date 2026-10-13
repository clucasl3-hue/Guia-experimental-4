from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import AsistenteController, EventoConciertoController, EntradaConciertoController

asistentes = AsistenteController()
eventos = EventoConciertoController()
entradas = EntradaConciertoController(asistentes, eventos)


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
# FUNCIONES DE ASISTENTES
# =====================================================================
def crear_asistente():
    imprimir_titulo("REGISTRAR ASISTENTE")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "cedula": input("Cédula: "),
        "telefono": input("Teléfono: ")
    }
    mostrar_resultado(*asistentes.crear(datos))
    pausa()

def listar_asistentes():
    imprimir_titulo("LISTA DE ASISTENTES")
    mostrar_lista(asistentes.leer(), "No hay asistentes registrados.")
    pausa()

def buscar_asistente():
    imprimir_titulo("BUSCAR ASISTENTE")
    termino = input("Nombre, apellido o cédula: ")
    mostrar_lista(asistentes.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_asistente():
    imprimir_titulo("VER ASISTENTE POR ID")
    a = asistentes.obtener(pedir_entero("Id: "))
    if not a: imprimir_error("No encontrado")
    else: mostrar_detalle(a)
    pausa()

def actualizar_asistente():
    imprimir_titulo("ACTUALIZAR ASISTENTE")
    id_a = pedir_entero("Id: ")
    a = asistentes.obtener(id_a)
    if not a:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("nombre", "apellido", "email", "cedula", "telefono"):
        actual = getattr(a, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*asistentes.actualizar(id_a, cambios))
    pausa()

def eliminar_asistente():
    imprimir_titulo("ELIMINAR ASISTENTE")
    id_a = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este asistente?"):
        mostrar_resultado(*asistentes.eliminar(id_a))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# FUNCIONES DE EVENTOS / CONCIERTOS
# =====================================================================
def crear_evento():
    imprimir_titulo("REGISTRAR EVENTO / CONCIERTO")
    datos = {
        "nombre_evento": input("Nombre del evento (ej. Rock Fest): "),
        "codigo_evento": input("Código (ej. EVT-01): "),
        "precio_base": input("Precio base de entrada ($): "),
        "aforo_maximo": input("Aforo máximo de personas: ")
    }
    mostrar_resultado(*eventos.crear(datos))
    pausa()

def listar_eventos():
    imprimir_titulo("CARTELERA DE EVENTOS")
    mostrar_lista(eventos.leer(), "No hay eventos registrados.")
    pausa()

def buscar_evento():
    imprimir_titulo("BUSCAR EVENTO")
    termino = input("Nombre o código: ")
    mostrar_lista(eventos.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_evento():
    imprimir_titulo("VER EVENTO POR ID")
    e = eventos.obtener(pedir_entero("Id: "))
    if not e: imprimir_error("No encontrado")
    else: mostrar_detalle(e)
    pausa()

def actualizar_evento():
    imprimir_titulo("ACTUALIZAR EVENTO")
    id_e = pedir_entero("Id: ")
    e = eventos.obtener(id_e)
    if not e:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("nombre_evento", "codigo_evento", "precio_base", "aforo_maximo"):
        actual = getattr(e, campo)
        nuevo = input(f"{campo.replace('_', ' ').capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*eventos.actualizar(id_e, cambios))
    pausa()

def eliminar_evento():
    imprimir_titulo("ELIMINAR EVENTO")
    id_e = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este evento?"):
        mostrar_resultado(*eventos.eliminar(id_e))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# FUNCIONES DE ENTRADAS
# =====================================================================
def registrar_entrada():
    imprimir_titulo("COMPRAR ENTRADA / BOLETO")
    imprimir_info("Asistentes:")
    mostrar_lista(asistentes.leer())
    imprimir_info("Eventos disponibles:")
    mostrar_lista(eventos.leer())

    ast_id = pedir_entero("\nId del asistente: ")
    ev_id = pedir_entero("Id del evento: ")
    es_vip = confirmar("¿Desea localidad VIP (incluye recargo de $25)?")

    datos = {
        "asistente_id": ast_id,
        "evento_id": ev_id,
        "es_vip": es_vip
    }
    mostrar_resultado(*entradas.crear(datos))
    pausa()

def listar_entradas():
    imprimir_titulo("LISTA DE ENTRADAS VENDIDAS")
    mostrar_lista(entradas.leer(), "No hay entradas registradas.")
    pausa()

def ver_comprobante_entrada():
    imprimir_titulo("COMPROBANTE DE ENTRADA")
    texto = entradas.comprobante_entrada(pedir_entero("Id de la entrada: "))
    if not texto: imprimir_error("No existe esa entrada")
    else: print(texto)
    pausa()

def cancelar_entrada():
    imprimir_titulo("CANCELAR ENTRADA")
    id_en = pedir_entero("Id de la entrada: ")
    if id_en and confirmar("¿Confirma cancelar esta entrada?"):
        mostrar_resultado(*entradas.eliminar(id_en))
    else:
        imprimir_info("Operación cancelada")
    pausa()

def resumen_eventos():
    imprimir_titulo("RESUMEN GESTIÓN DE EVENTOS")
    print(f"  Asistentes registrados : {len(asistentes.leer())}")
    print(f"  Eventos en cartelera   : {len(eventos.leer())}")
    print(f"  Entradas vendidas      : {len(entradas.leer())}")
    print(f"  Total recaudado        : ${entradas.total_recaudado():.2f}")
    pausa()


# =====================================================================
# CONFIGURACIÓN DE MENÚS
# =====================================================================
MENU_ASISTENTES = {
    "1": ("Registrar asistente", crear_asistente),
    "2": ("Ver todos", listar_asistentes),
    "3": ("Buscar", buscar_asistente),
    "4": ("Ver por id", ver_asistente),
    "5": ("Actualizar", actualizar_asistente),
    "6": ("Eliminar", eliminar_asistente),
    "0": ("Volver", None),
}

MENU_EVENTOS = {
    "1": ("Registrar evento", crear_evento),
    "2": ("Ver cartelera", listar_eventos),
    "3": ("Buscar", buscar_evento),
    "4": ("Ver por id", ver_evento),
    "5": ("Actualizar", actualizar_evento),
    "6": ("Eliminar", eliminar_evento),
    "0": ("Volver", None),
}

MENU_ENTRADAS = {
    "1": ("Comprar entrada", registrar_entrada),
    "2": ("Ver entradas", listar_entradas),
    "3": ("Ver comprobante", ver_comprobante_entrada),
    "4": ("Cancelar entrada", cancelar_entrada),
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
        imprimir_titulo("SISTEMA DE GESTIÓN DE EVENTOS")
        print("  1. Asistentes")
        print("  2. Eventos / Conciertos")
        print("  3. Entradas / Boletos")
        print("  4. Resumen")
        print("  0. Salir\n")

        tecla = input("Opción: ").strip()
        if tecla == "1": ejecutar_menu("ASISTENTES", MENU_ASISTENTES)
        elif tecla == "2": ejecutar_menu("EVENTOS", MENU_EVENTOS)
        elif tecla == "3": ejecutar_menu("ENTRADAS", MENU_ENTRADAS)
        elif tecla == "4": resumen_eventos()
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