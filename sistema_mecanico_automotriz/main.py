from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import PropietarioAutoController, ServicioTallerController, OrdenReparacionController

propietarios = PropietarioAutoController()
servicios = ServicioTallerController()
ordenes = OrdenReparacionController(propietarios, servicios)


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
# FUNCIONES DE PROPIETARIOS
# =====================================================================
def crear_propietario():
    imprimir_titulo("REGISTRAR PROPIETARIO")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "cedula": input("Cédula: "),
        "telefono": input("Teléfono: ")
    }
    mostrar_resultado(*propietarios.crear(datos))
    pausa()

def listar_propietarios():
    imprimir_titulo("LISTA DE PROPIETARIOS")
    mostrar_lista(propietarios.leer(), "No hay propietarios registrados.")
    pausa()

def buscar_propietario():
    imprimir_titulo("BUSCAR PROPIETARIO")
    termino = input("Nombre, apellido o cédula: ")
    mostrar_lista(propietarios.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_propietario():
    imprimir_titulo("VER PROPIETARIO POR ID")
    p = propietarios.obtener(pedir_entero("Id: "))
    if not p: imprimir_error("No encontrado")
    else: mostrar_detalle(p)
    pausa()

def actualizar_propietario():
    imprimir_titulo("ACTUALIZAR PROPIETARIO")
    id_p = pedir_entero("Id: ")
    p = propietarios.obtener(id_p)
    if not p:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("nombre", "apellido", "email", "cedula", "telefono"):
        actual = getattr(p, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*propietarios.actualizar(id_p, cambios))
    pausa()

def eliminar_propietario():
    imprimir_titulo("ELIMINAR PROPIETARIO")
    id_p = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este propietario?"):
        mostrar_resultado(*propietarios.eliminar(id_p))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# FUNCIONES DE SERVICIOS
# =====================================================================
def crear_servicio():
    imprimir_titulo("REGISTRAR SERVICIO DE TALLER")
    datos = {
        "nombre_servicio": input("Nombre del servicio (ej. Afinamiento): "),
        "codigo": input("Código (ej. SERV01): "),
        "costo_repuestos": input("Costo de repuestos ($): ")
    }
    mostrar_resultado(*servicios.crear(datos))
    pausa()

def listar_servicios():
    imprimir_titulo("CATÁLOGO DE SERVICIOS")
    mostrar_lista(servicios.leer(), "No hay servicios registrados.")
    pausa()

def buscar_servicio():
    imprimir_titulo("BUSCAR SERVICIO")
    termino = input("Nombre o código: ")
    mostrar_lista(servicios.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_servicio():
    imprimir_titulo("VER SERVICIO POR ID")
    s = servicios.obtener(pedir_entero("Id: "))
    if not s: imprimir_error("No encontrado")
    else: mostrar_detalle(s)
    pausa()

def actualizar_servicio():
    imprimir_titulo("ACTUALIZAR SERVICIO")
    id_s = pedir_entero("Id: ")
    s = servicios.obtener(id_s)
    if not s:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("nombre_servicio", "codigo", "costo_repuestos"):
        actual = getattr(s, campo)
        nuevo = input(f"{campo.replace('_', ' ').capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*servicios.actualizar(id_s, cambios))
    pausa()

def eliminar_servicio():
    imprimir_titulo("ELIMINAR SERVICIO")
    id_s = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este servicio?"):
        mostrar_resultado(*servicios.eliminar(id_s))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# FUNCIONES DE ÓRDENES
# =====================================================================
def registrar_orden():
    imprimir_titulo("GENERAR ORDEN DE REPARACIÓN")
    imprimir_info("Propietarios:")
    mostrar_lista(propietarios.leer())
    imprimir_info("Servicios disponibles:")
    mostrar_lista(servicios.leer())

    prop_id = pedir_entero("\nId del propietario: ")
    serv_id = pedir_entero("Id del servicio: ")
    placa = input("Placa del vehículo (ej. ABC-1234): ")
    urg_extra = float(input("Cargo por urgencia extra ($) [0 si no aplica]: ") or 0.0)

    datos = {
        "propietario_id": prop_id,
        "servicio_id": serv_id,
        "placa_vehiculo": placa,
        "urgencia_extra": urg_extra
    }
    mostrar_resultado(*ordenes.crear(datos))
    pausa()

def listar_ordenes():
    imprimir_titulo("LISTA DE ÓRDENES DE REPARACIÓN")
    mostrar_lista(ordenes.leer(), "No hay órdenes registradas.")
    pausa()

def ver_comprobante_orden():
    imprimir_titulo("COMPROBANTE DE ORDEN")
    texto = ordenes.comprobante_orden(pedir_entero("Id de la orden: "))
    if not texto: imprimir_error("No existe esa orden")
    else: print(texto)
    pausa()

def cancelar_orden():
    imprimir_titulo("CANCELAR ORDEN")
    id_o = pedir_entero("Id de la orden: ")
    if id_o and confirmar("¿Confirma cancelar esta orden de reparación?"):
        mostrar_resultado(*ordenes.eliminar(id_o))
    else:
        imprimir_info("Operación cancelada")
    pausa()

def resumen_taller():
    imprimir_titulo("RESUMEN TALLER MECÁNICO")
    print(f"  Propietarios registrados: {len(propietarios.leer())}")
    print(f"  Servicios en catálogo   : {len(servicios.leer())}")
    print(f"  Órdenes emitidas        : {len(ordenes.leer())}")
    print(f"  Total recaudado         : ${ordenes.total_recaudado():.2f}")
    pausa()


# =====================================================================
# CONFIGURACIÓN DE MENÚS
# =====================================================================
MENU_PROPIETARIOS = {
    "1": ("Registrar propietario", crear_propietario),
    "2": ("Ver todos", listar_propietarios),
    "3": ("Buscar", buscar_propietario),
    "4": ("Ver por id", ver_propietario),
    "5": ("Actualizar", actualizar_propietario),
    "6": ("Eliminar", eliminar_propietario),
    "0": ("Volver", None),
}

MENU_SERVICIOS = {
    "1": ("Registrar servicio", crear_servicio),
    "2": ("Ver catálogo", listar_servicios),
    "3": ("Buscar", buscar_servicio),
    "4": ("Ver por id", ver_servicio),
    "5": ("Actualizar", actualizar_servicio),
    "6": ("Eliminar", eliminar_servicio),
    "0": ("Volver", None),
}

MENU_ORDENES = {
    "1": ("Generar orden", registrar_orden),
    "2": ("Ver órdenes", listar_ordenes),
    "3": ("Ver comprobante", ver_comprobante_orden),
    "4": ("Cancelar orden", cancelar_orden),
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
        imprimir_titulo("SISTEMA DE TALLER MECÁNICO")
        print("  1. Propietarios")
        print("  2. Servicios")
        print("  3. Órdenes de Reparación")
        print("  4. Resumen")
        print("  0. Salir\n")

        tecla = input("Opción: ").strip()
        if tecla == "1": ejecutar_menu("PROPIETARIOS", MENU_PROPIETARIOS)
        elif tecla == "2": ejecutar_menu("SERVICIOS", MENU_SERVICIOS)
        elif tecla == "3": ejecutar_menu("ÓRDENES", MENU_ORDENES)
        elif tecla == "4": resumen_taller()
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