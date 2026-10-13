from abc import ABC, abstractmethod
import os

from models import ConductorParque, EspacioParqueo, TicketEstacionamiento
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


class ConductorParqueController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "conductores_parque.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [ConductorParque.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([c.a_diccionario() for c in self.lista])

    def placas_registradas(self, excepto_id=None):
        return {c.placa.strip().upper() for c in self.lista if c.id != excepto_id and c.placa}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "apellido", "email", "placa"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"
        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            if not es_email_valido(email): return f"Email inválido: '{email}'"
            if email in {c.email for c in self.lista if c.id != id_actual}:
                return "Ese email ya está registrado"
        if "placa" in datos:
            placa = str(datos["placa"]).strip().upper()
            if placa in self.placas_registradas(id_actual):
                return f"La placa '{placa}' ya está registrada"
        return None

    def leer(self): return self.lista
    def obtener(self, id_c):
        for c in self.lista:
            if c.id == id_c: return c
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [c for c in self.lista if t in c.nombre.lower() or t in c.apellido.lower() or t in c.placa.lower()]

    def siguiente(self):
        return max([c.id for c in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        conductor = ConductorParque(
            self.siguiente(), str(datos["nombre"]).strip().title(),
            str(datos["apellido"]).strip().title(), str(datos["email"]).strip().lower(),
            str(datos["placa"]).strip().upper(), str(datos.get("telefono", "")).strip()
        )
        self.lista.append(conductor)
        self.guardar()
        return True, f"Conductor registrado: {conductor.etiqueta()}"

    def actualizar(self, id_c, datos):
        c = self.obtener(id_c)
        if not c: return False, "No existe"
        error = self.validar(datos, id_c)
        if error: return False, error
        for k, v in datos.items():
            val = str(v).strip()
            if k in ("nombre", "apellido"): val = val.title()
            elif k == "email": val = val.lower()
            elif k == "placa": val = val.upper()
            setattr(c, k, val)
        self.guardar()
        return True, f"Conductor {id_c} actualizado"

    def eliminar(self, id_c):
        c = self.obtener(id_c)
        if not c: return False, "No existe"
        self.lista.remove(c)
        self.guardar()
        return True, "Conductor eliminado"


class EspacioParqueoController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "espacios_parqueo.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [EspacioParqueo.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([e.a_diccionario() for e in self.lista])

    def numeros_registrados(self, excepto_id=None):
        return {e.numero_espacio.strip().upper() for e in self.lista if e.id != excepto_id and e.numero_espacio}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("numero_espacio", "tipo_vehiculo"):
                if str(datos.get(campo, "")).strip() == "": return f"El campo {campo} es obligatorio"
        if "numero_espacio" in datos:
            num = str(datos["numero_espacio"]).strip().upper()
            if num in self.numeros_registrados(id_actual): return f"El espacio número '{num}' ya existe"
        return None

    def leer(self): return self.lista
    def obtener(self, id_e):
        for e in self.lista:
            if e.id == id_e: return e
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [e for e in self.lista if t in e.numero_espacio.lower() or t in e.tipo_vehiculo.lower()]

    def siguiente(self):
        return max([e.id for e in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        espacio = EspacioParqueo(
            self.siguiente(), str(datos["numero_espacio"]).strip().upper(),
            str(datos["tipo_vehiculo"]).strip().title(), True
        )
        self.lista.append(espacio)
        self.guardar()
        return True, f"Espacio registrado: {espacio.etiqueta()}"

    def actualizar(self, id_e, datos):
        e = self.obtener(id_e)
        if not e: return False, "No existe"
        error = self.validar(datos, id_e)
        if error: return False, error
        if "numero_espacio" in datos: e.numero_espacio = str(datos["numero_espacio"]).strip().upper()
        if "tipo_vehiculo" in datos: e.tipo_vehiculo = str(datos["tipo_vehiculo"]).strip().title()
        self.guardar()
        return True, "Espacio actualizado"

    def eliminar(self, id_e):
        e = self.obtener(id_e)
        if not e: return False, "No existe"
        self.lista.remove(e)
        self.guardar()
        return True, "Espacio eliminado"

    def espacios_disponibles(self):
        return [e for e in self.lista if e.disponible]


class TicketEstacionamientoController(CrudBase):
    def __init__(self, conductores, espacios, archivo=None):
        self.conductores = conductores
        self.espacios = espacios
        ruta = archivo or os.path.join(DATA_DIR, "tickets_parqueo.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [TicketEstacionamiento.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([t.a_diccionario() for t in self.lista])

    def validar(self, datos):
        try:
            cond_id = int(datos.get("conductor_id", 0))
            esp_id = int(datos.get("espacio_id", 0))
            horas = float(datos.get("horas_estadia", 0.0))
        except (TypeError, ValueError):
            return "IDs o horas inválidas"
        if not self.conductores.obtener(cond_id): return "No existe el conductor"
        espacio = self.espacios.obtener(esp_id)
        if not espacio: return "No existe el espacio de parqueo"
        if not espacio.disponible: return f"El espacio #{espacio.numero_espacio} se encuentra ocupado"
        if horas <= 0: return "Las horas de estadía deben ser mayores a 0"
        return None

    def leer(self): return self.lista
    def obtener(self, id_t):
        for t in self.lista:
            if t.id == id_t: return t
        return None

    def buscar(self, t):
        return [tic for tic in self.lista if t.strip() in tic.fecha_ingreso]

    def siguiente(self):
        return max([tic.id for tic in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        espacio = self.espacios.obtener(int(datos["espacio_id"]))
        horas = float(datos["horas_estadia"])

        total_pagar = EspacioParqueo.calcular_costo_estadia(horas)

        ticket = TicketEstacionamiento(
            self.siguiente(), int(datos["conductor_id"]), espacio.id,
            horas, total_pagar
        )
        espacio.disponible = False  # Ocupar espacio
        self.espacios.guardar()
        self.lista.append(ticket)
        self.guardar()
        return True, f"Ticket #{ticket.id} emitido con éxito. Total a pagar ({horas}h @ ${EspacioParqueo.TARIFA_HORA}/h): ${total_pagar:.2f}"

    def actualizar(self, id_t, datos): return False, "Los tickets emitidos no se modifican"

    def eliminar(self, id_t):
        t = self.obtener(id_t)
        if not t: return False, "No existe"
        espacio = self.espacios.obtener(t.espacio_id)
        if espacio:
            espacio.disponible = True  # Liberar espacio
            self.espacios.guardar()
        self.lista.remove(t)
        self.guardar()
        return True, "Ticket cerrado y espacio liberado"

    def comprobante_ticket(self, id_t):
        t = self.obtener(id_t)
        if not t: return None
        c = self.conductores.obtener(t.conductor_id)
        e = self.espacios.obtener(t.espacio_id)
        texto = f"TICKET DE ESTACIONAMIENTO #{t.id}   Ingreso: {t.fecha_ingreso}\n"
        texto += f"Conductor: {c.nombre_completo() if c else 'N/A'}   (Placa: {c.placa if c else 'N/A'})\n"
        texto += f"Espacio  : #{e.numero_espacio if e else 'N/A'} [{e.tipo_vehiculo if e else 'N/A'}]\n"
        texto += f"Estadía  : {t.horas_estadia} horas   ·   Tarifa: ${EspacioParqueo.TARIFA_HORA:.2f}/h\n"
        texto += "-" * 50 + f"\nTOTAL PAGADO: ${t.total_pagar:.2f}"
        return texto

    def total_recaudado(self):
        return round(sum(t.total_pagar for t in self.lista), 2)