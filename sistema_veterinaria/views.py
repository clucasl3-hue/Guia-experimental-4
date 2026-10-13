from abc import ABC, abstractmethod
import os

from models import Duenio, ServicioVeterinario, HistorialAtencion
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


class DuenioController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "duenios.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Duenio.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([d.a_diccionario() for d in self.lista])

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "apellido", "email"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"

        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            if not es_email_valido(email): return f"Email inválido: '{email}'"
            if email in {d.email for d in self.lista if d.id != id_actual}:
                return "Ese email ya está registrado"
        return None

    def leer(self): return self.lista

    def obtener(self, id_duenio):
        for d in self.lista:
            if d.id == id_duenio: return d
        return None

    def buscar(self, t):
        t = t.strip().lower()
        if not t: return []
        return [d for d in self.lista if t in d.nombre.lower() or t in d.apellido.lower() or t in d.email.lower()]

    def siguiente(self):
        return max([d.id for d in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        duenio = Duenio(
            self.siguiente(), str(datos["nombre"]).strip().title(),
            str(datos["apellido"]).strip().title(), str(datos["email"]).strip().lower(),
            str(datos.get("telefono", "")).strip(), str(datos.get("direccion", "")).strip().title()
        )
        self.lista.append(duenio)
        self.guardar()
        return True, f"Dueño registrado: {duenio.etiqueta()}"

    def actualizar(self, id_duenio, datos):
        duenio = self.obtener(id_duenio)
        if not duenio: return False, "No existe el dueño"
        error = self.validar(datos, id_duenio)
        if error: return False, error
        for k, v in datos.items():
            val = str(v).strip()
            if k in ("nombre", "apellido", "direccion"): val = val.title()
            elif k == "email": val = val.lower()
            setattr(duenio, k, val)
        self.guardar()
        return True, f"Dueño {id_duenio} actualizado"

    def eliminar(self, id_duenio):
        duenio = self.obtener(id_duenio)
        if not duenio: return False, "No existe"
        self.lista.remove(duenio)
        self.guardar()
        return True, f"Dueño {id_duenio} eliminado"


class ServicioVeterinarioController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "servicios.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [ServicioVeterinario.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([s.a_diccionario() for s in self.lista])

    def codigos_registrados(self, excepto_id=None):
        """CONJUNTO para verificar códigos de servicio únicos instantáneamente."""
        return {s.codigo.strip().upper() for s in self.lista if s.id != excepto_id and s.codigo}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre_servicio", "codigo", "costo"):
                if str(datos.get(campo, "")).strip() == "": return f"El campo {campo} es obligatorio"
        if "codigo" in datos:
            cod = str(datos["codigo"]).strip().upper()
            if cod in self.codigos_registrados(id_actual): return f"El código de servicio '{cod}' ya existe"
        return None

    def leer(self): return self.lista
    def obtener(self, id_servicio):
        for s in self.lista:
            if s.id == id_servicio: return s
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [s for s in self.lista if t in s.nombre_servicio.lower() or t in s.codigo.lower()]

    def siguiente(self):
        return max([s.id for s in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        servicio = ServicioVeterinario(
            self.siguiente(), str(datos["nombre_servicio"]).strip().title(),
            str(datos["codigo"]).strip().upper(), float(datos["costo"])
        )
        self.lista.append(servicio)
        self.guardar()
        return True, f"Servicio registrado: {servicio.etiqueta()}"

    def actualizar(self, id_servicio, datos):
        servicio = self.obtener(id_servicio)
        if not servicio: return False, "No existe"
        error = self.validar(datos, id_servicio)
        if error: return False, error
        if "nombre_servicio" in datos: servicio.nombre_servicio = str(datos["nombre_servicio"]).strip().title()
        if "codigo" in datos: servicio.codigo = str(datos["codigo"]).strip().upper()
        if "costo" in datos and str(datos["costo"]).strip() != "": servicio.costo = float(datos["costo"])
        self.guardar()
        return True, f"Servicio {id_servicio} actualizado"

    def eliminar(self, id_servicio):
        servicio = self.obtener(id_servicio)
        if not servicio: return False, "No existe"
        self.lista.remove(servicio)
        self.guardar()
        return True, "Servicio eliminado"


class HistorialAtencionController(CrudBase):
    def __init__(self, duenios, servicios, archivo=None):
        self.duenios = duenios
        self.servicios = servicios
        ruta = archivo or os.path.join(DATA_DIR, "historial_atencion.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [HistorialAtencion.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([h.a_diccionario() for h in self.lista])

    def validar(self, datos):
        try:
            due_id = int(datos.get("duenio_id", 0))
            ser_id = int(datos.get("servicio_id", 0))
        except (TypeError, ValueError):
            return "IDs inválidos"
        if not self.duenios.obtener(due_id): return "No existe el dueño"
        if not self.servicios.obtener(ser_id): return "No existe el servicio veterinario"
        if not str(datos.get("nombre_mascota", "")).strip(): return "El nombre de la mascota es obligatorio"
        return None

    def leer(self): return self.lista
    def obtener(self, id_historial):
        for h in self.lista:
            if h.id == id_historial: return h
        return None

    def buscar(self, t):
        return [h for h in self.lista if t.strip() in h.nombre_mascota.lower() or t.strip() in h.especie.lower()]

    def siguiente(self):
        return max([h.id for h in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        servicio = self.servicios.obtener(int(datos["servicio_id"]))
        
        es_afiliado = datos.get("es_afiliado", False)
        costo_final = ServicioVeterinario.calcular_costo_final(servicio.costo, es_afiliado)

        historial = HistorialAtencion(
            self.siguiente(), int(datos["duenio_id"]), servicio.id,
            str(datos["nombre_mascota"]).strip().title(),
            str(datos.get("especie", "Canino")).strip().title(),
            str(datos.get("observaciones", "")).strip(), costo_final
        )
        self.lista.append(historial)
        self.guardar()
        return True, f"Atención #{historial.id} registrada con éxito. Costo final: ${costo_final:.2f}"

    def actualizar(self, id_historial, datos): return False, "El historial no se modifica"

    def eliminar(self, id_historial):
        historial = self.obtener(id_historial)
        if not historial: return False, "No existe"
        self.lista.remove(historial)
        self.guardar()
        return True, "Registro de atención eliminado"

    def comprobante_atencion(self, id_historial):
        historial = self.obtener(id_historial)
        if not historial: return None
        due = self.duenios.obtener(historial.duenio_id)
        ser = self.servicios.obtener(historial.servicio_id)
        texto = f"COMPROBANTE VETERINARIA PATITAS FELICES - ATENCIÓN #{historial.id}\n"
        texto += f"Dueño   : {due.nombre_completo() if due else 'N/A'}   (Tel: {due.telefono if due else 'N/A'})\n"
        texto += f"Mascota : {historial.nombre_mascota} ({historial.especie})\n"
        texto += f"Servicio: {ser.nombre_servicio if ser else 'N/A'} [{ser.codigo if ser else 'N/A'}]\n"
        texto += "-" * 45 + f"\nObservaciones: {historial.observaciones or 'Ninguna'}\n"
        texto += f"TOTAL COBRADO: ${historial.costo_final:.2f}   (Fecha: {historial.fecha})"
        return texto

    def total_recaudado(self):
        return round(sum(h.costo_final for h in self.lista), 2)