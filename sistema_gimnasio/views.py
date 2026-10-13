from abc import ABC, abstractmethod
import os
from datetime import date

from models import Socio, ClaseGrupal, InscripcionClase
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


class SocioController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "socios.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Socio.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([s.a_diccionario() for s in self.lista])

    def numeros_socio_registrados(self, excepto_id=None):
        """CONJUNTO para verificar números de socio únicos de forma inmediata."""
        return {s.nro_socio.strip().upper() for s in self.lista if s.id != excepto_id and s.nro_socio}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "apellido", "email", "nro_socio"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"

        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            if not es_email_valido(email): return f"Email inválido: '{email}'"
            if email in {s.email for s in self.lista if s.id != id_actual}:
                return "Ese email ya está registrado"

        if "nro_socio" in datos:
            nro = str(datos["nro_socio"]).strip().upper()
            if nro in self.numeros_socio_registrados(id_actual):
                return f"El número de socio '{nro}' ya existe"
        return None

    def leer(self): return self.lista

    def obtener(self, id_socio):
        for s in self.lista:
            if s.id == id_socio: return s
        return None

    def buscar(self, t):
        t = t.strip().lower()
        if not t: return []
        return [s for s in self.lista if t in s.nombre.lower() or t in s.apellido.lower() or t in s.nro_socio.lower()]

    def siguiente(self):
        return max([s.id for s in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        socio = Socio(
            self.siguiente(), str(datos["nombre"]).strip().title(),
            str(datos["apellido"]).strip().title(), str(datos["email"]).strip().lower(),
            str(datos["nro_socio"]).strip().upper(), str(datos.get("objetivo", "")).strip().capitalize()
        )
        self.lista.append(socio)
        self.guardar()
        return True, f"Socio creado: {socio.etiqueta()}"

    def actualizar(self, id_socio, datos):
        socio = self.obtener(id_socio)
        if not socio: return False, "No existe el socio"
        error = self.validar(datos, id_socio)
        if error: return False, error
        for k, v in datos.items():
            val = str(v).strip()
            if k in ("nombre", "apellido"): val = val.title()
            elif k == "email": val = val.lower()
            elif k == "nro_socio": val = val.upper()
            elif k == "objetivo": val = val.capitalize()
            setattr(socio, k, val)
        self.guardar()
        return True, f"Socio {id_socio} actualizado"

    def eliminar(self, id_socio):
        socio = self.obtener(id_socio)
        if not socio: return False, "No existe"
        self.lista.remove(socio)
        self.guardar()
        return True, f"Socio {id_socio} eliminado"


class ClaseGrupalController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "clases.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [ClaseGrupal.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([c.a_diccionario() for c in self.lista])

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre_clase", "horario", "instructor"):
                if str(datos.get(campo, "")).strip() == "": return f"El campo {campo} es obligatorio"
        if "horario" in datos:
            horario = str(datos["horario"]).strip()
            if not ClaseGrupal.es_horario_valido(horario): return "Horario inválido"
        return None

    def leer(self): return self.lista
    def obtener(self, id_clase):
        for c in self.lista:
            if c.id == id_clase: return c
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [c for c in self.lista if t in c.nombre_clase.lower() or t in c.instructor.lower()]

    def siguiente(self):
        return max([c.id for c in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        clase = ClaseGrupal(
            self.siguiente(), str(datos["nombre_clase"]).strip().title(),
            str(datos["horario"]).strip(), str(datos["instructor"]).strip().title(),
            int(datos["cupos_maximos"]) if str(datos.get("cupos_maximos", "")).strip() != "" else ClaseGrupal.CUPOS_DEFAULT
        )
        self.lista.append(clase)
        self.guardar()
        return True, f"Clase creada: {clase.etiqueta()}"

    def actualizar(self, id_clase, datos):
        clase = self.obtener(id_clase)
        if not clase: return False, "No existe"
        error = self.validar(datos, id_clase)
        if error: return False, error
        if "nombre_clase" in datos: clase.nombre_clase = str(datos["nombre_clase"]).strip().title()
        if "horario" in datos: clase.horario = str(datos["horario"]).strip()
        if "instructor" in datos: clase.instructor = str(datos["instructor"]).strip().title()
        if "cupos_maximos" in datos and str(datos["cupos_maximos"]).strip() != "":
            clase.cupos_maximos = int(datos["cupos_maximos"])
        self.guardar()
        return True, f"Clase {id_clase} actualizada"

    def eliminar(self, id_clase):
        clase = self.obtener(id_clase)
        if not clase: return False, "No existe"
        self.lista.remove(clase)
        self.guardar()
        return True, "Clase eliminada"

    def clases_sin_cupo(self):
        return [c for c in self.lista if not c.hay_cupo()]


class InscripcionClaseController(CrudBase):
    def __init__(self, socios, clases, archivo=None):
        self.socios = socios
        self.clases = clases
        ruta = archivo or os.path.join(DATA_DIR, "inscripciones.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [InscripcionClase.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([i.a_diccionario() for i in self.lista])

    def validar(self, datos):
        try:
            soc_id = int(datos.get("socio_id", 0))
            cls_id = int(datos.get("clase_id", 0))
        except (TypeError, ValueError):
            return "IDs inválidos"
        if not self.socios.obtener(soc_id): return "No existe el socio"
        clase = self.clases.obtener(cls_id)
        if not clase: return "No existe la clase grupal"
        
        # Validar si ya está inscrito en esa misma clase
        for ins in self.lista:
            if ins.socio_id == soc_id and ins.clase_id == cls_id:
                return "El socio ya está inscrito en esta clase"

        if not clase.hay_cupo(): return f"La clase '{clase.nombre_clase}' no tiene cupos disponibles"
        return None

    def leer(self): return self.lista
    def obtener(self, id_inscripcion):
        for i in self.lista:
            if i.id == id_inscripcion: return i
        return None

    def buscar(self, t):
        return [i for i in self.lista if t.strip() in i.fecha_inscripcion]

    def siguiente(self):
        return max([i.id for i in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        clase = self.clases.obtener(int(datos["clase_id"]))
        
        inscripcion = InscripcionClase(
            self.siguiente(), int(datos["socio_id"]), clase.id
        )
        clase.ocupar_cupo()
        self.clases.guardar()
        self.lista.append(inscripcion)
        self.guardar()
        return True, f"Inscripción #{inscripcion.id} registrada con éxito"

    def actualizar(self, id_inscripcion, datos): return False, "Las inscripciones no se modifican"

    def eliminar(self, id_inscripcion):
        inscripcion = self.obtener(id_inscripcion)
        if not inscripcion: return False, "No existe"
        clase = self.clases.obtener(inscripcion.clase_id)
        if clase:
            clase.liberar_cupo()
            self.clases.guardar()
        self.lista.remove(inscripcion)
        self.guardar()
        return True, "Inscripción cancelada y cupo liberado"

    def comprobante_inscripcion(self, id_inscripcion):
        ins = self.obtener(id_inscripcion)
        if not ins: return None
        soc = self.socios.obtener(ins.socio_id)
        clase = self.clases.obtener(ins.clase_id)
        texto = f"COMPROBANTE DE INSCRIPCIÓN #{ins.id} · Fecha: {ins.fecha_inscripcion}\n"
        texto += f"Socio : {soc.nombre_completo() if soc else 'N/A'}   (Nro: {soc.nro_socio if soc else 'N/A'})\n"
        texto += f"Clase : {clase.nombre_clase if clase else 'N/A'} ({clase.horario if clase else 'N/A'})\n"
        texto += f"Instr : {clase.instructor if clase else 'N/A'}\n"
        texto += "-" * 42 + f"\nEstado: Activo en el sistema"
        return texto