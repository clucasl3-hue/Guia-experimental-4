from abc import ABC, abstractmethod
import os

from models import Pasajero, Vuelo, BoletoAvion
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


class PasajeroController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "pasajeros.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Pasajero.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([p.a_diccionario() for p in self.lista])

    def pasaportes_registrados(self, excepto_id=None):
        """CONJUNTO para verificar pasaportes únicos instantáneamente."""
        return {p.pasaporte.strip().upper() for p in self.lista if p.id != excepto_id and p.pasaporte}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "apellido", "email", "pasaporte"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"

        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            if not es_email_valido(email): return f"Email inválido: '{email}'"
            if email in {p.email for p in self.lista if p.id != id_actual}:
                return "Ese email ya está registrado"

        if "pasaporte" in datos:
            pas = str(datos["pasaporte"]).strip().upper()
            if pas in self.pasaportes_registrados(id_actual):
                return f"El pasaporte '{pas}' ya está registrado"
        return None

    def leer(self): return self.lista

    def obtener(self, id_pasajero):
        for p in self.lista:
            if p.id == id_pasajero: return p
        return None

    def buscar(self, t):
        t = t.strip().lower()
        if not t: return []
        return [p for p in self.lista if t in p.nombre.lower() or t in p.apellido.lower() or t in p.pasaporte.lower()]

    def siguiente(self):
        return max([p.id for p in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        pasajero = Pasajero(
            self.siguiente(), str(datos["nombre"]).strip().title(),
            str(datos["apellido"]).strip().title(), str(datos["email"]).strip().lower(),
            str(datos["pasaporte"]).strip().upper(), str(datos.get("nacionalidad", "")).strip().title()
        )
        self.lista.append(pasajero)
        self.guardar()
        return True, f"Pasajero creado: {pasajero.etiqueta()}"

    def actualizar(self, id_pasajero, datos):
        pasajero = self.obtener(id_pasajero)
        if not pasajero: return False, "No existe el pasajero"
        error = self.validar(datos, id_pasajero)
        if error: return False, error
        for k, v in datos.items():
            val = str(v).strip()
            if k in ("nombre", "apellido", "nacionalidad"): val = val.title()
            elif k == "email": val = val.lower()
            elif k == "pasaporte": val = val.upper()
            setattr(pasajero, k, val)
        self.guardar()
        return True, f"Pasajero {id_pasajero} actualizado"

    def eliminar(self, id_pasajero):
        pasajero = self.obtener(id_pasajero)
        if not pasajero: return False, "No existe"
        self.lista.remove(pasajero)
        self.guardar()
        return True, f"Pasajero {id_pasajero} eliminado"


class VueloController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "vuelos.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Vuelo.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([v.a_diccionario() for v in self.lista])

    def codigos_registrados(self, excepto_id=None):
        return {v.codigo_vuelo.strip().upper() for v in self.lista if v.id != excepto_id and v.codigo_vuelo}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("codigo_vuelo", "origen", "destino", "precio_base"):
                if str(datos.get(campo, "")).strip() == "": return f"El campo {campo} es obligatorio"
        if "codigo_vuelo" in datos:
            cod = str(datos["codigo_vuelo"]).strip().upper()
            if cod in self.codigos_registrados(id_actual): return f"El código de vuelo '{cod}' ya existe"
        return None

    def leer(self): return self.lista
    def obtener(self, id_vuelo):
        for v in self.lista:
            if v.id == id_vuelo: return v
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [v for v in self.lista if t in v.codigo_vuelo.lower() or t in v.origen.lower() or t in v.destino.lower()]

    def siguiente(self):
        return max([v.id for v in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        vuelo = Vuelo(
            self.siguiente(), str(datos["codigo_vuelo"]).strip().upper(),
            str(datos["origen"]).strip().title(), str(datos["destino"]).strip().title(),
            int(datos["asientos_disponibles"]) if str(datos.get("asientos_disponibles", "")).strip() != "" else 50,
            float(datos["precio_base"])
        )
        self.lista.append(vuelo)
        self.guardar()
        return True, f"Vuelo registrado: {vuelo.etiqueta()}"

    def actualizar(self, id_vuelo, datos):
        vuelo = self.obtener(id_vuelo)
        if not vuelo: return False, "No existe"
        error = self.validar(datos, id_vuelo)
        if error: return False, error
        if "codigo_vuelo" in datos: vuelo.codigo_vuelo = str(datos["codigo_vuelo"]).strip().upper()
        if "origen" in datos: vuelo.origen = str(datos["origen"]).strip().title()
        if "destino" in datos: vuelo.destino = str(datos["destino"]).strip().title()
        if "precio_base" in datos and str(datos["precio_base"]).strip() != "": vuelo.precio_base = float(datos["precio_base"])
        if "asientos_disponibles" in datos and str(datos["asientos_disponibles"]).strip() != "":
            vuelo.asientos_disponibles = int(datos["asientos_disponibles"])
        self.guardar()
        return True, f"Vuelo {id_vuelo} actualizado"

    def eliminar(self, id_vuelo):
        vuelo = self.obtener(id_vuelo)
        if not vuelo: return False, "No existe"
        self.lista.remove(vuelo)
        self.guardar()
        return True, "Vuelo eliminado"

    def vuelos_con_asientos(self):
        return [v for v in self.lista if v.hay_asientos()]


class BoletoAvionController(CrudBase):
    def __init__(self, pasajeros, vuelos, archivo=None):
        self.pasajeros = pasajeros
        self.vuelos = vuelos
        ruta = archivo or os.path.join(DATA_DIR, "boletos_avion.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [BoletoAvion.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([b.a_diccionario() for b in self.lista])

    def validar(self, datos):
        try:
            pas_id = int(datos.get("pasajero_id", 0))
            vue_id = int(datos.get("vuelo_id", 0))
        except (TypeError, ValueError):
            return "IDs inválidos"
        if not self.pasajeros.obtener(pas_id): return "No existe el pasajero"
        vuelo = self.vuelos.obtener(vue_id)
        if not vuelo: return "No existe el vuelo"
        if not vuelo.hay_asientos(): return f"El vuelo {vuelo.codigo_vuelo} no tiene asientos disponibles"
        return None

    def leer(self): return self.lista
    def obtener(self, id_boleto):
        for b in self.lista:
            if b.id == id_boleto: return b
        return None

    def buscar(self, t):
        return [b for b in self.lista if t.strip() in b.clase_asiento.lower()]

    def siguiente(self):
        return max([b.id for b in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        vuelo = self.vuelos.obtener(int(datos["vuelo_id"]))
        clase = str(datos.get("clase_asiento", "Economica")).strip().title()

        # Cálculo estático sumando tasa de aeropuerto
        total_pagar = Vuelo.calcular_total_vuelo(vuelo.precio_base, Vuelo.TASA_AEROPUERTO)

        boleto = BoletoAvion(
            self.siguiente(), int(datos["pasajero_id"]), vuelo.id,
            clase, total_pagar
        )
        vuelo.descontar_asiento()
        self.vuelos.guardar()
        self.lista.append(boleto)
        self.guardar()
        return True, f"Boleto de avión #{boleto.id} emitido con éxito. Total (incl. tasa aeroportuaria): ${total_pagar:.2f}"

    def actualizar(self, id_boleto, datos): return False, "Los boletos de avión no se modifican"

    def eliminar(self, id_boleto):
        boleto = self.obtener(id_boleto)
        if not boleto: return False, "No existe"
        vuelo = self.vuelos.obtener(boleto.vuelo_id)
        if vuelo:
            vuelo.aumentar_asiento()
            self.vuelos.guardar()
        self.lista.remove(boleto)
        self.guardar()
        return True, "Boleto cancelado y asiento devuelto al vuelo"

    def comprobante_boleto(self, id_boleto):
        boleto = self.obtener(id_boleto)
        if not boleto: return None
        pas = self.pasajeros.obtener(boleto.pasajero_id)
        vue = self.vuelos.obtener(boleto.vuelo_id)
        texto = f"PASS BOARDING / BOLETO DE AVIÓN #{boleto.id} · Clase: {boleto.clase_asiento}\n"
        texto += f"Pasajero: {pas.nombre_completo() if pas else 'N/A'}   (Pasaporte: {pas.pasaporte if pas else 'N/A'})\n"
        texto += f"Vuelo   : {vue.codigo_vuelo if vue else 'N/A'} : {vue.origen if vue else 'N/A'} ➔ {vue.destino if vue else 'N/A'}\n"
        texto += f"Tasa aeroportuaria incluida: ${Vuelo.TASA_AEROPUERTO:.2f}\n"
        texto += "-" * 50 + f"\nTOTAL PAGADO: ${boleto.precio_unitario:.2f}"
        return texto

    def total_recaudado(self):
        return round(sum(b.precio_unitario for b in self.lista), 2)