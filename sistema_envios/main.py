from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import RemitenteController, ZonaEnvioController, PaqueteEnvioController

remitentes = RemitenteController()
zonas = ZonaEnvioController()
paquetes = PaqueteEnvioController(remitentes, zonas)


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
# MENÚ REMITENTES
# =====================================================================
def crear_remitente():
    imprimir_titulo("REGISTRAR REMITENTE")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "ruc_cedula": input("RUC / Cédula: "),
        "telefono": input("Teléfono: ")
    }
    mostrar_resultado(*remitentes.crear(datos))
    pausa()

def listar_remitentes():
    imprimir_titulo("LISTA DE REMITENTES")
    mostrar_lista(remitentes.leer(), "No hay remitentes registrados.")
    pausa()

def buscar_remitente():
    imprimir_titulo("BUSCAR REMITENTE")
    termino = input("Nombre, apellido o RUC/Cédula: ")
    mostrar_lista(remitentes.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_remitente():
    imprimir_titulo("VER REMITENTE POR ID")
    r = remitentes.obtener(pedir_entero("Id: "))
    if not r: imprimir_error("No encontrado")
    else: mostrar_detalle(r)
    pausa()

def actualizar_remitente():
    imprimir_titulo("ACTUALIZAR REMITENTE")
    id_r = pedir_entero("Id: ")
    r = remitentes.obtener(id_r)
    if not r:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("nombre", "apellido", "email", "ruc_cedula", "telefono"):
        actual = getattr(r, campo)
        nuevo = input(f"{campo.replace('_', ' ').capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*remitentes.actualizar(id_r, cambios))
    pausa()

def eliminar_remitente():
    imprimir_titulo("ELIMINAR REMITENTE")
    id_r = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este remitente?"):
        mostrar_resultado(*remitentes.eliminar(id_r))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ ZONAS DE ENVÍO
# =====================================================================
def crear_zona():
    imprimir_titulo("REGISTRAR ZONA DE ENVÍO")
    datos = {
        "nombre_zona": input("Nombre de la zona (ej. Costa Norte): "),
        "codigo_postal": input("Código postal (ej. CP0901): "),
        "tarifa_base_kg": input("Tarifa base por kg ($): ")
    }
    mostrar_resultado(*zonas.crear(datos))
    pausa()

def listar_zonas():
    imprimir_titulo("CATÁLOGO DE ZONAS DE ENVÍO")
    mostrar_lista(zonas.leer(), "No hay zonas registradas.")
    pausa()

def buscar_zona():
    imprimir_titulo("BUSCAR ZONA")
    termino = input("Nombre de zona o código postal: ")
    mostrar_lista(zonas.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_zona():
    imprimir_titulo("VER ZONA POR ID")
    z = zonas.obtener(pedir_entero("Id: "))
    if not z: imprimir_error("No encontrado")
    else: mostrar_detalle(z)
    pausa()

def actualizar_zona():
    imprimir_titulo("ACTUALIZAR ZONA")
    id_z = pedir_entero("Id: ")
    z = zonas.obtener(id_z)
    if not z:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("nombre_zona", "codigo_postal", "tarifa_base_kg"):
        actual = getattr(z, campo)
        nuevo = input(f"{campo.replace('_', ' ').capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*zonas.actualizar(id_z, cambios))
    pausa()

def eliminar_zona():
    imprimir_titulo("ELIMINAR ZONA")
    id_z = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar esta zona?"):
        mostrar_resultado(*zonas.eliminar(id_z))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ PAQUETES / GUÍAS DE ENVÍO
# =====================================================================
def registrar_paquete():
    imprimir_titulo("GENERAR GUÍA DE ENVÍO")
    imprimir_info("Remitentes:")
    mostrar_lista(remitentes.leer())
    imprimir_info("Zonas disponibles:")
    mostrar_lista(zonas.leer())

    rem_id = pedir_entero("\nId del remitente: ")
    zon_id = pedir_entero("Id de la zona destino: ")
    peso = input("Peso en kg: ")
    desc = input("Descripción del contenido: ")

    datos = {
        "remitente_id": rem_id,
        "zona_id": zon_id,
        "peso_kg": peso,
        "descripcion": desc
    }
    mostrar_resultado(*paquetes.crear(datos))
    pausa()

def listar_paquetes():
    imprimir_titulo("LISTA DE ENVÍOS REALIZADOS")
    mostrar_lista(paquetes.leer(), "No hay paquetes registrados.")
    pausa()

def ver_comprobante_envio():
    imprimir_titulo("COMPROBANTE / GUÍA DE ENVÍO")
    texto = paquetes.comprobante_envio(pedir_entero("Id del paquete: "))
    if not texto: imprimir_error("No existe esa guía de envío")
    else: print(texto)
    pausa()

def cancelar_paquete():
    imprimir_titulo("CANCELAR ENVÍO")
    id_p = pedir_entero("Id del paquete: ")
    if id_p and confirmar("¿Confirma cancelar este envío?"):
        mostrar_resultado(*paquetes.eliminar(id_p))
    else:
        imprimir_info("Operación cancelada")
    pausa()

def resumen_courier():
    imprimir_titulo("RESUMEN DE SISTEMA DE COURIER / ENVÍOS")
    print(f"  Remitentes registrados : {len(remitentes.leer())}")
    print(f"  Zonas de envío activas : {len(zonas.leer())}")
    print(f"  Paquetes/Guías emitidos : {len(paquetes.leer())}")
    print(f"  Total recaudado        : ${paquetes.total_recaudado():.2f}")
    pausa()


# =====================================================================
# CONFIGURACIÓN DE MENÚS (Diccionarios)
# =====================================================================
MENU_REMITENTES = {
    "1": ("Registrar remitente", crear_remitente),
    "2": ("Ver todos", listar_remitentes),
    "3": ("Buscar", buscar_remitente),
    "4": ("Ver por id", ver_remitente),
    "5": ("Actualizar", actualizar_remitente),
    "6": ("Eliminar", eliminar_remitente),
    "0": ("Volver", None),
}

MENU_ZONAS = {
    "1": ("Registrar zona", crear_zona),
    "2": ("Ver todas", listar_zonas),
    "3": ("Buscar", buscar_zona),
    "4": ("Ver por id", ver_zona),
    "5": ("Actualizar", actualizar_zona),
    "6": ("Eliminar", eliminar_zona),
    "0": ("Volver", None),
}

MENU_PAQUETES = {
    "1": ("Generar guía de envío", registrar_paquete),
    "2": ("Ver guías/paquetes", listar_paquetes),
    "3": ("Ver comprobante", ver_comprobante_envio),
    "4": ("Cancelar envío", cancelar_paquete),
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
        imprimir_titulo("SISTEMA DE ENVÍOS / COURIER")
        print("  1. Remitentes")
        print("  2. Zonas de Envío")
        print("  3. Guías y Paquetes")
        print("  4. Resumen")
        print("  0. Salir\n")

        tecla = input("Opción: ").strip()
        if tecla == "1": ejecutar_menu("REMITENTES", MENU_REMITENTES)
        elif tecla == "2": ejecutar_menu("ZONAS DE ENVÍO", MENU_ZONAS)
        elif tecla == "3": ejecutar_menu("GUÍAS Y PAQUETES", MENU_PAQUETES)
        elif tecla == "4": resumen_courier()
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