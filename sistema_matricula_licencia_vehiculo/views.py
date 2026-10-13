from abc import ABC, abstractmethod
import os

from models import Conductor, TipoTramite, TurnoLicencia
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


class ConductorController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "conductores.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Conductor.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([c.a_diccionario() for c in self.lista])

    def licencias_registradas(self, excepto_id=None):
        """CONJUNTO para verificar números de licencia únicos instantáneamente."""
        return {c.licencia.strip().upper() for c in self.lista if c.id != excepto_id and c.licencia}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "apellido", "email", "licencia"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"

        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            if not es_email_valido(email): return f"Email inválido: '{email}'"
            if email in {c.email for c in self.lista if c.id != id_actual}:
                return "Ese email ya está registrado"

        if "licencia" in datos:
            lic = str(datos["licencia"]).strip().upper()
            if lic in self.licencias_registradas(id_actual):
                return f"La licencia '{lic}' ya está registrada"
        return None

    def leer(self): return self.lista

    def obtener(self, id_conductor):
        for c in self.lista:
            if c.id == id_conductor: return c
        return None

    def buscar(self, t):
        t = t.strip().lower()
        if not t: return []
        return [c for c in self.lista if t in c.nombre.lower() or t in c.apellido.lower() or t in c.licencia.lower()]

    def siguiente(self):
        return max([c.id for c in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        conductor = Conductor(
            self.siguiente(), str(datos["nombre"]).strip().title(),
            str(datos["apellido"]).strip().title(), str(datos["email"]).strip().lower(),
            str(datos["licencia"]).strip().upper(), str(datos.get("tipo_sangre", "")).strip().upper()
        )
        self.lista.append(conductor)
        self.guardar()
        return True, f"Conductor registrado: {conductor.etiqueta()}"

    def actualizar(self, id_conductor, datos):
        conductor = self.obtener(id_conductor)
        if not conductor: return False, "No existe el conductor"
        error = self.validar(datos, id_conductor)
        if error: return False, error
        for k, v in datos.items():
            val = str(v).strip()
            if k in ("nombre", "apellido"): val = val.title()
            elif k == "email": val = val.lower()
            elif k in ("licencia", "tipo_sangre"): val = val.upper()
            setattr(conductor, k, val)
        self.guardar()
        return True, f"Conductor {id_conductor} actualizado"

    def eliminar(self, id_conductor):
        conductor = self.obtener(id_conductor)
        if not conductor: return False, "No existe"
        self.lista.remove(conductor)
        self.guardar()
        return True, f"Conductor {id_conductor} eliminado"


class TipoTramiteController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "tipos_tramite.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [TipoTramite.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([t.a_diccionario() for t in self.lista])

    def codigos_registrados(self, excepto_id=None):
        return {t.codigo.strip().upper() for t in self.lista if t.id != excepto_id and t.codigo}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre_tramite", "codigo", "costo_base"):
                if str(datos.get(campo, "")).strip() == "": return f"El campo {campo} es obligatorio"
        if "codigo" in datos:
            cod = str(datos["codigo"]).strip().upper()
            if cod in self.codigos_registrados(id_actual): return f"El código de trámite '{cod}' ya existe"
        return None

    def leer(self): return self.lista
    def obtener(self, id_tramite):
        for t in self.lista:
            if t.id == id_tramite: return t
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [tr for tr in self.lista if t in tr.nombre_tramite.lower() or t in tr.codigo.lower()]

    def siguiente(self):
        return max([t.id for t in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        tramite = TipoTramite(
            self.siguiente(), str(datos["nombre_tramite"]).strip().title(),
            str(datos["codigo"]).strip().upper(), float(datos["costo_base"])
        )
        self.lista.append(tramite)
        self.guardar()
        return True, f"Trámite registrado: {tramite.etiqueta()}"

    def actualizar(self, id_tramite, datos):
        tramite = self.obtener(id_tramite)
        if not tramite: return False, "No existe"
        error = self.validar(datos, id_tramite)
        if error: return False, error
        if "nombre_tramite" in datos: tramite.nombre_tramite = str(datos["nombre_tramite"]).strip().title()
        if "codigo" in datos: tramite.codigo = str(datos["codigo"]).strip().upper()
        if "costo_base" in datos and str(datos["costo_base"]).strip() != "": tramite.costo_base = float(datos["costo_base"])
        self.guardar()
        return True, f"Trámite {id_tramite} actualizado"

    def eliminar(self, id_tramite):
        tramite = self.obtener(id_tramite)
        if not tramite: return False, "No existe"
        self.lista.remove(tramite)
        self.guardar()
        return True, "Trámite eliminado"


class TurnoLicenciaController(CrudBase):
    def __init__(self, conductores, tramites, archivo=None):
        self.conductores = conductores
        self.tramites = tramites
        ruta = archivo or os.path.join(DATA_DIR, "turnos_licencias.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [TurnoLicencia.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([t.a_diccionario() for t in self.lista])

    def validar(self, datos):
        try:
            con_id = int(datos.get("conductor_id", 0))
            tra_id = int(datos.get("tramite_id", 0))
            atraso = int(datos.get("dias_atraso", 0))
        except (TypeError, ValueError):
            return "Datos numéricos inválidos"
        if not self.conductores.obtener(con_id): return "No existe el conductor"
        if not self.tramites.obtener(tra_id): return "No existe el tipo de trámite"
        if atraso < 0: return "Los días de atraso no pueden ser negativos"
        return None

    def leer(self): return self.lista
    def obtener(self, id_turno):
        for t in self.lista:
            if t.id == id_turno: return t
        return None

    def buscar(self, t):
        return [tr for tr in self.lista if t.strip() in tr.fecha_asignada or t.strip() in tr.estado_pago.lower()]

    def siguiente(self):
        return max([t.id for t in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        tramite = self.tramites.obtener(int(datos["tramite_id"]))
        atraso = int(datos.get("dias_atraso", 0))

        # Cálculo estático con multas
        total_pagar = TipoTramite.calcular_total_con_multa(tramite.costo_base, atraso)

        turno = TurnoLicencia(
            self.siguiente(), int(datos["conductor_id"]), tramite.id,
            str(datos.get("fecha_asignada", "")).strip(), atraso, total_pagar, "Pagado"
        )
        self.lista.append(turno)
        self.guardar()
        return True, f"Turno #{turno.id} asignado con éxito. Total (incl. multas si aplica): ${total_pagar:.2f}"

    def actualizar(self, id_turno, datos): return False, "Los turnos no se modifican"

    def eliminar(self, id_turno):
        turno = self.obtener(id_turno)
        if not turno: return False, "No existe"
        self.lista.remove(turno)
        self.guardar()
        return True, "Turno cancelado del sistema"

    def comprobante_turno(self, id_turno):
        turno = self.obtener(id_turno)
        if not turno: return None
        con = self.conductores.obtener(turno.conductor_id)
        tra = self.tramites.obtener(turno.tramite_id)
        texto = f"COMPROBANTE DE TRÁNSITO - TURNO #{turno.id}   Fecha: {turno.fecha_asignada}\n"
        texto += f"Conductor: {con.nombre_completo() if con else 'N/A'}   (Licencia: {con.licencia if con else 'N/A'})\n"
        texto += f"Trámite  : {tra.nombre_tramite if tra else 'N/A'} [{tra.codigo if tra else 'N/A'}]\n"
        texto += f"Días atraso multas: {turno.dias_atraso} (Multa/día: ${TipoTramite.COSTO_MULTA_ATRASO:.2f})\n"
        texto += "-" * 50 + f"\nESTADO: {turno.estado_pago.upper()}   ·   TOTAL PAGADO: ${turno.total_pagado:.2f}"
        return texto

    def total_recaudado(self):
        return round(sum(t.total_pagado for t in self.lista), 2)