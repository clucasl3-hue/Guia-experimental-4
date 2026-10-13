from abc import ABC, abstractmethod
import os

from models import AtletaDojo, ClaseMarcial, InscripcionDojo
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


class AtletaDojoController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "atletas_dojo.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [AtletaDojo.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([a.a_diccionario() for a in self.lista])

    def socios_registrados(self, excepto_id=None):
        return {a.socio_id.strip().upper() for a in self.lista if a.id != excepto_id and a.socio_id}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "apellido", "email", "socio_id"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"
        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            if not es_email_valido(email): return f"Email inválido: '{email}'"
            if email in {a.email for a in self.lista if a.id != id_actual}:
                return "Ese email ya está registrado"
        if "socio_id" in datos:
            socio = str(datos["socio_id"]).strip().upper()
            if socio in self.socios_registrados(id_actual):
                return f"El ID de socio '{socio}' ya está registrado"
        return None

    def leer(self): return self.lista
    def obtener(self, id_a):
        for a in self.lista:
            if a.id == id_a: return a
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [a for a in self.lista if t in a.nombre.lower() or t in a.apellido.lower() or t in a.socio_id.lower()]

    def siguiente(self):
        return max([a.id for a in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        atleta = AtletaDojo(
            self.siguiente(), str(datos["nombre"]).strip().title(),
            str(datos["apellido"]).strip().title(), str(datos["email"]).strip().lower(),
            str(datos.get("cinturon", "Blanco")).strip().title(), str(datos["socio_id"]).strip().upper()
        )
        self.lista.append(atleta)
        self.guardar()
        return True, f"Atleta registrado: {atleta.etiqueta()}"

    def actualizar(self, id_a, datos):
        a = self.obtener(id_a)
        if not a: return False, "No existe"
        error = self.validar(datos, id_a)
        if error: return False, error
        for k, v in datos.items():
            val = str(v).strip()
            if k in ("nombre", "apellido", "cinturon"): val = val.title()
            elif k == "email": val = val.lower()
            elif k == "socio_id": val = val.upper()
            setattr(a, k, val)
        self.guardar()
        return True, f"Atleta {id_a} actualizado"

    def eliminar(self, id_a):
        a = self.obtener(id_a)
        if not a: return False, "No existe"
        self.lista.remove(a)
        self.guardar()
        return True, "Atleta eliminado"


class ClaseMarcialController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "clases_marciales.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [ClaseMarcial.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([c.a_diccionario() for c in self.lista])

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre_clase", "estilo", "costo_mensual"):
                if str(datos.get(campo, "")).strip() == "": return f"El campo {campo} es obligatorio"
        return None

    def leer(self): return self.lista
    def obtener(self, id_c):
        for c in self.lista:
            if c.id == id_c: return c
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [c for c in self.lista if t in c.nombre_clase.lower() or t in c.estilo.lower()]

    def siguiente(self):
        return max([c.id for c in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        clase = ClaseMarcial(
            self.siguiente(), str(datos["nombre_clase"]).strip().title(),
            str(datos["estilo"]).strip().title(), float(datos["costo_mensual"])
        )
        self.lista.append(clase)
        self.guardar()
        return True, f"Clase registrada: {clase.etiqueta()}"

    def actualizar(self, id_c, datos):
        c = self.obtener(id_c)
        if not c: return False, "No existe"
        error = self.validar(datos, id_c)
        if error: return False, error
        if "nombre_clase" in datos: c.nombre_clase = str(datos["nombre_clase"]).strip().title()
        if "estilo" in datos: c.estilo = str(datos["estilo"]).strip().title()
        if "costo_mensual" in datos and str(datos["costo_mensual"]).strip() != "": c.costo_mensual = float(datos["costo_mensual"])
        self.guardar()
        return True, "Clase actualizada"

    def eliminar(self, id_c):
        c = self.obtener(id_c)
        if not c: return False, "No existe"
        self.lista.remove(c)
        self.guardar()
        return True, "Clase eliminada"


class InscripcionDojoController(CrudBase):
    def __init__(self, atletas, clases, archivo=None):
        self.atletas = atletas
        self.clases = clases
        ruta = archivo or os.path.join(DATA_DIR, "inscripciones_dojo.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [InscripcionDojo.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([i.a_diccionario() for i in self.lista])

    def validar(self, datos):
        try:
            atl_id = int(datos.get("atleta_id", 0))
            cls_id = int(datos.get("clase_id", 0))
        except (TypeError, ValueError):
            return "IDs inválidos"
        if not self.atletas.obtener(atl_id): return "No existe el atleta"
        if not self.clases.obtener(cls_id): return "No existe la clase marcial"
        return None

    def leer(self): return self.lista
    def obtener(self, id_i):
        for i in self.lista:
            if i.id == id_i: return i
        return None

    def buscar(self, t):
        return [i for i in self.lista if t.strip() in i.fecha_inscripcion]

    def siguiente(self):
        return max([i.id for i in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        clase = self.clases.obtener(int(datos["clase_id"]))
        con_promo = datos.get("con_promo", False)

        total_pagar = ClaseMarcial.calcular_costo_inscripcion(clase.costo_mensual, con_promo)

        inscripcion = InscripcionDojo(
            self.siguiente(), int(datos["atleta_id"]), clase.id,
            total_pagar, str(datos.get("fecha_inscripcion", "")).strip()
        )
        self.lista.append(inscripcion)
        self.guardar()
        return True, f"Inscripción #{inscripcion.id} registrada con éxito. Total a pagar: ${total_pagar:.2f}"

    def actualizar(self, id_i, datos): return False, "Las inscripciones no se modifican"

    def eliminar(self, id_i):
        i = self.obtener(id_i)
        if not i: return False, "No existe"
        self.lista.remove(i)
        self.guardar()
        return True, "Inscripción cancelada"

    def comprobante_inscripcion(self, id_i):
        i = self.obtener(id_i)
        if not i: return None
        a = self.atletas.obtener(i.atleta_id)
        c = self.clases.obtener(i.clase_id)
        texto = f"COMPROBANTE DOJO / INSCRIPCIÓN #{i.id}   Fecha: {i.fecha_inscripcion}\n"
        texto += f"Atleta: {a.nombre_completo() if a else 'N/A'}   (Socio ID: {a.socio_id if a else 'N/A'})\n"
        texto += f"Clase : {c.nombre_clase if c else 'N/A'} [{c.estilo if c else 'N/A'}]\n"
        texto += f"Descuento aplicado si aplica: {ClaseMarcial.DESCUENTO_PROMOCION * 100}%\n"
        texto += "-" * 50 + f"\nTOTAL PAGADO: ${i.total_pagar:.2f}"
        return texto

    def total_recaudado(self):
        return round(sum(i.total_pagar for i in self.lista), 2)