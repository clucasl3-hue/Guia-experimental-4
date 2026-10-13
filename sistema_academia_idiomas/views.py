from abc import ABC, abstractmethod
import os

from models import EstudianteIdioma, CursoIdioma, MatriculaCurso
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


class EstudianteIdiomaController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "estudiantes_idiomas.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [EstudianteIdioma.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([e.a_diccionario() for e in self.lista])

    def documentos_registrados(self, excepto_id=None):
        return {e.documento.strip() for e in self.lista if e.id != excepto_id and e.documento}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "apellido", "email", "documento"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"
        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            if not es_email_valido(email): return f"Email inválido: '{email}'"
            if email in {e.email for e in self.lista if e.id != id_actual}:
                return "Ese email ya está registrado"
        if "documento" in datos:
            doc = str(datos["documento"]).strip()
            if doc in self.documentos_registrados(id_actual):
                return f"El documento '{doc}' ya está registrado"
        return None

    def leer(self): return self.lista
    def obtener(self, id_e):
        for e in self.lista:
            if e.id == id_e: return e
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [e for e in self.lista if t in e.nombre.lower() or t in e.apellido.lower() or t in e.documento.lower()]

    def siguiente(self):
        return max([e.id for e in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        estudiante = EstudianteIdioma(
            self.siguiente(), str(datos["nombre"]).strip().title(),
            str(datos["apellido"]).strip().title(), str(datos["email"]).strip().lower(),
            str(datos["documento"]).strip(), str(datos.get("telefono", "")).strip()
        )
        self.lista.append(estudiante)
        self.guardar()
        return True, f"Estudiante registrado: {estudiante.etiqueta()}"

    def actualizar(self, id_e, datos):
        e = self.obtener(id_e)
        if not e: return False, "No existe"
        error = self.validar(datos, id_e)
        if error: return False, error
        for k, v in datos.items():
            val = str(v).strip()
            if k in ("nombre", "apellido"): val = val.title()
            elif k == "email": val = val.lower()
            setattr(e, k, val)
        self.guardar()
        return True, f"Estudiante {id_e} actualizado"

    def eliminar(self, id_e):
        e = self.obtener(id_e)
        if not e: return False, "No existe"
        self.lista.remove(e)
        self.guardar()
        return True, "Estudiante eliminado"


class CursoIdiomaController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "cursos_idiomas.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [CursoIdioma.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([c.a_diccionario() for c in self.lista])

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre_idioma", "nivel", "costo_curso"):
                if str(datos.get(campo, "")).strip() == "": return f"El campo {campo} es obligatorio"
        return None

    def leer(self): return self.lista
    def obtener(self, id_c):
        for c in self.lista:
            if c.id == id_c: return c
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [c for c in self.lista if t in c.nombre_idioma.lower() or t in c.nivel.lower()]

    def siguiente(self):
        return max([c.id for c in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        curso = CursoIdioma(
            self.siguiente(), str(datos["nombre_idioma"]).strip().title(),
            str(datos["nivel"]).strip().upper(), float(datos["costo_curso"])
        )
        self.lista.append(curso)
        self.guardar()
        return True, f"Curso registrado: {curso.etiqueta()}"

    def actualizar(self, id_c, datos):
        c = self.obtener(id_c)
        if not c: return False, "No existe"
        error = self.validar(datos, id_c)
        if error: return False, error
        if "nombre_idioma" in datos: c.nombre_idioma = str(datos["nombre_idioma"]).strip().title()
        if "nivel" in datos: c.nivel = str(datos["nivel"]).strip().upper()
        if "costo_curso" in datos and str(datos["costo_curso"]).strip() != "": c.costo_curso = float(datos["costo_curso"])
        self.guardar()
        return True, "Curso actualizado"

    def eliminar(self, id_c):
        c = self.obtener(id_c)
        if not c: return False, "No existe"
        self.lista.remove(c)
        self.guardar()
        return True, "Curso eliminado"


class MatriculaCursoController(CrudBase):
    def __init__(self, estudiantes, cursos, archivo=None):
        self.estudiantes = estudiantes
        self.cursos = cursos
        ruta = archivo or os.path.join(DATA_DIR, "matriculas_idiomas.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [MatriculaCurso.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([m.a_diccionario() for m in self.lista])

    def validar(self, datos):
        try:
            est_id = int(datos.get("estudiante_id", 0))
            cur_id = int(datos.get("curso_id", 0))
        except (TypeError, ValueError):
            return "IDs inválidos"
        if not self.estudiantes.obtener(est_id): return "No existe el estudiante"
        if not self.cursos.obtener(cur_id): return "No existe el curso"
        return None

    def leer(self): return self.lista
    def obtener(self, id_m):
        for m in self.lista:
            if m.id == id_m: return m
        return None

    def buscar(self, t):
        return [m for m in self.lista if t.strip() in m.fecha_matricula]

    def siguiente(self):
        return max([m.id for m in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        curso = self.cursos.obtener(int(datos["curso_id"]))
        pronto_pago = datos.get("pronto_pago", False)

        costo_total = CursoIdioma.calcular_costo_matricula(curso.costo_curso, pronto_pago)

        matricula = MatriculaCurso(
            self.siguiente(), int(datos["estudiante_id"]), curso.id,
            costo_total, str(datos.get("fecha_matricula", "")).strip()
        )
        self.lista.append(matricula)
        self.guardar()
        return True, f"Matrícula #{matricula.id} registrada con éxito. Total a pagar: ${costo_total:.2f}"

    def actualizar(self, id_m, datos): return False, "Las matrículas no se modifican"

    def eliminar(self, id_m):
        m = self.obtener(id_m)
        if not m: return False, "No existe"
        self.lista.remove(m)
        self.guardar()
        return True, "Matrícula cancelada"

    def comprobante_matricula(self, id_m):
        m = self.obtener(id_m)
        if not m: return None
        e = self.estudiantes.obtener(m.estudiante_id)
        c = self.cursos.obtener(m.curso_id)
        texto = f"COMPROBANTE DE MATRÍCULA IDIOMAS #{m.id}   Fecha: {m.fecha_matricula}\n"
        texto += f"Estudiante: {e.nombre_completo() if e else 'N/A'}   (Doc: {e.documento if e else 'N/A'})\n"
        texto += f"Curso     : {c.nombre_idioma if c else 'N/A'} - Nivel {c.nivel if c else 'N/A'}\n"
        texto += f"Descuento pronto pago si aplica: {CursoIdioma.DESCUENTO_PRONTO_PAGO * 100}%\n"
        texto += "-" * 50 + f"\nTOTAL PAGADO: ${m.costo_total:.2f}"
        return texto

    def total_recaudado(self):
        return round(sum(m.costo_total for m in self.lista), 2)