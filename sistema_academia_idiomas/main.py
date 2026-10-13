from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import EstudianteIdiomaController, CursoIdiomaController, MatriculaCursoController

estudiantes = EstudianteIdiomaController()
cursos = CursoIdiomaController()
matriculas = MatriculaCursoController(estudiantes, cursos)


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
# FUNCIONES DE ESTUDIANTES
# =====================================================================
def crear_estudiante():
    imprimir_titulo("REGISTRAR ESTUDIANTE")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "documento": input("Documento / Pasaporte: "),
        "telefono": input("Teléfono: ")
    }
    mostrar_resultado(*estudiantes.crear(datos))
    pausa()

def listar_estudiantes():
    imprimir_titulo("LISTA DE ESTUDIANTES")
    mostrar_lista(estudiantes.leer(), "No hay estudiantes registrados.")
    pausa()

def buscar_estudiante():
    imprimir_titulo("BUSCAR ESTUDIANTE")
    termino = input("Nombre, apellido o documento: ")
    mostrar_lista(estudiantes.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_estudiante():
    imprimir_titulo("VER ESTUDIANTE POR ID")
    e = estudiantes.obtener(pedir_entero("Id: "))
    if not e: imprimir_error("No encontrado")
    else: mostrar_detalle(e)
    pausa()

def actualizar_estudiante():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    id_e = pedir_entero("Id: ")
    e = estudiantes.obtener(id_e)
    if not e:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("nombre", "apellido", "email", "documento", "telefono"):
        actual = getattr(e, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*estudiantes.actualizar(id_e, cambios))
    pausa()

def eliminar_estudiante():
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    id_e = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este estudiante?"):
        mostrar_resultado(*estudiantes.eliminar(id_e))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# FUNCIONES DE CURSOS
# =====================================================================
def crear_curso():
    imprimir_titulo("REGISTRAR CURSO DE IDIOMA")
    datos = {
        "nombre_idioma": input("Idioma (ej. Inglés, Francés): "),
        "nivel": input("Nivel (ej. A1, B2, C1): "),
        "costo_curso": input("Costo base del curso ($): ")
    }
    mostrar_resultado(*cursos.crear(datos))
    pausa()

def listar_cursos():
    imprimir_titulo("CATÁLOGO DE CURSOS")
    mostrar_lista(cursos.leer(), "No hay cursos registrados.")
    pausa()

def buscar_curso():
    imprimir_titulo("BUSCAR CURSO")
    termino = input("Idioma o nivel: ")
    mostrar_lista(cursos.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_curso():
    imprimir_titulo("VER CURSO POR ID")
    c = cursos.obtener(pedir_entero("Id: "))
    if not c: imprimir_error("No encontrado")
    else: mostrar_detalle(c)
    pausa()

def actualizar_curso():
    imprimir_titulo("ACTUALIZAR CURSO")
    id_c = pedir_entero("Id: ")
    c = cursos.obtener(id_c)
    if not c:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("nombre_idioma", "nivel", "costo_curso"):
        actual = getattr(c, campo)
        nuevo = input(f"{campo.replace('_', ' ').capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*cursos.actualizar(id_c, cambios))
    pausa()

def eliminar_curso():
    imprimir_titulo("ELIMINAR CURSO")
    id_c = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este curso?"):
        mostrar_resultado(*cursos.eliminar(id_c))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# FUNCIONES DE MATRÍCULAS
# =====================================================================
def registrar_matricula():
    imprimir_titulo("MATRICULAR ESTUDIANTE EN CURSO")
    imprimir_info("Estudiantes:")
    mostrar_lista(estudiantes.leer())
    imprimir_info("Cursos disponibles:")
    mostrar_lista(cursos.leer())

    est_id = pedir_entero("\nId del estudiante: ")
    cur_id = pedir_entero("Id del curso: ")
    pronto_pago = confirmar("¿Aplicar descuento por pronto pago (10% desc.)?")

    datos = {
        "estudiante_id": est_id,
        "curso_id": cur_id,
        "pronto_pago": pronto_pago
    }
    mostrar_resultado(*matriculas.crear(datos))
    pausa()

def listar_matriculas():
    imprimir_titulo("LISTA DE MATRÍCULAS")
    mostrar_lista(matriculas.leer(), "No hay matrículas registradas.")
    pausa()

def ver_comprobante_matricula():
    imprimir_titulo("COMPROBANTE DE MATRÍCULA")
    texto = matriculas.comprobante_matricula(pedir_entero("Id de la matrícula: "))
    if not texto: imprimir_error("No existe esa matrícula")
    else: print(texto)
    pausa()

def cancelar_matricula():
    imprimir_titulo("CANCELAR MATRÍCULA")
    id_m = pedir_entero("Id de la matrícula: ")
    if id_m and confirmar("¿Confirma cancelar esta matrícula?"):
        mostrar_resultado(*matriculas.eliminar(id_m))
    else:
        imprimir_info("Operación cancelada")
    pausa()

def resumen_idiomas():
    imprimir_titulo("RESUMEN ACADEMIA DE IDIOMAS")
    print(f"  Estudiantes registrados : {len(estudiantes.leer())}")
    print(f"  Cursos en catálogo      : {len(cursos.leer())}")
    print(f"  Matrículas totales      : {len(matriculas.leer())}")
    print(f"  Total recaudado         : ${matriculas.total_recaudado():.2f}")
    pausa()


# =====================================================================
# CONFIGURACIÓN DE MENÚS
# =====================================================================
MENU_ESTUDIANTES = {
    "1": ("Registrar estudiante", crear_estudiante),
    "2": ("Ver todos", listar_estudiantes),
    "3": ("Buscar", buscar_estudiante),
    "4": ("Ver por id", ver_estudiante),
    "5": ("Actualizar", actualizar_estudiante),
    "6": ("Eliminar", eliminar_estudiante),
    "0": ("Volver", None),
}

MENU_CURSOS = {
    "1": ("Registrar curso", crear_curso),
    "2": ("Ver catálogo", listar_cursos),
    "3": ("Buscar", buscar_curso),
    "4": ("Ver por id", ver_curso),
    "5": ("Actualizar", actualizar_curso),
    "6": ("Eliminar", eliminar_curso),
    "0": ("Volver", None),
}

MENU_MATRICULAS = {
    "1": ("Registrar matrícula", registrar_matricula),
    "2": ("Ver matrículas", listar_matriculas),
    "3": ("Ver comprobante", ver_comprobante_matricula),
    "4": ("Cancelar matrícula", cancelar_matricula),
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
        imprimir_titulo("SISTEMA DE ACADEMIA DE IDIOMAS")
        print("  1. Estudiantes")
        print("  2. Cursos")
        print("  3. Matrículas")
        print("  4. Resumen")
        print("  0. Salir\n")

        tecla = input("Opción: ").strip()
        if tecla == "1": ejecutar_menu("ESTUDIANTES", MENU_ESTUDIANTES)
        elif tecla == "2": ejecutar_menu("CURSOS", MENU_CURSOS)
        elif tecla == "3": ejecutar_menu("MATRICULAS", MENU_MATRICULAS)
        elif tecla == "4": resumen_idiomas()
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