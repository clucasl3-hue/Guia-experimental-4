from abc import ABC, abstractmethod
import os

from models import PacienteDental, TratamientoDental, CitaDental
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


class PacienteDentalController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "pacientes_dental.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [PacienteDental.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([p.a_diccionario() for p in self.lista])

    def cedulas_registradas(self, excepto_id=None):
        return {p.cedula.strip() for p in self.lista if p.id != excepto_id and p.cedula}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "apellido", "email", "cedula"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"
        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            if not es_email_valido(email): return f"Email inválido: '{email}'"
            if email in {p.email for p in self.lista if p.id != id_actual}:
                return "Ese email ya está registrado"
        if "cedula" in datos:
            ced = str(datos["cedula"]).strip()
            if ced in self.cedulas_registradas(id_actual):
                return f"La cédula '{ced}' ya está registrada"
        return None

    def leer(self): return self.lista
    def obtener(self, id_p):
        for p in self.lista:
            if p.id == id_p: return p
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [p for p in self.lista if t in p.nombre.lower() or t in p.apellido.lower() or t in p.cedula.lower()]

    def siguiente(self):
        return max([p.id for p in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        paciente = PacienteDental(
            self.siguiente(), str(datos["nombre"]).strip().title(),
            str(datos["apellido"]).strip().title(), str(datos["email"]).strip().lower(),
            str(datos["cedula"]).strip(), str(datos.get("telefono", "")).strip()
        )
        self.lista.append(paciente)
        self.guardar()
        return True, f"Paciente registrado: {paciente.etiqueta()}"

    def actualizar(self, id_p, datos):
        paciente = self.obtener(id_p)
        if not paciente: return False, "No existe"
        error = self.validar(datos, id_p)
        if error: return False, error
        for k, v in datos.items():
            val = str(v).strip()
            if k in ("nombre", "apellido"): val = val.title()
            elif k == "email": val = val.lower()
            setattr(paciente, k, val)
        self.guardar()
        return True, f"Paciente {id_p} actualizado"

    def eliminar(self, id_p):
        paciente = self.obtener(id_p)
        if not paciente: return False, "No existe"
        self.lista.remove(paciente)
        self.guardar()
        return True, "Paciente eliminado"


class TratamientoDentalController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "tratamientos_dental.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [TratamientoDental.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([t.a_diccionario() for t in self.lista])

    def codigos_registrados(self, excepto_id=None):
        return {t.codigo.strip().upper() for t in self.lista if t.id != excepto_id and t.codigo}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre_tratamiento", "codigo", "costo_base"):
                if str(datos.get(campo, "")).strip() == "": return f"El campo {campo} es obligatorio"
        if "codigo" in datos:
            cod = str(datos["codigo"]).strip().upper()
            if cod in self.codigos_registrados(id_actual): return f"El código '{cod}' ya existe"
        return None

    def leer(self): return self.lista
    def obtener(self, id_t):
        for t in self.lista:
            if t.id == id_t: return t
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [tr for tr in self.lista if t in tr.nombre_tratamiento.lower() or t in tr.codigo.lower()]

    def siguiente(self):
        return max([t.id for t in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        tratamiento = TratamientoDental(
            self.siguiente(), str(datos["nombre_tratamiento"]).strip().title(),
            str(datos["codigo"]).strip().upper(), float(datos["costo_base"])
        )
        self.lista.append(tratamiento)
        self.guardar()
        return True, f"Tratamiento registrado: {tratamiento.etiqueta()}"

    def actualizar(self, id_t, datos):
        t = self.obtener(id_t)
        if not t: return False, "No existe"
        error = self.validar(datos, id_t)
        if error: return False, error
        if "nombre_tratamiento" in datos: t.nombre_tratamiento = str(datos["nombre_tratamiento"]).strip().title()
        if "codigo" in datos: t.codigo = str(datos["codigo"]).strip().upper()
        if "costo_base" in datos and str(datos["costo_base"]).strip() != "": t.costo_base = float(datos["costo_base"])
        self.guardar()
        return True, "Tratamiento actualizado"

    def eliminar(self, id_t):
        t = self.obtener(id_t)
        if not t: return False, "No existe"
        self.lista.remove(t)
        self.guardar()
        return True, "Tratamiento eliminado"


class CitaDentalController(CrudBase):
    def __init__(self, pacientes, tratamientos, archivo=None):
        self.pacientes = pacientes
        self.tratamientos = tratamientos
        ruta = archivo or os.path.join(DATA_DIR, "citas_dental.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [CitaDental.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([c.a_diccionario() for c in self.lista])

    def validar(self, datos):
        try:
            pac_id = int(datos.get("paciente_id", 0))
            tra_id = int(datos.get("tratamiento_id", 0))
        except (TypeError, ValueError):
            return "IDs inválidos"
        if not self.pacientes.obtener(pac_id): return "No existe el paciente"
        if not self.tratamientos.obtener(tra_id): return "No existe el tratamiento"
        return None

    def leer(self): return self.lista
    def obtener(self, id_c):
        for c in self.lista:
            if c.id == id_c: return c
        return None

    def buscar(self, t):
        return [c for c in self.lista if t.strip() in c.fecha_cita or t.strip() in c.estado.lower()]

    def siguiente(self):
        return max([c.id for c in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        tratamiento = self.tratamientos.obtener(int(datos["tratamiento_id"]))
        con_seguro = datos.get("con_seguro", False)

        costo_final = TratamientoDental.calcular_costo_final(tratamiento.costo_base, con_seguro)

        cita = CitaDental(
            self.siguiente(), int(datos["paciente_id"]), tratamiento.id,
            str(datos.get("fecha_cita", "")).strip(), costo_final, "Confirmada"
        )
        self.lista.append(cita)
        self.guardar()
        return True, f"Cita #{cita.id} registrada con éxito. Total: ${costo_final:.2f}"

    def actualizar(self, id_c, datos): return False, "Las citas no se modifican directamente"

    def eliminar(self, id_c):
        c = self.obtener(id_c)
        if not c: return False, "No existe"
        self.lista.remove(c)
        self.guardar()
        return True, "Cita cancelada"

    def comprobante_cita(self, id_c):
        c = self.obtener(id_c)
        if not c: return None
        p = self.pacientes.obtener(c.paciente_id)
        t = self.tratamientos.obtener(c.tratamiento_id)
        texto = f"COMPROBANTE CLÍNICA DENTAL - CITA #{c.id}   Fecha: {c.fecha_cita}\n"
        texto += f"Paciente : {p.nombre_completo() if p else 'N/A'}   (Cédula: {p.cedula if p else 'N/A'})\n"
        texto += f"Tratamiento: {t.nombre_tratamiento if t else 'N/A'} [{t.codigo if t else 'N/A'}]\n"
        texto += "-" * 50 + f"\nESTADO: {c.estado.upper()}   ·   TOTAL COBRADO: ${c.costo_final:.2f}"
        return texto

    def total_recaudado(self):
        return round(sum(c.costo_final for c in self.lista), 2)