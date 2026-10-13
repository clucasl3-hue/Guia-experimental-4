from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import AdoptanteController, MascotaRefugioController, ProcesoAdopcionController

adoptantes = AdoptanteController()
mascotas = MascotaRefugioController()
adopciones = ProcesoAdopcionController(adoptantes, mascotas)


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
# FUNCIONES DE ADOPTANTES
# =====================================================================
def crear_adoptante():
    imprimir_titulo("REGISTRAR ADOPTANTE")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "cedula": input("Cédula: "),
        "telefono": input("Teléfono: ")
    }
    mostrar_resultado(*adoptantes.crear(datos))
    pausa()

def listar_adoptantes():
    imprimir_titulo("LISTA DE ADOPTANTES")
    mostrar_lista(adoptantes.leer(), "No hay adoptantes registrados.")
    pausa()

def buscar_adoptante():
    imprimir_titulo("BUSCAR ADOPTANTE")
    termino = input("Nombre, apellido o cédula: ")
    mostrar_lista(adoptantes.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_adoptante():
    imprimir_titulo("VER ADOPTANTE POR ID")
    a = adoptantes.obtener(pedir_entero("Id: "))
    if not a: imprimir_error("No encontrado")
    else: mostrar_detalle(a)
    pausa()

def actualizar_adoptante():
    imprimir_titulo("ACTUALIZAR ADOPTANTE")
    id_a = pedir_entero("Id: ")
    a = adoptantes.obtener(id_a)
    if not a:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("nombre", "apellido", "email", "cedula", "telefono"):
        actual = getattr(a, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*adoptantes.actualizar(id_a, cambios))
    pausa()

def eliminar_adoptante():
    imprimir_titulo("ELIMINAR ADOPTANTE")
    id_a = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar este adoptante?"):
        mostrar_resultado(*adoptantes.eliminar(id_a))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# FUNCIONES DE MASCOTAS
# =====================================================================
def crear_mascota():
    imprimir_titulo("REGISTRAR MASCOTA EN REFUGIO")
    datos = {
        "chip_id": input("Chip ID (ej. CHIP-999): "),
        "nombre_mascota": input("Nombre de la mascota: "),
        "especie": input("Especie (Perro, Gato, etc.): "),
        "edad_meses": input("Edad en meses: ")
    }
    mostrar_resultado(*mascotas.crear(datos))
    pausa()

def listar_mascotas():
    imprimir_titulo("LISTA DE MASCOTAS")
    mostrar_lista(mascotas.leer(), "No hay mascotas registradas.")
    pausa()

def buscar_mascota():
    imprimir_titulo("BUSCAR MASCOTA")
    termino = input("Chip ID, nombre o especie: ")
    mostrar_lista(mascotas.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_mascota():
    imprimir_titulo("VER MASCOTA POR ID")
    m = mascotas.obtener(pedir_entero("Id: "))
    if not m: imprimir_error("No encontrado")
    else: mostrar_detalle(m)
    pausa()

def actualizar_mascota():
    imprimir_titulo("ACTUALIZAR MASCOTA")
    id_m = pedir_entero("Id: ")
    m = mascotas.obtener(id_m)
    if not m:
        imprimir_error("No encontrado")
        return pausa()

    cambios = {}
    for campo in ("chip_id", "nombre_mascota", "especie", "edad_meses"):
        actual = getattr(m, campo)
        nuevo = input(f"{campo.replace('_', ' ').capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*mascotas.actualizar(id_m, cambios))
    pausa()

def eliminar_mascota():
    imprimir_titulo("ELIMINAR MASCOTA")
    id_m = pedir_entero("Id: ")
    if confirmar("¿Confirma eliminar esta mascota?"):
        mostrar_resultado(*mascotas.eliminar(id_m))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# FUNCIONES DE ADOPCIONES
# =====================================================================
def registrar_adopcion():
    imprimir_titulo("INICIAR PROCESO DE ADOPCIÓN")
    imprimir_info("Adoptantes:")
    mostrar_lista(adoptantes.leer())
    imprimir_info("Mascotas disponibles:")
    mostrar_lista(mascotas.mascotas_disponibles(), "No hay mascotas libres.")

    adp_id = pedir_entero("\nId del adoptante: ")
    mas_id = pedir_entero("Id de la mascota: ")
    donacion = float(input("Donación voluntaria extra ($) [0 si no aplica]: ") or 0.0)

    datos = {
        "adoptante_id": adp_id,
        "mascota_id": mas_id,
        "donacion_voluntaria": donacion
    }
    mostrar_resultado(*adopciones.crear(datos))
    pausa()

def listar_adopciones():
    imprimir_titulo("LISTA DE ADOPCIONES EXITOSAS")
    mostrar_lista(adopciones.leer(), "No hay adopciones registradas.")
    pausa()

def ver_comprobante_adopcion():
    imprimir_titulo("CERTIFICADO DE ADOPCIÓN")
    texto = adopciones.comprobante_adopcion(pedir_entero("Id de la adopción: "))
    if not texto: imprimir_error("No existe esa adopción")
    else: print(texto)
    pausa()

def cancelar_adopcion():
    imprimir_titulo("CANCELAR ADOPCIÓN")
    id_p = pedir_entero("Id de la adopción: ")
    if id_p and confirmar("¿Confirma cancelar este proceso y devolver la mascota al refugio?"):
        mostrar_resultado(*adopciones.eliminar(id_p))
    else:
        imprimir_info("Operación cancelada")
    pausa()

def resumen_refugio():
    imprimir_titulo("RESUMEN REFUGIO DE ANIMALES")
    print(f"  Adoptantes registrados  : {len(adoptantes.leer())}")
    print(f"  Mascotas totales        : {len(mascotas.leer())}")
    print(f"  Mascotas disponibles    : {len(mascotas.mascotas_disponibles())}")
    print(f"  Adopciones concretadas  : {len(adopciones.leer())}")
    print(f"  Total recaudado (Trámites/Donaciones): ${adopciones.total_recaudado():.2f}")
    pausa()


# =====================================================================
# CONFIGURACIÓN DE MENÚS
# =====================================================================
MENU_ADOPTANTES = {
    "1": ("Registrar adoptante", crear_adoptante),
    "2": ("Ver todos", listar_adoptantes),
    "3": ("Buscar", buscar_adoptante),
    "4": ("Ver por id", ver_adoptante),
    "5": ("Actualizar", actualizar_adoptante),
    "6": ("Eliminar", eliminar_adoptante),
    "0": ("Volver", None),
}

MENU_MASCOTAS = {
    "1": ("Registrar mascota", crear_mascota),
    "2": ("Ver todas", listar_mascotas),
    "3": ("Buscar", buscar_mascota),
    "4": ("Ver por id", ver_mascota),
    "5": ("Actualizar", actualizar_mascota),
    "6": ("Eliminar", eliminar_mascota),
    "0": ("Volver", None),
}

MENU_ADOPCIONES = {
    "1": ("Registrar adopción", registrar_adopcion),
    "2": ("Ver adopciones", listar_adopciones),
    "3": ("Ver certificado", ver_comprobante_adopcion),
    "4": ("Cancelar adopción", cancelar_adopcion),
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
        imprimir_titulo("SISTEMA DE REFUGIO DE ANIMALES")
        print("  1. Adoptantes")
        print("  2. Mascotas")
        print("  3. Procesos de Adopción")
        print("  4. Resumen")
        print("  0. Salir\n")

        tecla = input("Opción: ").strip()
        if tecla == "1": ejecutar_menu("ADOPTANTES", MENU_ADOPTANTES)
        elif tecla == "2": ejecutar_menu("MASCOTAS", MENU_MASCOTAS)
        elif tecla == "3": ejecutar_menu("ADOPCIONES", MENU_ADOPCIONES)
        elif tecla == "4": resumen_refugio()
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