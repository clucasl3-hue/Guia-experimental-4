from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import AtletaDojoController, ClaseMarcialController, InscripcionDojoController

atletas = AtletaDojoController()
clases = ClaseMarcialController()
inscripciones = InscripcionDojoController(atletas, clases)


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
# FUNCIONES DE ATLETAS
# =====================================================================
def crear_atleta():
    imprimir_titulo("REGISTRAR ATLETA")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "cinturon": input("Cinturón (ej. Blanco, Negro): ") or "Blanco",
        "socio_id": input("ID de socio (ej. SOC-001): ")
    }
    mostrar_resultado(*atletas.crear(datos))
    pausa()

def listar_atletas():
    imprimir_titulo("LISTA DE ATLETAS")
    mostrar_lista(atletas.leer(), "No hay atletas registrados.")
    pausa()

def buscar_atleta():
    imprimir_titulo("BUSCAR ATLETA")
    termino = input("Nombre, apellido o ID de socio: ")
    mostrar_lista(atletas.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_atleta():
    imprimir_titulo("VER ATLETA POR ID")
    a = atletas.obtener(pedir_entero("Id: "))
    if not a: imprimir_error("No encontrado")
    else: mostrar_detalle(a)
    pausa()

def actualizar_atleta():
    imprimir_titulo("ACTUALIZAR ATLETA")
    id_a = pedir_entero("Id: ")
    a = atletas.obtener(id_a)
    if not a:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("nombre", "apellido", "email", "cinturon", "socio_id"):
        actual = getattr(a, campo)
        nuevo = input(f"{campo.replace('_', ' ').capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*atletas.actualizar(id_a, cambios))
    pausa()

def eliminar_atleta():
    imprimir_titulo("ELIMINAR ATLETA")
    id_a = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este atleta?"):
        mostrar_resultado(*atletas.eliminar(id_a))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# FUNCIONES DE CLASES MARCIALES
# =====================================================================
def crear_clase():
    imprimir_titulo("REGISTRAR CLASE MARCIAL")
    datos = {
        "nombre_clase": input("Nombre de clase (ej. Defensa Personal): "),
        "estilo": input("Estilo (Karate, Judo, BJJ): "),
        "costo_mensual": input("Costo mensual ($): ")
    }
    mostrar_resultado(*clases.crear(datos))
    pausa()

def listar_clases():
    imprimir_titulo("CATÁLOGO DE CLASES")
    mostrar_lista(clases.leer(), "No hay clases registradas.")
    pausa()

def buscar_clase():
    imprimir_titulo("BUSCAR CLASE")
    termino = input("Nombre o estilo: ")
    mostrar_lista(clases.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_clase():
    imprimir_titulo("VER CLASE POR ID")
    c = clases.obtener(pedir_entero("Id: "))
    if not c: imprimir_error("No encontrado")
    else: mostrar_detalle(c)
    pausa()

def actualizar_clase():
    imprimir_titulo("ACTUALIZAR CLASE")
    id_c = pedir_entero("Id: ")
    c = clases.obtener(id_c)
    if not c:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("nombre_clase", "estilo", "costo_mensual"):
        actual = getattr(c, campo)
        nuevo = input(f"{campo.replace('_', ' ').capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*clases.actualizar(id_c, cambios))
    pausa()

def eliminar_clase():
    imprimir_titulo("ELIMINAR CLASE")
    id_c = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar esta clase?"):
        mostrar_resultado(*clases.eliminar(id_c))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# FUNCIONES DE INSCRIPCIONES
# =====================================================================
def registrar_inscripcion():
    imprimir_titulo("REGISTRAR INSCRIPCIÓN AL DOJO")
    imprimir_info("Atletas:")
    mostrar_lista(atletas.leer())
    imprimir_info("Clases disponibles:")
    mostrar_lista(clases.leer())

    atl_id = pedir_entero("\nId del atleta: ")
    cls_id = pedir_entero("Id de la clase: ")
    con_promo = confirmar("¿Aplicar descuento promocional (15%)?")

    datos = {
        "atleta_id": atl_id,
        "clase_id": cls_id,
        "con_promo": con_promo
    }
    mostrar_resultado(*inscripciones.crear(datos))
    pausa()

def listar_inscripciones():
    imprimir_titulo("LISTA DE INSCRIPCIONES")
    mostrar_lista(inscripciones.leer(), "No hay inscripciones registradas.")
    pausa()

def ver_comprobante_inscripcion():
    imprimir_titulo("COMPROBANTE DE INSCRIPCIÓN")
    texto = inscripciones.comprobante_inscripcion(pedir_entero("Id de la inscripción: "))
    if not texto: imprimir_error("No existe esa inscripción")
    else: print(texto)
    pausa()

def cancelar_inscripcion():
    imprimir_titulo("CANCELAR INSCRIPCIÓN")
    id_i = pedir_entero("Id de la inscripción: ")
    if id_i and confirmar("¿Confirma cancelar esta inscripción?"):
        mostrar_resultado(*inscripciones.eliminar(id_i))
    else:
        imprimir_info("Operación cancelada")
    pausa()

def resumen_dojo():
    imprimir_titulo("RESUMEN ACADEMIA / DOJO")
    print(f"  Atletas registrados   : {len(atletas.leer())}")
    print(f"  Clases en catálogo    : {len(clases.leer())}")
    print(f"  Inscripciones totales : {len(inscripciones.leer())}")
    print(f"  Total recaudado       : ${inscripciones.total_recaudado():.2f}")
    pausa()


# =====================================================================
# CONFIGURACIÓN DE MENÚS
# =====================================================================
MENU_ATLETAS = {
    "1": ("Registrar atleta", crear_atleta),
    "2": ("Ver todos", listar_atletas),
    "3": ("Buscar", buscar_atleta),
    "4": ("Ver por id", ver_atleta),
    "5": ("Actualizar", actualizar_atleta),
    "6": ("Eliminar", eliminar_atleta),
    "0": ("Volver", None),
}

MENU_CLASES = {
    "1": ("Registrar clase", crear_clase),
    "2": ("Ver catálogo", listar_clases),
    "3": ("Buscar", buscar_clase),
    "4": ("Ver por id", ver_clase),
    "5": ("Actualizar", actualizar_clase),
    "6": ("Eliminar", eliminar_clase),
    "0": ("Volver", None),
}

MENU_INSCRIPCIONES = {
    "1": ("Registrar inscripción", registrar_inscripcion),
    "2": ("Ver inscripciones", listar_inscripciones),
    "3": ("Ver comprobante", ver_comprobante_inscripcion),
    "4": ("Cancelar inscripción", cancelar_inscripcion),
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
        imprimir_titulo("SISTEMA DE DOJO - ARTES MARCIALES")
        print("  1. Atletas")
        print("  2. Clases Marciales")
        print("  3. Inscripciones")
        print("  4. Resumen")
        print("  0. Salir\n")

        tecla = input("Opción: ").strip()
        if tecla == "1": ejecutar_menu("ATLETAS", MENU_ATLETAS)
        elif tecla == "2": ejecutar_menu("CLASES", MENU_CLASES)
        elif tecla == "3": ejecutar_menu("INSCRIPCIONES", MENU_INSCRIPCIONES)
        elif tecla == "4": resumen_dojo()
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