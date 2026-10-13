from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import ClienteCineController, PeliculaController, BoletoController

clientes = ClienteCineController()
peliculas = PeliculaController()
boletos = BoletoController(clientes, peliculas)


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
# MENÚ CLIENTES CINE
# =====================================================================
def crear_cliente():
    imprimir_titulo("REGISTRAR CLIENTE")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "tarjeta_fidelidad": input("Tarjeta fidelidad (opcional): ")
    }
    mostrar_resultado(*clientes.crear(datos))
    pausa()

def listar_clientes():
    imprimir_titulo("LISTA DE CLIENTES")
    mostrar_lista(clientes.leer(), "No hay clientes registrados.")
    pausa()

def buscar_cliente():
    imprimir_titulo("BUSCAR CLIENTE")
    termino = input("Nombre, apellido o tarjeta: ")
    mostrar_lista(clientes.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_cliente():
    imprimir_titulo("VER CLIENTE POR ID")
    c = clientes.obtener(pedir_entero("Id: "))
    if not c: imprimir_error("No encontrado")
    else: mostrar_detalle(c)
    pausa()

def actualizar_cliente():
    imprimir_titulo("ACTUALIZAR CLIENTE")
    id_c = pedir_entero("Id: ")
    c = clientes.obtener(id_c)
    if not c:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("nombre", "apellido", "email", "tarjeta_fidelidad"):
        actual = getattr(c, campo)
        nuevo = input(f"{campo.replace('_', ' ').capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*clientes.actualizar(id_c, cambios))
    pausa()

def eliminar_cliente():
    imprimir_titulo("ELIMINAR CLIENTE")
    id_c = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este cliente?"):
        mostrar_resultado(*clientes.eliminar(id_c))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ PELÍCULAS
# =====================================================================
def crear_pelicula():
    imprimir_titulo("REGISTRAR PELÍCULA")
    datos = {
        "titulo": input("Título: "),
        "genero": input("Género: "),
        "duracion_min": input("Duración en minutos: "),
        "asientos_disponibles": input("Asientos (Enter para 50 por defecto): ")
    }
    mostrar_resultado(*peliculas.crear(datos))
    pausa()

def listar_peliculas():
    imprimir_titulo("CARTELERA DE PELÍCULAS")
    mostrar_lista(peliculas.leer(), "No hay películas registradas.")
    pausa()

def buscar_pelicula():
    imprimir_titulo("BUSCAR PELÍCULA")
    termino = input("Título o género: ")
    mostrar_lista(peliculas.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_pelicula():
    imprimir_titulo("VER PELÍCULA POR ID")
    p = peliculas.obtener(pedir_entero("Id: "))
    if not p: imprimir_error("No encontrado")
    else: mostrar_detalle(p)
    pausa()

def actualizar_pelicula():
    imprimir_titulo("ACTUALIZAR PELÍCULA")
    id_p = pedir_entero("Id: ")
    p = peliculas.obtener(id_p)
    if not p:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("titulo", "genero", "duracion_min", "asientos_disponibles"):
        actual = getattr(p, campo)
        nuevo = input(f"{campo.replace('_', ' ').capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*peliculas.actualizar(id_p, cambios))
    pausa()

def eliminar_pelicula():
    imprimir_titulo("ELIMINAR PELÍCULA")
    id_p = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar esta película?"):
        mostrar_resultado(*peliculas.eliminar(id_p))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ BOLETOS
# =====================================================================
def comprar_boletos():
    imprimir_titulo("COMPRAR BOLETOS DE CINE")
    imprimir_info("Clientes:")
    mostrar_lista(clientes.leer())
    imprimir_info("Cartelera disponible:")
    mostrar_lista(peliculas.peliculas_con_espacio(), "No hay películas con asientos.")

    cli_id = pedir_entero("\nId del cliente: ")
    pel_id = pedir_entero("Id de la película: ")
    cant = pedir_entero("Cantidad de boletos: ")
    sala = input("Sala (Enter para Sala 1): ") or "Sala 1"

    datos = {
        "cliente_id": cli_id,
        "pelicula_id": pel_id,
        "cantidad_boletos": cant,
        "sala": sala
    }
    mostrar_resultado(*boletos.crear(datos))
    pausa()

def listar_boletos():
    imprimir_titulo("LISTA DE BOLETOS VENDIDOS")
    mostrar_lista(boletos.leer(), "No hay boletos vendidos.")
    pausa()

def ver_comprobante_boleto():
    imprimir_titulo("COMPROBANTE DE BOLETO")
    texto = boletos.comprobante_boleto(pedir_entero("Id del boleto: "))
    if not texto: imprimir_error("No existe ese boleto")
    else: print(texto)
    pausa()

def cancelar_boleto():
    imprimir_titulo("CANCELAR BOLETO")
    id_b = pedir_entero("Id del boleto: ")
    if id_b and confirmar("¿Confirma cancelar la compra de boletos?"):
        mostrar_resultado(*boletos.eliminar(id_b))
    else:
        imprimir_info("Operación cancelada")
    pausa()

def resumen_cine():
    imprimir_titulo("RESUMEN DE CINE")
    print(f"  Clientes registrados    : {len(clientes.leer())}")
    print(f"  Películas en cartelera  : {len(peliculas.leer())}")
    print(f"  Boletos emitidos        : {len(boletos.leer())}")
    print(f"  Total recaudado         : ${boletos.total_recaudado():.2f}")
    pausa()


# =====================================================================
# CONFIGURACIÓN DE MENÚS (Diccionarios)
# =====================================================================
MENU_CLIENTES = {
    "1": ("Registrar cliente", crear_cliente),
    "2": ("Ver todos", listar_clientes),
    "3": ("Buscar", buscar_cliente),
    "4": ("Ver por id", ver_cliente),
    "5": ("Actualizar", actualizar_cliente),
    "6": ("Eliminar", eliminar_cliente),
    "0": ("Volver", None),
}

MENU_PELICULAS = {
    "1": ("Registrar película", crear_pelicula),
    "2": ("Ver cartelera", listar_peliculas),
    "3": ("Buscar", buscar_pelicula),
    "4": ("Ver por id", ver_pelicula),
    "5": ("Actualizar", actualizar_pelicula),
    "6": ("Eliminar", eliminar_pelicula),
    "0": ("Volver", None),
}

MENU_BOLETOS = {
    "1": ("Comprar boletos", comprar_boletos),
    "2": ("Ver boletos", listar_boletos),
    "3": ("Ver comprobante", ver_comprobante_boleto),
    "4": ("Cancelar boletos", cancelar_boleto),
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
        imprimir_titulo("SISTEMA DE CINE - BOLETERÍA")
        print("  1. Clientes")
        print("  2. Películas")
        print("  3. Boletos")
        print("  4. Resumen")
        print("  0. Salir\n")

        tecla = input("Opción: ").strip()
        if tecla == "1": ejecutar_menu("CLIENTES", MENU_CLIENTES)
        elif tecla == "2": ejecutar_menu("PELÍCULAS", MENU_PELICULAS)
        elif tecla == "3": ejecutar_menu("BOLETOS", MENU_BOLETOS)
        elif tecla == "4": resumen_cine()
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