from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import ConductorController, TipoTramiteController, TurnoLicenciaController

conductores = ConductorController()
tramites = TipoTramiteController()
turnos = TurnoLicenciaController(conductores, tramites)


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
# MENÚ CONDUCTORES
# =====================================================================
def crear_conductor():
    imprimir_titulo("REGISTRAR CONDUCTOR")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "licencia": input("Número de licencia (ej. LIC12345): "),
        "tipo_sangre": input("Tipo de sangre (ej. O+): ")
    }
    mostrar_resultado(*conductores.crear(datos))
    pausa()

def listar_conductores():
    imprimir_titulo("LISTA DE CONDUCTORES")
    mostrar_lista(conductores.leer(), "No hay conductores registrados.")
    pausa()

def buscar_conductor():
    imprimir_titulo("BUSCAR CONDUCTOR")
    termino = input("Nombre, apellido o licencia: ")
    mostrar_lista(conductores.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_conductor():
    imprimir_titulo("VER CONDUCTOR POR ID")
    c = conductores.obtener(pedir_entero("Id: "))
    if not c: imprimir_error("No encontrado")
    else: mostrar_detalle(c)
    pausa()

def actualizar_conductor():
    imprimir_titulo("ACTUALIZAR CONDUCTOR")
    id_c = pedir_entero("Id: ")
    c = conductores.obtener(id_c)
    if not c:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("nombre", "apellido", "email", "licencia", "tipo_sangre"):
        actual = getattr(c, campo)
        nuevo = input(f"{campo.replace('_', ' ').capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*conductores.actualizar(id_c, cambios))
    pausa()

def eliminar_conductor():
    imprimir_titulo("ELIMINAR CONDUCTOR")
    id_c = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este conductor?"):
        mostrar_resultado(*conductores.eliminar(id_c))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ TIPOS DE TRÁMITE
# =====================================================================
def crear_tramite():
    imprimir_titulo("REGISTRAR TIPO DE TRÁMITE")
    datos = {
        "nombre_tramite": input("Nombre del trámite (ej. Renovación Licencia): "),
        "codigo": input("Código (ej. REN01): "),
        "costo_base": input("Costo base ($): ")
    }
    mostrar_resultado(*tramites.crear(datos))
    pausa()

def listar_tramites():
    imprimir_titulo("CATÁLOGO DE TRÁMITES")
    mostrar_lista(tramites.leer(), "No hay trámites registrados.")
    pausa()

def buscar_tramite():
    imprimir_titulo("BUSCAR TRÁMITE")
    termino = input("Nombre o código: ")
    mostrar_lista(tramites.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_tramite():
    imprimir_titulo("VER TRÁMITE POR ID")
    t = tramites.obtener(pedir_entero("Id: "))
    if not t: imprimir_error("No encontrado")
    else: mostrar_detalle(t)
    pausa()

def actualizar_tramite():
    imprimir_titulo("ACTUALIZAR TRÁMITE")
    id_t = pedir_entero("Id: ")
    t = tramites.obtener(id_t)
    if not t:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("nombre_tramite", "codigo", "costo_base"):
        actual = getattr(t, campo)
        nuevo = input(f"{campo.replace('_', ' ').capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*tramites.actualizar(id_t, cambios))
    pausa()

def eliminar_tramite():
    imprimir_titulo("ELIMINAR TRÁMITE")
    id_t = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este trámite?"):
        mostrar_resultado(*tramites.eliminar(id_t))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ TURNOS Y LICENCIAS
# =====================================================================
def asignar_turno():
    imprimir_titulo("ASIGNAR TURNO DE LICENCIA")
    imprimir_info("Conductores:")
    mostrar_lista(conductores.leer())
    imprimir_info("Trámites disponibles:")
    mostrar_lista(tramites.leer())

    con_id = pedir_entero("\nId del conductor: ")
    tra_id = pedir_entero("Id del trámite: ")
    atraso = pedir_entero("Días de atraso/multa (Enter para 0): ") or 0
    fecha = input("Fecha asignada (ej. 2026-06-15): ")

    datos = {
        "conductor_id": con_id,
        "tramite_id": tra_id,
        "dias_atraso": atraso,
        "fecha_asignada": fecha
    }
    mostrar_resultado(*turnos.crear(datos))
    pausa()

def listar_turnos():
    imprimir_titulo("LISTA DE TURNOS ASIGNADOS")
    mostrar_lista(turnos.leer(), "No hay turnos registrados.")
    pausa()

def ver_comprobante_turno():
    imprimir_titulo("COMPROBANTE DE TURNO")
    texto = turnos.comprobante_turno(pedir_entero("Id del turno: "))
    if not texto: imprimir_error("No existe ese turno")
    else: print(texto)
    pausa()

def cancelar_turno():
    imprimir_titulo("CANCELAR TURNO")
    id_t = pedir_entero("Id del turno: ")
    if id_t and confirmar("¿Confirma cancelar este turno?"):
        mostrar_resultado(*turnos.eliminar(id_t))
    else:
        imprimir_info("Operación cancelada")
    pausa()

def resumen_transito():
    imprimir_titulo("RESUMEN CONTROL DE TRÁNSITO")
    print(f"  Conductores registrados : {len(conductores.leer())}")
    print(f"  Tipos de trámites       : {len(tramites.leer())}")
    print(f"  Turnos emitidos         : {len(turnos.leer())}")
    print(f"  Total recaudado (multas): ${turnos.total_recaudado():.2f}")
    pausa()


# =====================================================================
# CONFIGURACIÓN DE MENÚS (Diccionarios)
# =====================================================================
MENU_CONDUCTORES = {
    "1": ("Registrar conductor", crear_conductor),
    "2": ("Ver todos", listar_conductores),
    "3": ("Buscar", buscar_conductor),
    "4": ("Ver por id", ver_conductor),
    "5": ("Actualizar", actualizar_conductor),
    "6": ("Eliminar", eliminar_conductor),
    "0": ("Volver", None),
}

MENU_TRAMITES = {
    "1": ("Registrar trámite", crear_tramite),
    "2": ("Ver todos", listar_tramites),
    "3": ("Buscar", buscar_tramite),
    "4": ("Ver por id", ver_tramite),
    "5": ("Actualizar", actualizar_tramite),
    "6": ("Eliminar", eliminar_tramite),
    "0": ("Volver", None),
}

MENU_TURNOS = {
    "1": ("Asignar turno", asignar_turno),
    "2": ("Ver turnos", listar_turnos),
    "3": ("Ver comprobante", ver_comprobante_turno),
    "4": ("Cancelar turno", cancelar_turno),
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
        imprimir_titulo("SISTEMA CONTROL DE TRÁNSITO - LICENCIAS")
        print("  1. Conductores")
        print("  2. Tipos de Trámite")
        print("  3. Turnos y Licencias")
        print("  4. Resumen")
        print("  0. Salir\n")

        tecla = input("Opción: ").strip()
        if tecla == "1": ejecutar_menu("CONDUCTORES", MENU_CONDUCTORES)
        elif tecla == "2": ejecutar_menu("TRÁMITES", MENU_TRAMITES)
        elif tecla == "3": ejecutar_menu("TURNOS", MENU_TURNOS)
        elif tecla == "4": resumen_transito()
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