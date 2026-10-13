from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import InquilinoController, PropiedadController, ContratoAlquilerController

inquilinos = InquilinoController()
propiedades = PropiedadController()
contratos = ContratoAlquilerController(inquilinos, propiedades)


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
# FUNCIONES DE INQUILINOS
# =====================================================================
def crear_inquilino():
    imprimir_titulo("REGISTRAR INQUILINO")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "documento": input("Documento / Cédula: "),
        "telefono": input("Teléfono: ")
    }
    mostrar_resultado(*inquilinos.crear(datos))
    pausa()

def listar_inquilinos():
    imprimir_titulo("LISTA DE INQUILINOS")
    mostrar_lista(inquilinos.leer(), "No hay inquilinos registrados.")
    pausa()

def buscar_inquilino():
    imprimir_titulo("BUSCAR INQUILINO")
    termino = input("Nombre, apellido o documento: ")
    mostrar_lista(inquilinos.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_inquilino():
    imprimir_titulo("VER INQUILINO POR ID")
    i = inquilinos.obtener(pedir_entero("Id: "))
    if not i: imprimir_error("No encontrado")
    else: mostrar_detalle(i)
    pausa()

def actualizar_inquilino():
    imprimir_titulo("ACTUALIZAR INQUILINO")
    id_i = pedir_entero("Id: ")
    i = inquilinos.obtener(id_i)
    if not i:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("nombre", "apellido", "email", "documento", "telefono"):
        actual = getattr(i, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*inquilinos.actualizar(id_i, cambios))
    pausa()

def eliminar_inquilino():
    imprimir_titulo("ELIMINAR INQUILINO")
    id_i = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este inquilino?"):
        mostrar_resultado(*inquilinos.eliminar(id_i))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# FUNCIONES DE PROPIEDADES
# =====================================================================
def crear_propiedad():
    imprimir_titulo("REGISTRAR PROPIEDAD")
    datos = {
        "codigo_propiedad": input("Código (ej. PROP101): "),
        "tipo": input("Tipo (Departamento, Casa, Local): "),
        "direccion": input("Dirección: "),
        "precio_mes": input("Precio por mes ($): ")
    }
    mostrar_resultado(*propiedades.crear(datos))
    pausa()

def listar_propiedades():
    imprimir_titulo("CATÁLOGO DE PROPIEDADES")
    mostrar_lista(propiedades.leer(), "No hay propiedades registradas.")
    pausa()

def buscar_propiedad():
    imprimir_titulo("BUSCAR PROPIEDAD")
    termino = input("Código, tipo o dirección: ")
    mostrar_lista(propiedades.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_propiedad():
    imprimir_titulo("VER PROPIEDAD POR ID")
    p = propiedades.obtener(pedir_entero("Id: "))
    if not p: imprimir_error("No encontrado")
    else: mostrar_detalle(p)
    pausa()

def actualizar_propiedad():
    imprimir_titulo("ACTUALIZAR PROPIEDAD")
    id_p = pedir_entero("Id: ")
    p = propiedades.obtener(id_p)
    if not p:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("codigo_propiedad", "tipo", "direccion", "precio_mes"):
        actual = getattr(p, campo)
        nuevo = input(f"{campo.replace('_', ' ').capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*propiedades.actualizar(id_p, cambios))
    pausa()

def eliminar_propiedad():
    imprimir_titulo("ELIMINAR PROPIEDAD")
    id_p = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar esta propiedad?"):
        mostrar_resultado(*propiedades.eliminar(id_p))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# FUNCIONES DE CONTRATOS
# =====================================================================
def registrar_contrato():
    imprimir_titulo("GENERAR CONTRATO DE ALQUILER")
    imprimir_info("Inquilinos:")
    mostrar_lista(inquilinos.leer())
    imprimir_info("Propiedades disponibles:")
    mostrar_lista(propiedades.propiedades_disponibles(), "No hay propiedades libres.")

    inq_id = pedir_entero("\nId del inquilino: ")
    prop_id = pedir_entero("Id de la propiedad: ")
    meses = pedir_entero("Meses de contrato: ")
    fecha = input("Fecha de inicio (ej. 2026-06-01): ")

    datos = {
        "inquilino_id": inq_id,
        "propiedad_id": prop_id,
        "meses_contrato": meses,
        "fecha_inicio": fecha
    }
    mostrar_resultado(*contratos.crear(datos))
    pausa()

def listar_contratos():
    imprimir_titulo("LISTA DE CONTRATOS")
    mostrar_lista(contratos.leer(), "No hay contratos registrados.")
    pausa()

def ver_comprobante_contrato():
    imprimir_titulo("COMPROBANTE DE CONTRATO")
    texto = contratos.comprobante_contrato(pedir_entero("Id del contrato: "))
    if not texto: imprimir_error("No existe ese contrato")
    else: print(texto)
    pausa()

def cancelar_contrato():
    imprimir_titulo("CANCELAR CONTRATO")
    id_c = pedir_entero("Id del contrato: ")
    if id_c and confirmar("¿Confirma cancelar este contrato y liberar la propiedad?"):
        mostrar_resultado(*contratos.eliminar(id_c))
    else:
        imprimir_info("Operación cancelada")
    pausa()

def resumen_inmobiliaria():
    imprimir_titulo("RESUMEN INMOBILIARIA")
    print(f"  Inquilinos registrados  : {len(inquilinos.leer())}")
    print(f"  Propiedades totales     : {len(propiedades.leer())}")
    print(f"  Propiedades libres      : {len(propiedades.propiedades_disponibles())}")
    print(f"  Contratos activos       : {len(contratos.leer())}")
    print(f"  Total inicial recaudado : ${contratos.total_recaudado():.2f}")
    pausa()


# =====================================================================
# CONFIGURACIÓN DE MENÚS
# =====================================================================
MENU_INQUILINOS = {
    "1": ("Registrar inquilino", crear_inquilino),
    "2": ("Ver todos", listar_inquilinos),
    "3": ("Buscar", buscar_inquilino),
    "4": ("Ver por id", ver_inquilino),
    "5": ("Actualizar", actualizar_inquilino),
    "6": ("Eliminar", eliminar_inquilino),
    "0": ("Volver", None),
}

MENU_PROPIEDADES = {
    "1": ("Registrar propiedad", crear_propiedad),
    "2": ("Ver todas", listar_propiedades),
    "3": ("Buscar", buscar_propiedad),
    "4": ("Ver por id", ver_propiedad),
    "5": ("Actualizar", actualizar_propiedad),
    "6": ("Eliminar", eliminar_propiedad),
    "0": ("Volver", None),
}

MENU_CONTRATOS = {
    "1": ("Generar contrato", registrar_contrato),
    "2": ("Ver contratos", listar_contratos),
    "3": ("Ver comprobante", ver_comprobante_contrato),
    "4": ("Cancelar contrato", cancelar_contrato),
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
        imprimir_titulo("SISTEMA DE INMOBILIARIA")
        print("  1. Inquilinos")
        print("  2. Propiedades")
        print("  3. Contratos de Alquiler")
        print("  4. Resumen")
        print("  0. Salir\n")

        tecla = input("Opción: ").strip()
        if tecla == "1": ejecutar_menu("INQUILINOS", MENU_INQUILINOS)
        elif tecla == "2": ejecutar_menu("PROPIEDADES", MENU_PROPIEDADES)
        elif tecla == "3": ejecutar_menu("CONTRATOS", MENU_CONTRATOS)
        elif tecla == "4": resumen_inmobiliaria()
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