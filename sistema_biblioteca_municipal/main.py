from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import LectorController, LibroController, PrestamoController

lectores = LectorController()
libros = LibroController()
prestamos = PrestamoController(lectores, libros)


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
# MENÚ LECTORES
# =====================================================================
def crear_lector():
    imprimir_titulo("REGISTRAR LECTOR")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "codigo_lector": input("Código de lector (ej. LEC001): "),
        "telefono": input("Teléfono: ")
    }
    mostrar_resultado(*lectores.crear(datos))
    pausa()

def listar_lectores():
    imprimir_titulo("LISTA DE LECTORES")
    mostrar_lista(lectores.leer(), "No hay lectores registrados.")
    pausa()

def buscar_lector():
    imprimir_titulo("BUSCAR LECTOR")
    termino = input("Nombre, apellido o código: ")
    mostrar_lista(lectores.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_lector():
    imprimir_titulo("VER LECTOR POR ID")
    l = lectores.obtener(pedir_entero("Id: "))
    if not l: imprimir_error("No encontrado")
    else: mostrar_detalle(l)
    pausa()

def actualizar_lector():
    imprimir_titulo("ACTUALIZAR LECTOR")
    id_l = pedir_entero("Id: ")
    l = lectores.obtener(id_l)
    if not l:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("nombre", "apellido", "email", "codigo_lector", "telefono"):
        actual = getattr(l, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*lectores.actualizar(id_l, cambios))
    pausa()

def eliminar_lector():
    imprimir_titulo("ELIMINAR LECTOR")
    id_l = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este lector?"):
        mostrar_resultado(*lectores.eliminar(id_l))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ LIBROS
# =====================================================================
def crear_libro():
    imprimir_titulo("REGISTRAR LIBRO")
    datos = {
        "titulo": input("Título del libro: "),
        "isbn": input("ISBN: "),
        "autor": input("Autor: "),
        "ejemplares_disponibles": input("Ejemplares (Enter para 1 por defecto): ")
    }
    mostrar_resultado(*libros.crear(datos))
    pausa()

def listar_libros():
    imprimir_titulo("CATÁLOGO DE LIBROS")
    mostrar_lista(libros.leer(), "No hay libros registrados.")
    pausa()

def buscar_libro():
    imprimir_titulo("BUSCAR LIBRO")
    termino = input("Título, autor o ISBN: ")
    mostrar_lista(libros.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_libro():
    imprimir_titulo("VER LIBRO POR ID")
    lib = libros.obtener(pedir_entero("Id: "))
    if not lib: imprimir_error("No encontrado")
    else: mostrar_detalle(lib)
    pausa()

def actualizar_libro():
    imprimir_titulo("ACTUALIZAR LIBRO")
    id_lib = pedir_entero("Id: ")
    lib = libros.obtener(id_lib)
    if not lib:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("titulo", "isbn", "autor", "ejemplares_disponibles"):
        actual = getattr(lib, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*libros.actualizar(id_lib, cambios))
    pausa()

def eliminar_libro():
    imprimir_titulo("ELIMINAR LIBRO")
    id_lib = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este libro?"):
        mostrar_resultado(*libros.eliminar(id_lib))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ PRÉSTAMOS
# =====================================================================
def registrar_prestamo():
    imprimir_titulo("REGISTRAR PRÉSTAMO")
    imprimir_info("Lectores:")
    mostrar_lista(lectores.leer())
    imprimir_info("Libros:")
    mostrar_lista(libros.leer())

    lec_id = pedir_entero("\nId del lector: ")
    lib_id = pedir_entero("Id del libro: ")

    datos = {
        "lector_id": lec_id,
        "libro_id": lib_id
    }
    mostrar_resultado(*prestamos.crear(datos))
    pausa()

def listar_prestamos():
    imprimir_titulo("LISTA DE PRÉSTAMOS")
    mostrar_lista(prestamos.leer(), "No hay préstamos registrados.")
    pausa()

def registrar_devolucion_libro():
    imprimir_titulo("REGISTRAR DEVOLUCIÓN")
    mostrar_lista(prestamos.leer())
    id_p = pedir_entero("\nId del préstamo a devolver: ")
    mostrar_resultado(*prestamos.registrar_devolucion(id_p))
    pausa()

def ver_comprobante_prestamo():
    imprimir_titulo("COMPROBANTE DE PRÉSTAMO")
    texto = prestamos.comprobante_prestamo(pedir_entero("Id del préstamo: "))
    if not texto: imprimir_error("No existe ese préstamo")
    else: print(texto)
    pausa()

def resumen_biblioteca():
    imprimir_titulo("RESUMEN DE BIBLIOTECA")
    print(f"  Lectores registrados : {len(lectores.leer())}")
    print(f"  Libros en catálogo   : {len(libros.leer())}")
    sin_stock = libros.libros_sin_ejemplares()
    print(f"  Libros agotados      : {', '.join(l.titulo for l in sin_stock) or 'ninguno'}")
    print(f"  Préstamos totales    : {len(prestamos.leer())}")
    activos = sum(1 for p in prestamos.leer() if p.estado == "Activo")
    print(f"  Préstamos activos    : {activos}")
    pausa()


# =====================================================================
# CONFIGURACIÓN DE MENÚS (Diccionarios)
# =====================================================================
MENU_LECTORES = {
    "1": ("Registrar lector", crear_lector),
    "2": ("Ver todos", listar_lectores),
    "3": ("Buscar", buscar_lector),
    "4": ("Ver por id", ver_lector),
    "5": ("Actualizar", actualizar_lector),
    "6": ("Eliminar", eliminar_lector),
    "0": ("Volver", None),
}

MENU_LIBROS = {
    "1": ("Registrar libro", crear_libro),
    "2": ("Ver catálogo", listar_libros),
    "3": ("Buscar", buscar_libro),
    "4": ("Ver por id", ver_libro),
    "5": ("Actualizar", actualizar_libro),
    "6": ("Eliminar", eliminar_libro),
    "0": ("Volver", None),
}

MENU_PRESTAMOS = {
    "1": ("Registrar préstamo", registrar_prestamo),
    "2": ("Ver todos los préstamos", listar_prestamos),
    "3": ("Registrar devolución", registrar_devolucion_libro),
    "4": ("Ver comprobante", ver_comprobante_prestamo),
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
        imprimir_titulo("SISTEMA BIBLIOTECA MUNICIPAL")
        print("  1. Lectores")
        print("  2. Libros")
        print("  3. Préstamos")
        print("  4. Resumen")
        print("  0. Salir\n")

        tecla = input("Opción: ").strip()
        if tecla == "1": ejecutar_menu("LECTORES", MENU_LECTORES)
        elif tecla == "2": ejecutar_menu("LIBROS", MENU_LIBROS)
        elif tecla == "3": ejecutar_menu("PRÉSTAMOS", MENU_PRESTAMOS)
        elif tecla == "4": resumen_biblioteca()
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