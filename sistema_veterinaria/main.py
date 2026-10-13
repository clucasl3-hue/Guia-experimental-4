from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import DuenioController, ServicioVeterinarioController, HistorialAtencionController

duenios = DuenioController()
servicios = ServicioVeterinarioController()
historiales = HistorialAtencionController(duenios, servicios)


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
# MENÚ DUEÑOS
# =====================================================================
def crear_duenio():
    imprimir_titulo("REGISTRAR DUEÑO")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "telefono": input("Teléfono: "),
        "direccion": input("Dirección: ")
    }
    mostrar_resultado(*duenios.crear(datos))
    pausa()

def listar_duenios():
    imprimir_titulo("LISTA DE DUEÑOS")
    mostrar_lista(duenios.leer(), "No hay dueños registrados.")
    pausa()

def buscar_duenio():
    imprimir_titulo("BUSCAR DUEÑO")
    termino = input("Nombre, apellido o email: ")
    mostrar_lista(duenios.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_duenio():
    imprimir_titulo("VER DUEÑO POR ID")
    d = duenios.obtener(pedir_entero("Id: "))
    if not d: imprimir_error("No encontrado")
    else: mostrar_detalle(d)
    pausa()

def actualizar_duenio():
    imprimir_titulo("ACTUALIZAR DUEÑO")
    id_d = pedir_entero("Id: ")
    d = duenios.obtener(id_d)
    if not d:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("nombre", "apellido", "email", "telefono", "direccion"):
        actual = getattr(d, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*duenios.actualizar(id_d, cambios))
    pausa()

def eliminar_duenio():
    imprimir_titulo("ELIMINAR DUEÑO")
    id_d = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este dueño?"):
        mostrar_resultado(*duenios.eliminar(id_d))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ SERVICIOS VETERINARIOS
# =====================================================================
def crear_servicio():
    imprimir_titulo("REGISTRAR SERVICIO")
    datos = {
        "nombre_servicio": input("Nombre del servicio (ej. Vacuna Antirrábica): "),
        "codigo": input("Código (ej. VAC01): "),
        "costo": input("Costo base ($): ")
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
    for campo in ("nombre_servicio", "codigo", "costo"):
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
# MENÚ HISTORIAL DE ATENCIÓN
# =====================================================================
def registrar_atencion():
    imprimir_titulo("REGISTRAR ATENCIÓN VETERINARIA")
    imprimir_info("Dueños:")
    mostrar_lista(duenios.leer())
    imprimir_info("Servicios disponibles:")
    mostrar_lista(servicios.leer())

    due_id = pedir_entero("\nId del dueño: ")
    ser_id = pedir_entero("Id del servicio: ")
    mascota = input("Nombre de la mascota: ")
    especie = input("Especie (ej. Canino, Felino): ")
    obs = input("Observaciones médicas: ")
    es_afil = confirmar("¿El dueño tiene membresía afiliada (15% desc.)?")

    datos = {
        "duenio_id": due_id,
        "servicio_id": ser_id,
        "nombre_mascota": mascota,
        "especie": especie,
        "observaciones": obs,
        "es_afiliado": es_afil
    }
    mostrar_resultado(*historiales.crear(datos))
    pausa()

def listar_historial():
    imprimir_titulo("HISTORIAL DE ATENCIONES")
    mostrar_lista(historiales.leer(), "No hay atenciones registradas.")
    pausa()

def ver_comprobante_atencion():
    imprimir_titulo("COMPROBANTE DE ATENCIÓN")
    texto = historiales.comprobante_atencion(pedir_entero("Id de la atención: "))
    if not texto: imprimir_error("No existe esa atención")
    else: print(texto)
    pausa()

def cancelar_atencion():
    imprimir_titulo("ELIMINAR REGISTRO")
    id_h = pedir_entero("Id de la atención: ")
    if id_h and confirmar("¿Confirma eliminar este registro?"):
        mostrar_resultado(*historiales.eliminar(id_h))
    else:
        imprimir_info("Operación cancelada")
    pausa()

def resumen_veterinaria():
    imprimir_titulo("RESUMEN VETERINARIA PATITAS FELICES")
    print(f"  Dueños registrados      : {len(duenios.leer())}")
    print(f"  Servicios en catálogo   : {len(servicios.leer())}")
    print(f"  Atenciones brindadas    : {len(historiales.leer())}")
    print(f"  Total recaudado         : ${historiales.total_recaudado():.2f}")
    pausa()


# =====================================================================
# CONFIGURACIÓN DE MENÚS (Diccionarios)
# =====================================================================
MENU_DUENIOS = {
    "1": ("Registrar dueño", crear_duenio),
    "2": ("Ver todos", listar_duenios),
    "3": ("Buscar", buscar_duenio),
    "4": ("Ver por id", ver_duenio),
    "5": ("Actualizar", actualizar_duenio),
    "6": ("Eliminar", eliminar_duenio),
    "0": ("Volver", None),
}

MENU_SERVICIOS = {
    "1": ("Registrar servicio", crear_servicio),
    "2": ("Ver todos", listar_servicios),
    "3": ("Buscar", buscar_servicio),
    "4": ("Ver por id", ver_servicio),
    "5": ("Actualizar", actualizar_servicio),
    "6": ("Eliminar", eliminar_servicio),
    "0": ("Volver", None),
}

MENU_HISTORIAL = {
    "1": ("Registrar atención", registrar_atencion),
    "2": ("Ver historial", listar_historial),
    "3": ("Ver comprobante", ver_comprobante_atencion),
    "4": ("Eliminar registro", cancelar_atencion),
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
        imprimir_titulo("SISTEMA VETERINARIA PATITAS FELICES")
        print("  1. Dueños y Mascotas")
        print("  2. Servicios Veterinarios")
        print("  3. Historial de Atenciones")
        print("  4. Resumen")
        print("  0. Salir\n")

        tecla = input("Opción: ").strip()
        if tecla == "1": ejecutar_menu("DUEÑOS", MENU_DUENIOS)
        elif tecla == "2": ejecutar_menu("SERVICIOS", MENU_SERVICIOS)
        elif tecla == "3": ejecutar_menu("HISTORIAL", MENU_HISTORIAL)
        elif tecla == "4": resumen_veterinaria()
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