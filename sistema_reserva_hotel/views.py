from abc import ABC, abstractmethod
import os
from datetime import date

from models import Huesped, Habitacion, Reserva
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


class HuespedController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "huespedes.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Huesped.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([h.a_diccionario() for h in self.lista])

    def pasaportes_registrados(self, excepto_id=None):
        """CONJUNTO para verificar pasaportes únicos de forma inmediata."""
        return {h.pasaporte.strip().upper() for h in self.lista if h.id != excepto_id and h.pasaporte}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "apellido", "email", "pasaporte"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"

        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            if not es_email_valido(email): return f"Email inválido: '{email}'"
            if email in {h.email for h in self.lista if h.id != id_actual}:
                return "Ese email ya está registrado"

        if "pasaporte" in datos:
            pasaporte = str(datos["pasaporte"]).strip().upper()
            if pasaporte in self.pasaportes_registrados(id_actual):
                return f"El pasaporte '{pasaporte}' ya está registrado"
        return None

    def leer(self): return self.lista

    def obtener(self, id_huesped):
        for h in self.lista:
            if h.id == id_huesped: return h
        return None

    def buscar(self, t):
        t = t.strip().lower()
        if not t: return []
        return [h for h in self.lista if t in h.nombre.lower() or t in h.apellido.lower() or t in h.pasaporte.lower()]

    def siguiente(self):
        return max([h.id for h in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        huesped = Huesped(
            self.siguiente(), str(datos["nombre"]).strip().title(),
            str(datos["apellido"]).strip().title(), str(datos["email"]).strip().lower(),
            str(datos["pasaporte"]).strip().upper(), str(datos.get("pais", "")).strip().title()
        )
        self.lista.append(huesped)
        self.guardar()
        return True, f"Huésped creado: {huesped.etiqueta()}"

    def actualizar(self, id_huesped, datos):
        huesped = self.obtener(id_huesped)
        if not huesped: return False, "No existe el huésped"
        error = self.validar(datos, id_huesped)
        if error: return False, error
        for k, v in datos.items():
            val = str(v).strip()
            if k in ("nombre", "apellido", "pais"): val = val.title()
            elif k == "email": val = val.lower()
            elif k == "pasaporte": val = val.upper()
            setattr(huesped, k, val)
        self.guardar()
        return True, f"Huésped {id_huesped} actualizado"

    def eliminar(self, id_huesped):
        huesped = self.obtener(id_huesped)
        if not huesped: return False, "No existe"
        self.lista.remove(huesped)
        self.guardar()
        return True, f"Huésped {id_huesped} eliminado"


class HabitacionController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "habitaciones.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Habitacion.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([hab.a_diccionario() for hab in self.lista])

    def numeros_habitacion_registrados(self, excepto_id=None):
        return {hab.numero_habitacion.strip().upper() for hab in self.lista if hab.id != excepto_id}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("numero_habitacion", "tipo", "precio_noche"):
                if str(datos.get(campo, "")).strip() == "": return f"El campo {campo} es obligatorio"
        if "numero_habitacion" in datos:
            num = str(datos["numero_habitacion"]).strip().upper()
            if num in self.numeros_habitacion_registrados(id_actual): return f"La habitación '{num}' ya existe"
        return None

    def leer(self): return self.lista
    def obtener(self, id_habitacion):
        for hab in self.lista:
            if hab.id == id_habitacion: return hab
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [hab for hab in self.lista if t in hab.numero_habitacion.lower() or t in hab.tipo.lower()]

    def siguiente(self):
        return max([hab.id for hab in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        habitacion = Habitacion(
            self.siguiente(), str(datos["numero_habitacion"]).strip().upper(),
            str(datos["tipo"]).strip().title(), float(datos["precio_noche"]), True
        )
        self.lista.append(habitacion)
        self.guardar()
        return True, f"Habitación registrada: {habitacion.etiqueta()}"

    def actualizar(self, id_habitacion, datos):
        habitacion = self.obtener(id_habitacion)
        if not habitacion: return False, "No existe"
        error = self.validar(datos, id_habitacion)
        if error: return False, error
        if "numero_habitacion" in datos: habitacion.numero_habitacion = str(datos["numero_habitacion"]).strip().upper()
        if "tipo" in datos: habitacion.tipo = str(datos["tipo"]).strip().title()
        if "precio_noche" in datos and str(datos["precio_noche"]).strip() != "":
            habitacion.precio_noche = float(datos["precio_noche"])
        self.guardar()
        return True, f"Habitación {id_habitacion} actualizada"

    def eliminar(self, id_habitacion):
        habitacion = self.obtener(id_habitacion)
        if not habitacion: return False, "No existe"
        self.lista.remove(habitacion)
        self.guardar()
        return True, "Habitación eliminada"

    def habitaciones_disponibles(self):
        return [hab for hab in self.lista if hab.disponible]


class ReservaController(CrudBase):
    def __init__(self, huespedes, habitaciones, archivo=None):
        self.huespedes = huespedes
        self.habitaciones = habitaciones
        ruta = archivo or os.path.join(DATA_DIR, "reservas.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Reserva.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([r.a_diccionario() for r in self.lista])

    def validar(self, datos):
        try:
            hue_id = int(datos.get("huesped_id", 0))
            hab_id = int(datos.get("habitacion_id", 0))
            noches = int(datos.get("noches", 0))
        except (TypeError, ValueError):
            return "Datos numéricos inválidos"
        if not self.huespedes.obtener(hue_id): return "No existe el huésped"
        habitacion = self.habitaciones.obtener(hab_id)
        if not habitacion: return "No existe la habitación"
        if not habitacion.disponible: return f"La habitación {habitacion.numero_habitacion} está ocupada"
        if noches <= 0: return "La cantidad de noches debe ser mayor a 0"
        return None

    def leer(self): return self.lista
    def obtener(self, id_reserva):
        for r in self.lista:
            if r.id == id_reserva: return r
        return None

    def buscar(self, t):
        return [r for r in self.lista if t.strip() in r.fecha_inicio]

    def siguiente(self):
        return max([r.id for r in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        habitacion = self.habitaciones.obtener(int(datos["habitacion_id"]))
        noches = int(datos["noches"])

        # Cálculos con métodos estáticos de Habitacion
        subtotal = Habitacion.calcular_subtotal(habitacion.precio_noche, noches)
        total_pagar = Habitacion.calcular_total_con_impuesto(subtotal)

        reserva = Reserva(
            self.siguiente(), int(datos["huesped_id"]), habitacion.id,
            noches, str(datos.get("fecha_inicio", "")).strip(), total_pagar
        )
        habitacion.disponible = False  # Ocupar habitación
        self.habitaciones.guardar()
        self.lista.append(reserva)
        self.guardar()
        return True, f"Reserva #{reserva.id} creada con éxito. Total (con 12% IVA): ${total_pagar:.2f}"

    def actualizar(self, id_reserva, datos): return False, "Las reservas no se modifican"

    def eliminar(self, id_reserva):
        reserva = self.obtener(id_reserva)
        if not reserva: return False, "No existe"
        habitacion = self.habitaciones.obtener(reserva.habitacion_id)
        if habitacion:
            habitacion.disponible = True  # Liberar habitación
            self.habitaciones.guardar()
        self.lista.remove(reserva)
        self.guardar()
        return True, "Reserva cancelada y habitación liberada"

    def comprobante_reserva(self, id_reserva):
        reserva = self.obtener(id_reserva)
        if not reserva: return None
        hue = self.huespedes.obtener(reserva.huesped_id)
        hab = self.habitaciones.obtener(reserva.habitacion_id)
        texto = f"COMPROBANTE DE RESERVA #{reserva.id} · Fecha Inicio: {reserva.fecha_inicio}\n"
        texto += f"Huésped : {hue.nombre_completo() if hue else 'N/A'}   (Pasaporte: {hue.pasaporte if hue else 'N/A'})\n"
        texto += f"Habitación: {hab.numero_habitacion if hab else 'N/A'} ({hab.tipo if hab else 'N/A'})\n"
        texto += f"Noches  : {reserva.noches}\n"
        texto += "-" * 42 + f"\nTOTAL A PAGAR (incl. {Habitacion.IMPUESTO_HOTEL*100}% IVA): ${reserva.total:.2f}"
        return texto

    def total_recaudado(self):
        return round(sum(r.total for r in self.lista), 2)