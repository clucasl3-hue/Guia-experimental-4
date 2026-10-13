from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import SocioController, ClaseGrupalController, InscripcionClaseController

socios = SocioController()
clases = ClaseGrupalController()
inscripciones = InscripcionClaseController(socios, clases)


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
# MENÚ SOCIOS
# =====================================================================
def crear_socio():
    imprimir_titulo("REGISTRAR SOCIO")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "nro_socio": input("Número de socio (ej. SOC001): "),
        "objetivo": input("Objetivo (ej. Hipertrofia, Cardio): ")
    }
    mostrar_resultado(*socios.crear(datos))
    pausa()

def listar_socios():
    imprimir_titulo("LISTA DE SOCIOS")
    mostrar_lista(socios.leer(), "No hay socios registrados.")
    pausa()

def buscar_socio():
    imprimir_titulo("BUSCAR SOCIO")
    termino = input("Nombre, apellido o nro de socio: ")
    mostrar_lista(socios.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_socio():
    imprimir_titulo("VER SOCIO POR ID")
    s = socios.obtener(pedir_entero("Id: "))
    if not s: imprimir_error("No encontrado")
    else: mostrar_detalle(s)
    pausa()

def actualizar_socio():
    imprimir_titulo("ACTUALIZAR SOCIO")
    id_s = pedir_entero("Id: ")
    s = socios.obtener(id_s)
    if not s:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("nombre", "apellido", "email", "nro_socio", "objetivo"):
        actual = getattr(s, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*socios.actualizar(id_s, cambios))
    pausa()

def eliminar_socio():
    imprimir_titulo("ELIMINAR SOCIO")
    id_s = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este socio?"):
        mostrar_resultado(*socios.eliminar(id_s))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ CLASES GRUPALES
# =====================================================================
def crear_clase():
    imprimir_titulo("REGISTRAR CLASE GRUPAL")
    datos = {
        "nombre_clase": input("Nombre de la clase (ej. Spinning): "),
        "horario": input("Horario (ej. Lunes 08:00): "),
        "instructor": input("Instructor: "),
        "cupos_maximos": input("Cupos máximos (Enter para 15 por defecto): ")
    }
    mostrar_resultado(*clases.crear(datos))
    pausa()

def listar_clases():
    imprimir_titulo("LISTA DE CLASES GRUPALES")
    mostrar_lista(clases.leer(), "No hay clases registradas.")
    pausa()

def buscar_clase():
    imprimir_titulo("BUSCAR CLASE")
    termino = input("Nombre o instructor: ")
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
    for campo in ("nombre_clase", "horario", "instructor", "cupos_maximos"):
        actual = getattr(c, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
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
# MENÚ INSCRIPCIONES
# =====================================================================
def registrar_inscripcion():
    imprimir_titulo("INSCRIBIR SOCIO A CLASE")
    imprimir_info("Socios:")
    mostrar_lista(socios.leer())
    imprimir_info("Clases Grupales:")
    mostrar_lista(clases.leer())

    soc_id = pedir_entero("\nId del socio: ")
    cls_id = pedir_entero("Id de la clase: ")

    datos = {
        "socio_id": soc_id,
        "clase_id": cls_id
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

def resumen_gimnasio():
    imprimir_titulo("RESUMEN DE GIMNASIO")
    print(f"  Socios registrados     : {len(socios.leer())}")
    print(f"  Clases grupales activas: {len(clases.leer())}")
    sin_cupos = clases.clases_sin_cupo()
    print(f"  Clases llenas          : {', '.join(c.nombre_clase for c in sin_cupos) or 'ninguna'}")
    print(f"  Total de inscripciones : {len(inscripciones.leer())}")
    pausa()


# =====================================================================
# CONFIGURACIÓN DE MENÚS (Diccionarios)
# =====================================================================
MENU_SOCIOS = {
    "1": ("Registrar socio", crear_socio),
    "2": ("Ver todos", listar_socios),
    "3": ("Buscar", buscar_socio),
    "4": ("Ver por id", ver_socio),
    "5": ("Actualizar", actualizar_socio),
    "6": ("Eliminar", eliminar_socio),
    "0": ("Volver", None),
}

MENU_CLASES = {
    "1": ("Registrar clase", crear_clase),
    "2": ("Ver todas", listar_clases),
    "3": ("Buscar", buscar_clase),
    "4": ("Ver por id", ver_clase),
    "5": ("Actualizar", actualizar_clase),
    "6": ("Eliminar", eliminar_clase),
    "0": ("Volver", None),
}

MENU_INSCRIPCIONES = {
    "1": ("Inscribir a clase", registrar_inscripcion),
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
        imprimir_titulo("SISTEMA DE GIMNASIO FITNESS")
        print("  1. Socios")
        print("  2. Clases Grupales")
        print("  3. Inscripciones")
        print("  4. Resumen")
        print("  0. Salir\n")

        tecla = input("Opción: ").strip()
        if tecla == "1": ejecutar_menu("SOCIOS", MENU_SOCIOS)
        elif tecla == "2": ejecutar_menu("CLASES GRUPALES", MENU_CLASES)
        elif tecla == "3": ejecutar_menu("INSCRIPCIONES", MENU_INSCRIPCIONES)
        elif tecla == "4": resumen_gimnasio()
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