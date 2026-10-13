from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import PacienteController, DoctorController, CitaMedicaController

pacientes = PacienteController()
doctores = DoctorController()
citas = CitaMedicaController(pacientes, doctores)


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
# MENÚ PACIENTES
# =====================================================================
def crear_paciente():
    imprimir_titulo("REGISTRAR PACIENTE")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "cedula": input("Cédula: "),
        "tipo_sangre": input("Tipo de sangre (ej. O+): ")
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
    for campo in ("nombre", "apellido", "email", "cedula", "tipo_sangre"):
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
# MENÚ DOCTORES
# =====================================================================
def crear_doctor():
    imprimir_titulo("REGISTRAR DOCTOR")
    datos = {
        "nombre_doctor": input("Nombre del doctor: "),
        "especialidad": input("Especialidad: "),
        "consultorio": input("Consultorio: "),
        "costo": input("Costo consulta (Enter para $50 por defecto): ")
    }
    mostrar_resultado(*doctores.crear(datos))
    pausa()

def listar_doctores():
    imprimir_titulo("LISTA DE DOCTORES")
    mostrar_lista(doctores.leer(), "No hay doctores registrados.")
    pausa()

def buscar_doctor():
    imprimir_titulo("BUSCAR DOCTOR")
    termino = input("Nombre o especialidad: ")
    mostrar_lista(doctores.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_doctor():
    imprimir_titulo("VER DOCTOR POR ID")
    d = doctores.obtener(pedir_entero("Id: "))
    if not d: imprimir_error("No encontrado")
    else: mostrar_detalle(d)
    pausa()

def actualizar_doctor():
    imprimir_titulo("ACTUALIZAR DOCTOR")
    id_d = pedir_entero("Id: ")
    d = doctores.obtener(id_d)
    if not d:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("nombre_doctor", "especialidad", "consultorio", "costo"):
        actual = getattr(d, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*doctores.actualizar(id_d, cambios))
    pausa()

def eliminar_doctor():
    imprimir_titulo("ELIMINAR DOCTOR")
    id_d = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este doctor?"):
        mostrar_resultado(*doctores.eliminar(id_d))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ CITAS MÉDICAS
# =====================================================================
def agendar_cita():
    imprimir_titulo("AGENDAR CITA MÉDICA")
    imprimir_info("Pacientes:")
    mostrar_lista(pacientes.leer())
    imprimir_info("Doctores:")
    mostrar_lista(doctores.leer())

    pac_id = pedir_entero("\nId del paciente: ")
    doc_id = pedir_entero("Id del doctor: ")
    fecha = input("Fecha de la cita (ej. 2026-06-15): ")
    sintomas = input("Síntomas o motivo: ")
    es_tercera = confirmar("¿El paciente es de tercera edad (50% desc.)?")

    datos = {
        "paciente_id": pac_id,
        "doctor_id": doc_id,
        "fecha": fecha,
        "sintomas": sintomas,
        "es_tercera_edad": es_tercera
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
    if id_c and confirmar("¿Confirma cancelar la cita?"):
        mostrar_resultado(*citas.eliminar(id_c))
    else:
        imprimir_info("Operación cancelada")
    pausa()

def resumen_hospital():
    imprimir_titulo("RESUMEN HOSPITALARIO")
    print(f"  Pacientes registrados : {len(pacientes.leer())}")
    print(f"  Tipos de sangre       : {', '.join(pacientes.tipos_sangre_unicos()) or '-'}")
    print(f"  Doctores en staff     : {len(doctores.leer())}")
    print(f"  Citas médicas agendadas: {len(citas.leer())}")
    print(f"  Total recaudado       : ${citas.total_recaudado():.2f}")
    pausa()


# =====================================================================
# CONFIGURACIÓN DE MENÚS (Diccionarios)
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

MENU_DOCTORES = {
    "1": ("Registrar doctor", crear_doctor),
    "2": ("Ver todos", listar_doctores),
    "3": ("Buscar", buscar_doctor),
    "4": ("Ver por id", ver_doctor),
    "5": ("Actualizar", actualizar_doctor),
    "6": ("Eliminar", eliminar_doctor),
    "0": ("Volver", None),
}

MENU_CITAS = {
    "1": ("Agendar cita", agendar_cita),
    "2": ("Ver todas las citas", listar_citas),
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
        imprimir_titulo("SISTEMA HOSPITALARIO CLÍNICA")
        print("  1. Pacientes")
        print("  2. Doctores")
        print("  3. Citas Médicas")
        print("  4. Resumen")
        print("  0. Salir\n")

        tecla = input("Opción: ").strip()
        if tecla == "1": ejecutar_menu("PACIENTES", MENU_PACIENTES)
        elif tecla == "2": ejecutar_menu("DOCTORES", MENU_DOCTORES)
        elif tecla == "3": ejecutar_menu("CITAS MÉDICAS", MENU_CITAS)
        elif tecla == "4": resumen_hospital()
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