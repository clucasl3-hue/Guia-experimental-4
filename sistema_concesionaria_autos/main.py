from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import CompradorController, VehiculoController, VentaVehiculoController

compradores = CompradorController()
vehiculos = VehiculoController()
ventas = VentaVehiculoController(compradores, vehiculos)


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
# MENÚ COMPRADORES
# =====================================================================
def crear_comprador():
    imprimir_titulo("REGISTRAR COMPRADOR")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "cedula": input("Cédula: "),
        "presupuesto": input("Presupuesto estimado ($): ")
    }
    mostrar_resultado(*compradores.crear(datos))
    pausa()

def listar_compradores():
    imprimir_titulo("LISTA DE COMPRADORES")
    mostrar_lista(compradores.leer(), "No hay compradores registrados.")
    pausa()

def buscar_comprador():
    imprimir_titulo("BUSCAR COMPRADOR")
    termino = input("Nombre, apellido o cédula: ")
    mostrar_lista(compradores.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_comprador():
    imprimir_titulo("VER COMPRADOR POR ID")
    c = compradores.obtener(pedir_entero("Id: "))
    if not c: imprimir_error("No encontrado")
    else: mostrar_detalle(c)
    pausa()

def actualizar_comprador():
    imprimir_titulo("ACTUALIZAR COMPRADOR")
    id_c = pedir_entero("Id: ")
    c = compradores.obtener(id_c)
    if not c:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("nombre", "apellido", "email", "cedula", "presupuesto"):
        actual = getattr(c, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*compradores.actualizar(id_c, cambios))
    pausa()

def eliminar_comprador():
    imprimir_titulo("ELIMINAR COMPRADOR")
    id_c = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este comprador?"):
        mostrar_resultado(*compradores.eliminar(id_c))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ VEHÍCULOS
# =====================================================================
def crear_vehiculo():
    imprimir_titulo("REGISTRAR VEHÍCULO")
    print(f"Marcas permitidas: {', '.join(__import__('models').Vehiculo.MARCAS_PERMITIDAS)}")
    datos = {
        "marca": input("Marca: "),
        "modelo": input("Modelo: "),
        "anio": input("Año: "),
        "precio_base": input("Precio base ($): "),
        "stock": input("Stock (Enter para 1): ")
    }
    mostrar_resultado(*vehiculos.crear(datos))
    pausa()

def listar_vehiculos():
    imprimir_titulo("INVENTARIO DE VEHÍCULOS")
    mostrar_lista(vehiculos.leer(), "No hay vehículos registrados.")
    pausa()

def buscar_vehiculo():
    imprimir_titulo("BUSCAR VEHÍCULO")
    termino = input("Marca o modelo: ")
    mostrar_lista(vehiculos.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_vehiculo():
    imprimir_titulo("VER VEHÍCULO POR ID")
    v = vehiculos.obtener(pedir_entero("Id: "))
    if not v: imprimir_error("No encontrado")
    else: mostrar_detalle(v)
    pausa()

def actualizar_vehiculo():
    imprimir_titulo("ACTUALIZAR VEHÍCULO")
    id_v = pedir_entero("Id: ")
    v = vehiculos.obtener(id_v)
    if not v:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("marca", "modelo", "anio", "precio_base", "stock"):
        actual = getattr(v, campo)
        nuevo = input(f"{campo.replace('_', ' ').capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*vehiculos.actualizar(id_v, cambios))
    pausa()

def eliminar_vehiculo():
    imprimir_titulo("ELIMINAR VEHÍCULO")
    id_v = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este vehículo?"):
        mostrar_resultado(*vehiculos.eliminar(id_v))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ VENTAS DE VEHÍCULOS
# =====================================================================
def registrar_venta():
    imprimir_titulo("REGISTRAR VENTA DE VEHÍCULO")
    imprimir_info("Compradores:")
    mostrar_lista(compradores.leer())
    imprimir_info("Vehículos en stock:")
    mostrar_lista(vehiculos.vehiculos_disponibles(), "No hay vehículos disponibles.")

    com_id = pedir_entero("\nId del comprador: ")
    veh_id = pedir_entero("Id del vehículo: ")

    datos = {
        "comprador_id": com_id,
        "vehiculo_id": veh_id
    }
    mostrar_resultado(*ventas.crear(datos))
    pausa()

def listar_ventas():
    imprimir_titulo("REGISTRO DE VENTAS")
    mostrar_lista(ventas.leer(), "No hay ventas registradas.")
    pausa()

def ver_factura_venta():
    imprimir_titulo("FACTURA DE VENTA")
    texto = ventas.factura_venta(pedir_entero("Id de la venta: "))
    if not texto: imprimir_error("No existe esa venta")
    else: print(texto)
    pausa()

def cancelar_venta():
    imprimir_titulo("ANULAR VENTA")
    id_v = pedir_entero("Id de la venta: ")
    if id_v and confirmar("¿Confirma anular esta venta?"):
        mostrar_resultado(*ventas.eliminar(id_v))
    else:
        imprimir_info("Operación cancelada")
    pausa()

def resumen_concesionaria():
    imprimir_titulo("RESUMEN CONCESIONARIA DE AUTOS")
    print(f"  Compradores registrados : {len(compradores.leer())}")
    print(f"  Modelos en catálogo     : {len(vehiculos.leer())}")
    print(f"  Ventas totales realizadas: {len(ventas.leer())}")
    print(f"  Total recaudado         : ${ventas.total_recaudado():...2f}" if hasattr(ventas, 'total_recaudado') else "")
    pausa()


# =====================================================================
# CONFIGURACIÓN DE MENÚS (Diccionarios)
# =====================================================================
MENU_COMPRADORES = {
    "1": ("Registrar comprador", crear_comprador),
    "2": ("Ver todos", listar_compradores),
    "3": ("Buscar", buscar_comprador),
    "4": ("Ver por id", ver_comprador),
    "5": ("Actualizar", actualizar_comprador),
    "6": ("Eliminar", eliminar_comprador),
    "0": ("Volver", None),
}

MENU_VEHICULOS = {
    "1": ("Registrar vehículo", crear_vehiculo),
    "2": ("Ver inventario", listar_vehiculos),
    "3": ("Buscar", buscar_vehiculo),
    "4": ("Ver por id", ver_vehiculo),
    "5": ("Actualizar", actualizar_vehiculo),
    "6": ("Eliminar", eliminar_vehiculo),
    "0": ("Volver", None),
}

MENU_VENTAS = {
    "1": ("Registrar venta", registrar_venta),
    "2": ("Ver ventas", listar_ventas),
    "3": ("Ver factura", ver_factura_venta),
    "4": ("Anular venta", cancelar_venta),
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
        imprimir_titulo("SISTEMA CONCESIONARIA DE AUTOS")
        print("  1. Compradores")
        print("  2. Vehículos")
        print("  3. Ventas")
        print("  4. Resumen")
        print("  0. Salir\n")

        tecla = input("Opción: ").strip()
        if tecla == "1": ejecutar_menu("COMPRADORES", MENU_COMPRADORES)
        elif tecla == "2": ejecutar_menu("VEHÍCULOS", MENU_VEHICULOS)
        elif tecla == "3": ejecutar_menu("VENTAS", MENU_VENTAS)
        elif tecla == "4": resumen_concesionaria()
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