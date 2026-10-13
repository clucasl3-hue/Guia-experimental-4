from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import PacienteDentalController, TratamientoDentalController, CitaDentalController

pacientes = PacienteDentalController()
tratamientos = TratamientoDentalController()
citas = CitaDentalController(pacientes, tratamientos)


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
# FUNCIONES DE PACIENTES
# =====================================================================
def crear_paciente():
    imprimir_titulo("REGISTRAR PACIENTE DENTAL")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "cedula": input("Cédula: "),
        "telefono": input("Teléfono: ")
    }
    mostrar_resultado(*pacientes.crear(datos))
    pausa()

def listar_pacientes():
    imprimir_titulo("LISTA DE PACIENTES")
    mostrar_lista(pacientes.leer(), "No hay pacientes registrados.")
    pausa()

def buscar_paciente():
    imprimir_titulo("BUSCAR PACIENTE")
    termino = input("Nombre, apellido o cédula: ")
    mostrar_lista(pacientes.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_paciente():
    imprimir_titulo("VER PACIENTE POR ID")
    p = pacientes.obtener(pedir_entero("Id: "))
    if not p: imprimir_error("No encontrado")
    else: mostrar_detalle(p)
    pausa()

def actualizar_paciente():
    imprimir_titulo("ACTUALIZAR PACIENTE")
    id_p = pedir_entero("Id: ")
    p = pacientes.obtener(id_p)
    if not p:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("nombre", "apellido", "email", "cedula", "telefono"):
        actual = getattr(p, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*pacientes.actualizar(id_p, cambios))
    pausa()

def eliminar_paciente():
    imprimir_titulo("ELIMINAR PACIENTE")
    id_p = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este paciente?"):
        mostrar_resultado(*pacientes.eliminar(id_p))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# FUNCIONES DE TRATAMIENTOS
# =====================================================================
def crear_tratamiento():
    imprimir_titulo("REGISTRAR TRATAMIENTO")
    datos = {
        "nombre_tratamiento": input("Nombre del tratamiento (ej. Limpieza Dental): "),
        "codigo": input("Código (ej. LIM01): "),
        "costo_base": input("Costo base ($): ")
    }
    mostrar_resultado(*tratamientos.crear(datos))
    pausa()

def listar_tratamientos():
    imprimir_titulo("CATÁLOGO DE TRATAMIENTOS")
    mostrar_lista(tratamientos.leer(), "No hay tratamientos registrados.")
    pausa()

def buscar_tratamiento():
    imprimir_titulo("BUSCAR TRATAMIENTO")
    termino = input("Nombre o código: ")
    mostrar_lista(tratamientos.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_tratamiento():
    imprimir_titulo("VER TRATAMIENTO POR ID")
    t = tratamientos.obtener(pedir_entero("Id: "))
    if not t: imprimir_error("No encontrado")
    else: mostrar_detalle(t)
    pausa()

def actualizar_tratamiento():
    imprimir_titulo("ACTUALIZAR TRATAMIENTO")
    id_t = pedir_entero("Id: ")
    t = tratamientos.obtener(id_t)
    if not t:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("nombre_tratamiento", "codigo", "costo_base"):
        actual = getattr(t, campo)
        nuevo = input(f"{campo.replace('_', ' ').capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*tratamientos.actualizar(id_t, cambios))
    pausa()

def eliminar_tratamiento():
    imprimir_titulo("ELIMINAR TRATAMIENTO")
    id_t = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este tratamiento?"):
        mostrar_resultado(*tratamientos.eliminar(id_t))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# FUNCIONES DE CITAS
# =====================================================================
def registrar_cita():
    imprimir_titulo("AGENDAR CITA DENTAL")
    imprimir_info("Pacientes:")
    mostrar_lista(pacientes.leer())
    imprimir_info("Tratamientos:")
    mostrar_lista(tratamientos.leer())

    pac_id = pedir_entero("\nId del paciente: ")
    tra_id = pedir_entero("Id del tratamiento: ")
    con_seg = confirmar("¿El paciente tiene seguro dental (20% desc.)?")
    fecha = input("Fecha de cita (ej. 2026-06-20): ")

    datos = {
        "paciente_id": pac_id,
        "tratamiento_id": tra_id,
        "con_seguro": con_seg,
        "fecha_cita": fecha
    }
    mostrar_resultado(*citas.crear(datos))
    pausa()

def listar_citas():
    imprimir_titulo("LISTA DE CITAS MÉDICAS")
    mostrar_lista(citas.leer(), "No hay citas registradas.")
    pausa()

def ver_comprobante_cita():
    imprimir_titulo("COMPROBANTE DE CITA")
    texto = citas.comprobante_cita(pedir_entero("Id de la cita: "))
    if not texto: imprimir_error("No existe esa cita")
    else: print(texto)
    pausa()

def cancelar_cita():
    imprimir_titulo("CANCELAR CITA")
    id_c = pedir_entero("Id de la cita: ")
    if id_c and confirmar("¿Confirma cancelar esta cita?"):
        mostrar_resultado(*citas.eliminar(id_c))
    else:
        imprimir_info("Operación cancelada")
    pausa()

def resumen_dental():
    imprimir_titulo("RESUMEN CLÍNICA DENTAL")
    print(f"  Pacientes registrados   : {len(pacientes.leer())}")
    print(f"  Tratamientos en catálogo: {len(tratamientos.leer())}")
    print(f"  Citas agendadas         : {len(citas.leer())}")
    print(f"  Total recaudado         : ${citas.total_recaudado():.2f}")
    pausa()


# =====================================================================
# CONFIGURACIÓN DE MENÚS (Definidos después de todas las funciones)
# =====================================================================
MENU_PACIENTES = {
    "1": ("Registrar paciente", crear_paciente),
    "2": ("Ver todos", listar_pacientes),
    "3": ("Buscar", buscar_paciente),
    "4": ("Ver por id", ver_paciente),
    "5": ("Actualizar", actualizar_paciente),
    "6": ("Eliminar", eliminar_paciente),
    "0": ("Volver", None),
}

MENU_TRATAMIENTOS = {
    "1": ("Registrar tratamiento", crear_tratamiento),
    "2": ("Ver catálogo", listar_tratamientos),
    "3": ("Buscar", buscar_tratamiento),
    "4": ("Ver por id", ver_tratamiento),
    "5": ("Actualizar", actualizar_tratamiento),
    "6": ("Eliminar", eliminar_tratamiento),
    "0": ("Volver", None),
}

MENU_CITAS = {
    "1": ("Agendar cita", registrar_cita),
    "2": ("Ver citas", listar_citas),
    "3": ("Ver comprobante", ver_comprobante_cita),
    "4": ("Cancelar cita", cancelar_cita),
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
        imprimir_titulo("SISTEMA CLÍNICA DENTAL")
        print("  1. Pacientes")
        print("  2. Tratamientos")
        print("  3. Citas Médicas")
        print("  4. Resumen")
        print("  0. Salir\n")

        tecla = input("Opción: ").strip()
        if tecla == "1": ejecutar_menu("PACIENTES", MENU_PACIENTES)
        elif tecla == "2": ejecutar_menu("TRATAMIENTOS", MENU_TRATAMIENTOS)
        elif tecla == "3": ejecutar_menu("CITAS", MENU_CITAS)
        elif tecla == "4": resumen_dental()
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