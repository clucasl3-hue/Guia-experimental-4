from abc import ABC, abstractmethod
import os
from datetime import date

from models import Lector, Libro, Prestamo
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


class CrudBase(ABC):
    @abstractmethod
    def leer(self): pass
    @abstractmethod
    def obtener(self, id_registro): pass
    @abstractmethod
    def buscar(self, texto): pass
    @abstractmethod
    def siguiente(self): pass
    @abstractmethod
    def crear(self, datos): pass
    @abstractmethod
    def actualizar(self, id_registro, datos): pass
    @abstractmethod
    def eliminar(self, id_registro): pass


class LectorController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "lectores.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Lector.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([l.a_diccionario() for l in self.lista])

    def codigos_registrados(self, excepto_id=None):
        """CONJUNTO para verificar códigos de lector únicos instantáneamente."""
        return {l.codigo_lector.strip().upper() for l in self.lista if l.id != excepto_id and l.codigo_lector}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "apellido", "email", "codigo_lector"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"

        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            if not es_email_valido(email): return f"Email inválido: '{email}'"
            if email in {l.email for l in self.lista if l.id != id_actual}:
                return "Ese email ya está registrado"

        if "codigo_lector" in datos:
            codigo = str(datos["codigo_lector"]).strip().upper()
            if codigo in self.codigos_registrados(id_actual):
                return f"El código de lector '{codigo}' ya existe"
        return None

    def leer(self): return self.lista

    def obtener(self, id_lector):
        for l in self.lista:
            if l.id == id_lector: return l
        return None

    def buscar(self, t):
        t = t.strip().lower()
        if not t: return []
        return [l for l in self.lista if t in l.nombre.lower() or t in l.apellido.lower() or t in l.codigo_lector.lower()]

    def siguiente(self):
        return max([l.id for l in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        lector = Lector(
            self.siguiente(), str(datos["nombre"]).strip().title(),
            str(datos["apellido"]).strip().title(), str(datos["email"]).strip().lower(),
            str(datos["codigo_lector"]).strip().upper(), str(datos.get("telefono", "")).strip()
        )
        self.lista.append(lector)
        self.guardar()
        return True, f"Lector creado: {lector.etiqueta()}"

    def actualizar(self, id_lector, datos):
        lector = self.obtener(id_lector)
        if not lector: return False, "No existe el lector"
        error = self.validar(datos, id_lector)
        if error: return False, error
        for k, v in datos.items():
            val = str(v).strip()
            if k in ("nombre", "apellido"): val = val.title()
            elif k == "email": val = val.lower()
            elif k == "codigo_lector": val = val.upper()
            setattr(lector, k, val)
        self.guardar()
        return True, f"Lector {id_lector} actualizado"

    def eliminar(self, id_lector):
        lector = self.obtener(id_lector)
        if not lector: return False, "No existe"
        self.lista.remove(lector)
        self.guardar()
        return True, f"Lector {id_lector} eliminado"


class LibroController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "libros.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Libro.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([lib.a_diccionario() for lib in self.lista])

    def isbns_registrados(self, excepto_id=None):
        return {lib.isbn.strip().upper() for lib in self.lista if lib.id != excepto_id}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("titulo", "isbn", "autor"):
                if str(datos.get(campo, "")).strip() == "": return f"El campo {campo} es obligatorio"
        if "isbn" in datos:
            isbn = str(datos["isbn"]).strip().upper()
            if not Libro.es_isbn_valido(isbn): return "ISBN inválido (muy corto)"
            if isbn in self.isbns_registrados(id_actual): return f"El ISBN '{isbn}' ya está registrado"
        return None

    def leer(self): return self.lista
    def obtener(self, id_libro):
        for lib in self.lista:
            if lib.id == id_libro: return lib
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [lib for lib in self.lista if t in lib.titulo.lower() or t in lib.autor.lower() or t in lib.isbn.lower()]

    def siguiente(self):
        return max([lib.id for lib in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        libro = Libro(
            self.siguiente(), str(datos["titulo"]).strip().title(),
            str(datos["isbn"]).strip().upper(), str(datos["autor"]).strip().title(),
            int(datos["ejemplares_disponibles"]) if str(datos.get("ejemplares_disponibles", "")).strip() != "" else 1
        )
        self.lista.append(libro)
        self.guardar()
        return True, f"Libro registrado: {libro.etiqueta()}"

    def actualizar(self, id_libro, datos):
        libro = self.obtener(id_libro)
        if not libro: return False, "No existe el libro"
        error = self.validar(datos, id_libro)
        if error: return False, error
        if "titulo" in datos: libro.titulo = str(datos["titulo"]).strip().title()
        if "isbn" in datos: libro.isbn = str(datos["isbn"]).strip().upper()
        if "autor" in datos: libro.autor = str(datos["autor"]).strip().title()
        if "ejemplares_disponibles" in datos and str(datos["ejemplares_disponibles"]).strip() != "":
            libro.ejemplares_disponibles = int(datos["ejemplares_disponibles"])
        self.guardar()
        return True, f"Libro {id_libro} actualizado"

    def eliminar(self, id_libro):
        libro = self.obtener(id_libro)
        if not libro: return False, "No existe"
        self.lista.remove(libro)
        self.guardar()
        return True, "Libro eliminado"

    def libros_sin_ejemplares(self):
        return [lib for lib in self.lista if not lib.hay_ejemplares()]


class PrestamoController(CrudBase):
    def __init__(self, lectores, libros, archivo=None):
        self.lectores = lectores
        self.libros = libros
        ruta = archivo or os.path.join(DATA_DIR, "prestamos.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Prestamo.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([p.a_diccionario() for p in self.lista])

    def validar(self, datos):
        try:
            lec_id = int(datos.get("lector_id", 0))
            lib_id = int(datos.get("libro_id", 0))
        except (TypeError, ValueError):
            return "IDs inválidos"
        if not self.lectores.obtener(lec_id): return "No existe el lector"
        libro = self.libros.obtener(lib_id)
        if not libro: return "No existe el libro"
        if not libro.hay_ejemplares(): return f"El libro '{libro.titulo}' no tiene ejemplares disponibles"
        return None

    def leer(self): return self.lista
    def obtener(self, id_prestamo):
        for p in self.lista:
            if p.id == id_prestamo: return p
        return None

    def buscar(self, t):
        return [p for p in self.lista if t.strip() in p.estado or t.strip() in p.fecha_prestamo]

    def siguiente(self):
        return max([p.id for p in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        libro = self.libros.obtener(int(datos["libro_id"]))
        
        prestamo = Prestamo(
            self.siguiente(), int(datos["lector_id"]), libro.id
        )
        libro.prestar_ejemplar()
        self.libros.guardar()
        self.lista.append(prestamo)
        self.guardar()
        return True, f"Préstamo #{prestamo.id} registrado con éxito (Máx. {Libro.MAX_DIAS_PRESTAMO} días)"

    def actualizar(self, id_prestamo, datos): return False, "Use la opción de registrar devolución"

    def eliminar(self, id_prestamo):
        # Eliminar equivale a anular y devolver el ejemplar si estaba activo
        prestamo = self.obtener(id_prestamo)
        if not prestamo: return False, "No existe"
        if prestamo.estado == "Activo":
            libro = self.libros.obtener(prestamo.libro_id)
            if libro:
                libro.devolver_ejemplar()
                self.libros.guardar()
        self.lista.remove(prestamo)
        self.guardar()
        return True, "Préstamo eliminado del registro"

    def registrar_devolucion(self, id_prestamo):
        prestamo = self.obtener(id_prestamo)
        if not prestamo: return False, "No existe el préstamo"
        if prestamo.estado == "Devuelto": return False, "Este libro ya fue devuelto anteriormente"

        prestamo.estado = "Devuelto"
        prestamo.fecha_devolucion = date.today().isoformat()

        libro = self.libros.obtener(prestamo.libro_id)
        if libro:
            libro.devolver_ejemplar()
            self.libros.guardar()

        self.guardar()
        return True, f"Devolución registrada con éxito para el préstamo #{id_prestamo}"

    def comprobante_prestamo(self, id_prestamo):
        prestamo = self.obtener(id_prestamo)
        if not prestamo: return None
        lec = self.lectores.obtener(prestamo.lector_id)
        lib = self.libros.obtener(prestamo.libro_id)
        texto = f"COMPLETO DE PRÉSTAMO #{prestamo.id} · Estado: {prestamo.estado.upper()}\n"
        texto += f"Lector : {lec.nombre_completo() if lec else 'N/A'}   (Código: {lec.codigo_lector if lec else 'N/A'})\n"
        texto += f"Libro  : '{lib.titulo if lib else 'N/A'}' por {lib.autor if lib else 'N/A'}\n"
        texto += "-" * 42 + f"\nF. Préstamo : {prestamo.fecha_prestamo}\n"
        texto += f"F. Devolución: {prestamo.fecha_devolucion}\n"
        texto += f"Plazo límite: {Libro.MAX_DIAS_PRESTAMO} días"
        return texto