from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import ComensalController, PlatilloMenuController, PedidoRestauranteController

comensales = ComensalController()
platillos = PlatilloMenuController()
pedidos = PedidoRestauranteController(comensales, platillos)


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
# FUNCIONES DE COMENSALES
# =====================================================================
def crear_comensal():
    imprimir_titulo("REGISTRAR COMENSAL")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "direccion": input("Dirección: "),
        "telefono": input("Teléfono: ")
    }
    mostrar_resultado(*comensales.crear(datos))
    pausa()

def listar_comensales():
    imprimir_titulo("LISTA DE COMENSALES")
    mostrar_lista(comensales.leer(), "No hay comensales registrados.")
    pausa()

def buscar_comensal():
    imprimir_titulo("BUSCAR COMENSAL")
    termino = input("Nombre, apellido o email: ")
    mostrar_lista(comensales.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_comensal():
    imprimir_titulo("VER COMENSAL POR ID")
    c = comensales.obtener(pedir_entero("Id: "))
    if not c: imprimir_error("No encontrado")
    else: mostrar_detalle(c)
    pausa()

def actualizar_comensal():
    imprimir_titulo("ACTUALIZAR COMENSAL")
    id_c = pedir_entero("Id: ")
    c = comensales.obtener(id_c)
    if not c:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("nombre", "apellido", "email", "direccion", "telefono"):
        actual = getattr(c, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*comensales.actualizar(id_c, cambios))
    pausa()

def eliminar_comensal():
    imprimir_titulo("ELIMINAR COMENSAL")
    id_c = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este comensal?"):
        mostrar_resultado(*comensales.eliminar(id_c))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# FUNCIONES DE PLATILLOS
# =====================================================================
def crear_platillo():
    imprimir_titulo("REGISTRAR PLATILLO")
    datos = {
        "nombre_platillo": input("Nombre del plato (ej. Lomo Saltado): "),
        "categoria": input("Categoría (ej. Plato Fuerte): "),
        "precio": input("Precio ($): ")
    }
    mostrar_resultado(*platillos.crear(datos))
    pausa()

def listar_platillos():
    imprimir_titulo("MENÚ DE PLATILLOS")
    mostrar_lista(platillos.leer(), "No hay platillos registrados.")
    pausa()

def buscar_platillo():
    imprimir_titulo("BUSCAR PLATILLO")
    termino = input("Nombre o categoría: ")
    mostrar_lista(platillos.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_platillo():
    imprimir_titulo("VER PLATILLO POR ID")
    p = platillos.obtener(pedir_entero("Id: "))
    if not p: imprimir_error("No encontrado")
    else: mostrar_detalle(p)
    pausa()

def actualizar_platillo():
    imprimir_titulo("ACTUALIZAR PLATILLO")
    id_p = pedir_entero("Id: ")
    p = platillos.obtener(id_p)
    if not p:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("nombre_platillo", "categoria", "precio"):
        actual = getattr(p, campo)
        nuevo = input(f"{campo.replace('_', ' ').capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*platillos.actualizar(id_p, cambios))
    pausa()

def eliminar_platillo():
    imprimir_titulo("ELIMINAR PLATILLO")
    id_p = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este platillo?"):
        mostrar_resultado(*platillos.eliminar(id_p))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# FUNCIONES DE PEDIDOS
# =====================================================================
def registrar_pedido():
    imprimir_titulo("REALIZAR PEDIDO / DELIVERY")
    imprimir_info("Comensales:")
    mostrar_lista(comensales.leer())
    imprimir_info("Menú disponible:")
    mostrar_lista(platillos.leer())

    com_id = pedir_entero("\nId del comensal: ")
    pla_id = pedir_entero("Id del platillo: ")
    cant = pedir_entero("Cantidad: ")
    con_deliv = confirmar("¿Incluir tarifa de envío a domicilio ($3.50)?")

    datos = {
        "comensal_id": com_id,
        "platillo_id": pla_id,
        "cantidad": cant,
        "con_delivery": con_deliv
    }
    mostrar_resultado(*pedidos.crear(datos))
    pausa()

def listar_pedidos():
    imprimir_titulo("LISTA DE PEDIDOS")
    mostrar_lista(pedidos.leer(), "No hay pedidos registrados.")
    pausa()

def ver_comprobante_pedido():
    imprimir_titulo("COMPROBANTE DE PEDIDO")
    texto = pedidos.comprobante_pedido(pedir_entero("Id del pedido: "))
    if not texto: imprimir_error("No existe ese pedido")
    else: print(texto)
    pausa()

def cancelar_pedido():
    imprimir_titulo("CANCELAR PEDIDO")
    id_ped = pedir_entero("Id del pedido: ")
    if id_ped and confirmar("¿Confirma cancelar este pedido?"):
        mostrar_resultado(*pedidos.eliminar(id_ped))
    else:
        imprimir_info("Operación cancelada")
    pausa()

def resumen_restaurante():
    imprimir_titulo("RESUMEN RESTAURANTE & DELIVERY")
    print(f"  Comensales registrados  : {len(comensales.leer())}")
    print(f"  Platillos en menú       : {len(platillos.leer())}")
    print(f"  Pedidos totales         : {len(pedidos.leer())}")
    print(f"  Total recaudado         : ${pedidos.total_recaudado():.2f}")
    pausa()


# =====================================================================
# CONFIGURACIÓN DE MENÚS
# =====================================================================
MENU_COMENSALES = {
    "1": ("Registrar comensal", crear_comensal),
    "2": ("Ver todos", listar_comensales),
    "3": ("Buscar", buscar_comensal),
    "4": ("Ver por id", ver_comensal),
    "5": ("Actualizar", actualizar_comensal),
    "6": ("Eliminar", eliminar_comensal),
    "0": ("Volver", None),
}

MENU_PLATILLOS = {
    "1": ("Registrar platillo", crear_platillo),
    "2": ("Ver menú", listar_platillos),
    "3": ("Buscar", buscar_platillo),
    "4": ("Ver por id", ver_platillo),
    "5": ("Actualizar", actualizar_platillo),
    "6": ("Eliminar", eliminar_platillo),
    "0": ("Volver", None),
}

MENU_PEDIDOS = {
    "1": ("Realizar pedido", registrar_pedido),
    "2": ("Ver pedidos", listar_pedidos),
    "3": ("Ver comprobante", ver_comprobante_pedido),
    "4": ("Cancelar pedido", cancelar_pedido),
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
        imprimir_titulo("SISTEMA DE RESTAURANTE - DELIVERY")
        print("  1. Comensales")
        print("  2. Platillos / Menú")
        print("  3. Pedidos")
        print("  4. Resumen")
        print("  0. Salir\n")

        tecla = input("Opción: ").strip()
        if tecla == "1": ejecutar_menu("COMENSALES", MENU_COMENSALES)
        elif tecla == "2": ejecutar_menu("PLATILLOS", MENU_PLATILLOS)
        elif tecla == "3": ejecutar_menu("PEDIDOS", MENU_PEDIDOS)
        elif tecla == "4": resumen_restaurante()
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