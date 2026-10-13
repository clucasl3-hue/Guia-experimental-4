from abc import ABC, abstractmethod
import os

from models import Paciente, Doctor, CitaMedica
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


class PacienteController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "pacientes.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Paciente.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([p.a_diccionario() for p in self.lista])

    def cedulas_registradas(self, excepto_id=None):
        """CONJUNTO para verificar cédulas únicas de forma instantánea."""
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
            cedula = str(datos["cedula"]).strip()
            if cedula in self.cedulas_registradas(id_actual):
                return f"La cédula '{cedula}' ya está registrada"
        return None

    def leer(self): return self.lista

    def obtener(self, id_paciente):
        for p in self.lista:
            if p.id == id_paciente: return p
        return None

    def buscar(self, t):
        t = t.strip().lower()
        if not t: return []
        return [p for p in self.lista if t in p.nombre.lower() or t in p.apellido.lower() or t in p.cedula.lower()]

    def siguiente(self):
        return max([p.id for p in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        paciente = Paciente(
            self.siguiente(), str(datos["nombre"]).strip().title(),
            str(datos["apellido"]).strip().title(), str(datos["email"]).strip().lower(),
            str(datos["cedula"]).strip(), str(datos.get("tipo_sangre", "")).strip().upper()
        )
        self.lista.append(paciente)
        self.guardar()
        return True, f"Paciente creado: {paciente.etiqueta()}"

    def actualizar(self, id_paciente, datos):
        paciente = self.obtener(id_paciente)
        if not paciente: return False, "No existe el paciente"
        error = self.validar(datos, id_paciente)
        if error: return False, error
        for k, v in datos.items():
            val = str(v).strip()
            if k in ("nombre", "apellido"): val = val.title()
            elif k == "email": val = val.lower()
            elif k == "tipo_sangre": val = val.upper()
            setattr(paciente, k, val)
        self.guardar()
        return True, f"Paciente {id_paciente} actualizado"

    def eliminar(self, id_paciente):
        paciente = self.obtener(id_paciente)
        if not paciente: return False, "No existe"
        self.lista.remove(paciente)
        self.guardar()
        return True, f"Paciente {id_paciente} eliminado"

    def tipos_sangre_unicos(self):
        return sorted({p.tipo_sangre for p in self.lista if p.tipo_sangre})


class DoctorController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "doctores.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Doctor.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([d.a_diccionario() for d in self.lista])

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre_doctor", "especialidad", "consultorio"):
                if str(datos.get(campo, "")).strip() == "": return f"El campo {campo} es obligatorio"
        if "costo" in datos and str(datos["costo"]).strip() != "":
            if not Doctor.es_costo_valido(datos["costo"]):
                return "El costo de la consulta debe ser mayor a 0"
        return None

    def leer(self): return self.lista
    def obtener(self, id_doctor):
        for d in self.lista:
            if d.id == id_doctor: return d
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [d for d in self.lista if t in d.nombre_doctor.lower() or t in d.especialidad.lower()]

    def siguiente(self):
        return max([d.id for d in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        doctor = Doctor(
            self.siguiente(), str(datos["nombre_doctor"]).strip().title(),
            str(datos["especialidad"]).strip().title(), str(datos["consultorio"]).strip().upper(),
            float(datos["costo"]) if str(datos.get("costo", "")).strip() != "" else Doctor.COSTO_BASE
        )
        self.lista.append(doctor)
        self.guardar()
        return True, f"Doctor registrado: {doctor.etiqueta()}"

    def actualizar(self, id_doctor, datos):
        doctor = self.obtener(id_doctor)
        if not doctor: return False, "No existe"
        error = self.validar(datos, id_doctor)
        if error: return False, error
        if "nombre_doctor" in datos: doctor.nombre_doctor = str(datos["nombre_doctor"]).strip().title()
        if "especialidad" in datos: doctor.especialidad = str(datos["especialidad"]).strip().title()
        if "consultorio" in datos: doctor.consultorio = str(datos["consultorio"]).strip().upper()
        if "costo" in datos and str(datos["costo"]).strip() != "": doctor.costo = float(datos["costo"])
        self.guardar()
        return True, f"Doctor {id_doctor} actualizado"

    def eliminar(self, id_doctor):
        doctor = self.obtener(id_doctor)
        if not doctor: return False, "No existe"
        self.lista.remove(doctor)
        self.guardar()
        return True, "Doctor eliminado"


class CitaMedicaController(CrudBase):
    def __init__(self, pacientes, doctores, archivo=None):
        self.pacientes = pacientes
        self.doctores = doctores
        ruta = archivo or os.path.join(DATA_DIR, "citas.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [CitaMedica.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([c.a_diccionario() for c in self.lista])

    def validar(self, datos):
        try:
            pac_id = int(datos.get("paciente_id", 0))
            doc_id = int(datos.get("doctor_id", 0))
        except (TypeError, ValueError):
            return "IDs inválidos"
        if not self.pacientes.obtener(pac_id): return "No existe el paciente"
        if not self.doctores.obtener(doc_id): return "No existe el doctor"
        if not str(datos.get("fecha", "")).strip(): return "La fecha es obligatoria"
        return None

    def leer(self): return self.lista
    def obtener(self, id_cita):
        for c in self.lista:
            if c.id == id_cita: return c
        return None

    def buscar(self, t):
        return [c for c in self.lista if t.strip() in c.fecha]

    def siguiente(self):
        return max([c.id for c in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        doctor = self.doctores.obtener(int(datos["doctor_id"]))
        
        # Opcional: descuento de tercera edad (pedir 'si' o 'no')
        es_tercera = datos.get("es_tercera_edad", False)
        valor_final = Doctor.calcular_con_descuento_tercera_edad(doctor.costo, es_tercera)

        cita = CitaMedica(
            self.siguiente(), int(datos["paciente_id"]), doctor.id,
            str(datos["fecha"]).strip(), str(datos.get("sintomas", "")).strip(), valor_final
        )
        self.lista.append(cita)
        self.guardar()
        return True, f"Cita #{cita.id} agendada con éxito por ${valor_final:.2f}"

    def actualizar(self, id_cita, datos): return False, "Las citas no se modifican directamente: cancélela y agende otra"

    def eliminar(self, id_cita):
        cita = self.obtener(id_cita)
        if not cita: return False, "No existe"
        self.lista.remove(cita)
        self.guardar()
        return True, "Cita médica cancelada"

    def comprobante_cita(self, id_cita):
        cita = self.obtener(id_cita)
        if not cita: return None
        pac = self.pacientes.obtener(cita.paciente_id)
        doc = self.doctores.obtener(cita.doctor_id)
        texto = f"COMPROBANTE DE CITA #{cita.id}   Fecha: {cita.fecha}\n"
        texto += f"Paciente: {pac.nombre_completo() if pac else 'N/A'}   (Cédula: {pac.cedula if pac else 'N/A'})\n"
        texto += f"Doctor  : Dr(a). {doc.nombre_doctor if doc else 'N/A'} - {doc.especialidad if doc else 'N/A'}\n"
        texto += f"Consultorio: {doc.consultorio if doc else 'N/A'}\n"
        texto += "-" * 42 + f"\nSíntomas: {cita.sintomas or 'Ninguno'}\n"
        texto += f"TOTAL PAGADO: ${cita.valor_pagado:.2f}"
        return texto

    def total_recaudado(self):
        return round(sum(c.valor_pagado for c in self.lista), 2)