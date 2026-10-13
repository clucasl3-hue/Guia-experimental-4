from abc import ABC, abstractmethod
import os

from models import Asistente, EventoConcierto, EntradaConcierto
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


class AsistenteController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "asistentes_eventos.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Asistente.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([a.a_diccionario() for a in self.lista])

    def cedulas_registradas(self, excepto_id=None):
        return {a.cedula.strip() for a in self.lista if a.id != excepto_id and a.cedula}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "apellido", "email", "cedula"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"
        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            if not es_email_valido(email): return f"Email inválido: '{email}'"
            if email in {a.email for a in self.lista if a.id != id_actual}:
                return "Ese email ya está registrado"
        if "cedula" in datos:
            ced = str(datos["cedula"]).strip()
            if ced in self.cedulas_registradas(id_actual):
                return f"La cédula '{ced}' ya está registrada"
        return None

    def leer(self): return self.lista
    def obtener(self, id_a):
        for a in self.lista:
            if a.id == id_a: return a
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [a for a in self.lista if t in a.nombre.lower() or t in a.apellido.lower() or t in a.cedula.lower()]

    def siguiente(self):
        return max([a.id for a in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        asistente = Asistente(
            self.siguiente(), str(datos["nombre"]).strip().title(),
            str(datos["apellido"]).strip().title(), str(datos["email"]).strip().lower(),
            str(datos["cedula"]).strip(), str(datos.get("telefono", "")).strip()
        )
        self.lista.append(asistente)
        self.guardar()
        return True, f"Asistente registrado: {asistente.etiqueta()}"

    def actualizar(self, id_a, datos):
        a = self.obtener(id_a)
        if not a: return False, "No existe"
        error = self.validar(datos, id_a)
        if error: return False, error
        for k, v in datos.items():
            val = str(v).strip()
            if k in ("nombre", "apellido"): val = val.title()
            elif k == "email": val = val.lower()
            setattr(a, k, val)
        self.guardar()
        return True, f"Asistente {id_a} actualizado"

    def eliminar(self, id_a):
        a = self.obtener(id_a)
        if not a: return False, "No existe"
        self.lista.remove(a)
        self.guardar()
        return True, "Asistente eliminado"


class EventoConciertoController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "eventos_conciertos.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [EventoConcierto.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([e.a_diccionario() for e in self.lista])

    def codigos_registrados(self, excepto_id=None):
        return {e.codigo_evento.strip().upper() for e in self.lista if e.id != excepto_id and e.codigo_evento}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre_evento", "codigo_evento", "precio_base", "aforo_maximo"):
                if str(datos.get(campo, "")).strip() == "": return f"El campo {campo} es obligatorio"
        if "codigo_evento" in datos:
            cod = str(datos["codigo_evento"]).strip().upper()
            if cod in self.codigos_registrados(id_actual): return f"El código de evento '{cod}' ya existe"
        return None

    def leer(self): return self.lista
    def obtener(self, id_e):
        for e in self.lista:
            if e.id == id_e: return e
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [e for e in self.lista if t in e.nombre_evento.lower() or t in e.codigo_evento.lower()]

    def siguiente(self):
        return max([e.id for e in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        evento = EventoConcierto(
            self.siguiente(), str(datos["nombre_evento"]).strip().title(),
            str(datos["codigo_evento"]).strip().upper(), float(datos["precio_base"]),
            int(datos["aforo_maximo"])
        )
        self.lista.append(evento)
        self.guardar()
        return True, f"Evento registrado: {evento.etiqueta()}"

    def actualizar(self, id_e, datos):
        e = self.obtener(id_e)
        if not e: return False, "No existe"
        error = self.validar(datos, id_e)
        if error: return False, error
        if "nombre_evento" in datos: e.nombre_evento = str(datos["nombre_evento"]).strip().title()
        if "codigo_evento" in datos: e.codigo_evento = str(datos["codigo_evento"]).strip().upper()
        if "precio_base" in datos and str(datos["precio_base"]).strip() != "": e.precio_base = float(datos["precio_base"])
        if "aforo_maximo" in datos and str(datos["aforo_maximo"]).strip() != "": e.aforo_maximo = int(datos["aforo_maximo"])
        self.guardar()
        return True, "Evento actualizado"

    def eliminar(self, id_e):
        e = self.obtener(id_e)
        if not e: return False, "No existe"
        self.lista.remove(e)
        self.guardar()
        return True, "Evento eliminado"


class EntradaConciertoController(CrudBase):
    def __init__(self, asistentes, eventos, archivo=None):
        self.asistentes = asistentes
        self.eventos = eventos
        ruta = archivo or os.path.join(DATA_DIR, "entradas_conciertos.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [EntradaConcierto.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([en.a_diccionario() for en in self.lista])

    def validar(self, datos):
        try:
            ast_id = int(datos.get("asistente_id", 0))
            ev_id = int(datos.get("evento_id", 0))
        except (TypeError, ValueError):
            return "IDs inválidos"
        if not self.asistentes.obtener(ast_id): return "No existe el asistente"
        evento = self.eventos.obtener(ev_id)
        if not evento: return "No existe el evento"
        
        # Validar aforo actual del evento
        vendidas = sum(1 for en in self.lista if en.evento_id == evento.id)
        if vendidas >= evento.aforo_maximo:
            return f"El evento {evento.nombre_evento} ya agotó su aforo máximo ({evento.aforo_maximo} entradas)."
        return None

    def leer(self): return self.lista
    def obtener(self, id_en):
        for en in self.lista:
            if en.id == id_en: return en
        return None

    def buscar(self, t):
        return [en for en in self.lista if t.strip().lower() in en.tipo_localidad.lower() or t.strip() in en.fecha_compra]

    def siguiente(self):
        return max([en.id for en in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        evento = self.eventos.obtener(int(datos["evento_id"]))
        es_vip = datos.get("es_vip", False)

        costo_total = EventoConcierto.calcular_costo_entrada(evento.precio_base, es_vip)
        localidad = "VIP" if es_vip else "General"

        entrada = EntradaConcierto(
            self.siguiente(), int(datos["asistente_id"]), evento.id,
            localidad, costo_total, str(datos.get("fecha_compra", "")).strip()
        )
        self.lista.append(entrada)
        self.guardar()
        return True, f"Entrada #{entrada.id} [{localidad}] vendida con éxito. Total: ${costo_total:.2f}"

    def actualizar(self, id_en, datos): return False, "Las entradas no se modifican"

    def eliminar(self, id_en):
        en = self.obtener(id_en)
        if not en: return False, "No existe"
        self.lista.remove(en)
        self.guardar()
        return True, "Entrada cancelada"

    def comprobante_entrada(self, id_en):
        en = self.obtener(id_en)
        if not en: return None
        a = self.asistentes.obtener(en.asistente_id)
        e = self.eventos.obtener(en.evento_id)
        texto = f"COMPROBANTE DE ENTRADA / CONCIERTO #{en.id}   Fecha: {en.fecha_compra}\n"
        texto += f"Asistente: {a.nombre_completo() if a else 'N/A'}   (Cédula: {a.cedula if a else 'N/A'})\n"
        texto += f"Evento   : [{e.codigo_evento if e else 'N/A'}] {e.nombre_evento if e else 'N/A'}\n"
        texto += f"Localidad: {en.tipo_localidad}   ·   Recargo VIP fijo: ${EventoConcierto.RECARGO_VIP:.2f}\n"
        texto += "-" * 50 + f"\nTOTAL PAGADO: ${en.costo_total:.2f}"
        return texto

    def total_recaudado(self):
        return round(sum(en.costo_total for en in self.lista), 2)