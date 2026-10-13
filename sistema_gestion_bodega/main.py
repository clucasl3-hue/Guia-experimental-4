from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import ProveedorController, ProductoBodegaController, MovimientoStockController

proveedores = ProveedorController()
productos = ProductoBodegaController()
movimientos = MovimientoStockController(proveedores, productos)


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
# FUNCIONES DE PROVEEDORES
# =====================================================================
def crear_proveedor():
    imprimir_titulo("REGISTRAR PROVEEDOR")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "ruc": input("RUC: "),
        "telefono": input("Teléfono: ")
    }
    mostrar_resultado(*proveedores.crear(datos))
    pausa()

def listar_proveedores():
    imprimir_titulo("LISTA DE PROVEEDORES")
    mostrar_lista(proveedores.leer(), "No hay proveedores registrados.")
    pausa()

def buscar_proveedor():
    imprimir_titulo("BUSCAR PROVEEDOR")
    termino = input("Nombre, apellido o RUC: ")
    mostrar_lista(proveedores.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_proveedor():
    imprimir_titulo("VER PROVEEDOR POR ID")
    p = proveedores.obtener(pedir_entero("Id: "))
    if not p: imprimir_error("No encontrado")
    else: mostrar_detalle(p)
    pausa()

def actualizar_proveedor():
    imprimir_titulo("ACTUALIZAR PROVEEDOR")
    id_p = pedir_entero("Id: ")
    p = proveedores.obtener(id_p)
    if not p:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("nombre", "apellido", "email", "ruc", "telefono"):
        actual = getattr(p, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*proveedores.actualizar(id_p, cambios))
    pausa()

def eliminar_proveedor():
    imprimir_titulo("ELIMINAR PROVEEDOR")
    id_p = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este proveedor?"):
        mostrar_resultado(*proveedores.eliminar(id_p))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# FUNCIONES DE PRODUCTOS
# =====================================================================
def crear_producto():
    imprimir_titulo("REGISTRAR PRODUCTO EN BODEGA")
    datos = {
        "sku": input("SKU / Código (ej. PROD-001): "),
        "nombre_producto": input("Nombre del producto: "),
        "stock_actual": input("Stock inicial: "),
        "precio_costo": input("Precio de costo ($): ")
    }
    mostrar_resultado(*productos.crear(datos))
    pausa()

def listar_productos():
    imprimir_titulo("INVENTARIO DE PRODUCTOS")
    mostrar_lista(productos.leer(), "No hay productos registrados.")
    pausa()

def buscar_producto():
    imprimir_titulo("BUSCAR PRODUCTO")
    termino = input("SKU o nombre: ")
    mostrar_lista(productos.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_producto():
    imprimir_titulo("VER PRODUCTO POR ID")
    p = productos.obtener(pedir_entero("Id: "))
    if not p: imprimir_error("No encontrado")
    else: mostrar_detalle(p)
    pausa()

def actualizar_producto():
    imprimir_titulo("ACTUALIZAR PRODUCTO")
    id_p = pedir_entero("Id: ")
    p = productos.obtener(id_p)
    if not p:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("sku", "nombre_producto", "stock_actual", "precio_costo"):
        actual = getattr(p, campo)
        nuevo = input(f"{campo.replace('_', ' ').capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*productos.actualizar(id_p, cambios))
    pausa()

def eliminar_producto():
    imprimir_titulo("ELIMINAR PRODUCTO")
    id_p = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este producto?"):
        mostrar_resultado(*productos.eliminar(id_p))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# FUNCIONES DE MOVIMIENTOS
# =====================================================================
def registrar_movimiento():
    imprimir_titulo("REGISTRAR MOVIMIENTO DE STOCK")
    imprimir_info("Proveedores:")
    mostrar_lista(proveedores.leer())
    imprimir_info("Productos en inventario:")
    mostrar_lista(productos.leer(), "No hay productos.")

    prov_id = pedir_entero("\nId del proveedor: ")
    prod_id = pedir_entero("Id del producto: ")
    tipo = input("Tipo de movimiento (Entrada / Salida): ")
    cant = pedir_entero("Cantidad: ")

    datos = {
        "proveedor_id": prov_id,
        "producto_id": prod_id,
        "tipo_movimiento": tipo,
        "cantidad": cant
    }
    mostrar_resultado(*movimientos.crear(datos))
    pausa()

def listar_movimientos():
    imprimir_titulo("HISTORIAL DE MOVIMIENTOS")
    mostrar_lista(movimientos.leer(), "No hay movimientos registrados.")
    pausa()

def ver_comprobante_movimiento():
    imprimir_titulo("COMPROBANTE DE MOVIMIENTO")
    texto = movimientos.comprobante_movimiento(pedir_entero("Id del movimiento: "))
    if not texto: imprimir_error("No existe ese movimiento")
    else: print(texto)
    pausa()

def cancelar_movimiento():
    imprimir_titulo("ELIMINAR / REVERTIR MOVIMIENTO")
    id_m = pedir_entero("Id del movimiento: ")
    if id_m and confirmar("¿Confirma eliminar este movimiento y revertir el stock?"):
        mostrar_resultado(*movimientos.eliminar(id_m))
    else:
        imprimir_info("Operación cancelada")
    pausa()

def resumen_bodega():
    imprimir_titulo("RESUMEN SISTEMA DE BODEGA")
    print(f"  Proveedores registrados : {len(proveedores.leer())}")
    print(f"  Productos en catálogo   : {len(productos.leer())}")
    print(f"  Movimientos totales     : {len(movimientos.leer())}")
    print(f"  Total invertido (Entradas): ${movimientos.total_invertido():.2f}")
    pausa()


# =====================================================================
# CONFIGURACIÓN DE MENÚS
# =====================================================================
MENU_PROVEEDORES = {
    "1": ("Registrar proveedor", crear_proveedor),
    "2": ("Ver todos", listar_proveedores),
    "3": ("Buscar", buscar_proveedor),
    "4": ("Ver por id", ver_proveedor),
    "5": ("Actualizar", actualizar_proveedor),
    "6": ("Eliminar", eliminar_proveedor),
    "0": ("Volver", None),
}

MENU_PRODUCTOS = {
    "1": ("Registrar producto", crear_producto),
    "2": ("Ver inventario", listar_productos),
    "3": ("Buscar", buscar_producto),
    "4": ("Ver por id", ver_producto),
    "5": ("Actualizar", actualizar_producto),
    "6": ("Eliminar", eliminar_producto),
    "0": ("Volver", None),
}

MENU_MOVIMIENTOS = {
    "1": ("Registrar movimiento", registrar_movimiento),
    "2": ("Ver historial", listar_movimientos),
    "3": ("Ver comprobante", ver_comprobante_movimiento),
    "4": ("Revertir/Eliminar movimiento", cancelar_movimiento),
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
        imprimir_titulo("SISTEMA DE BODEGA E INVENTARIO")
        print("  1. Proveedores")
        print("  2. Productos")
        print("  3. Movimientos de Stock")
        print("  4. Resumen")
        print("  0. Salir\n")

        tecla = input("Opción: ").strip()
        if tecla == "1": ejecutar_menu("PROVEEDORES", MENU_PROVEEDORES)
        elif tecla == "2": ejecutar_menu("PRODUCTOS", MENU_PRODUCTOS)
        elif tecla == "3": ejecutar_menu("MOVIMIENTOS", MENU_MOVIMIENTOS)
        elif tecla == "4": resumen_bodega()
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