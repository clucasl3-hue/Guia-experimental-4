from abc import ABC, abstractmethod
import os

from models import Remitente, ZonaEnvio, PaqueteEnvio
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


class RemitenteController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "remitentes.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Remitente.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([r.a_diccionario() for r in self.lista])

    def rucs_registrados(self, excepto_id=None):
        """CONJUNTO para verificar RUC/cédulas únicas instantáneamente."""
        return {r.ruc_cedula.strip() for r in self.lista if r.id != excepto_id and r.ruc_cedula}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "apellido", "email", "ruc_cedula"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"

        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            if not es_email_valido(email): return f"Email inválido: '{email}'"
            if email in {r.email for r in self.lista if r.id != id_actual}:
                return "Ese email ya está registrado"

        if "ruc_cedula" in datos:
            ruc = str(datos["ruc_cedula"]).strip()
            if ruc in self.rucs_registrados(id_actual):
                return f"El RUC/Cédula '{ruc}' ya está registrado"
        return None

    def leer(self): return self.lista

    def obtener(self, id_remitente):
        for r in self.lista:
            if r.id == id_remitente: return r
        return None

    def buscar(self, t):
        t = t.strip().lower()
        if not t: return []
        return [r for r in self.lista if t in r.nombre.lower() or t in r.apellido.lower() or t in r.ruc_cedula.lower()]

    def siguiente(self):
        return max([r.id for r in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        remitente = Remitente(
            self.siguiente(), str(datos["nombre"]).strip().title(),
            str(datos["apellido"]).strip().title(), str(datos["email"]).strip().lower(),
            str(datos["ruc_cedula"]).strip(), str(datos.get("telefono", "")).strip()
        )
        self.lista.append(remitente)
        self.guardar()
        return True, f"Remitente registrado: {remitente.etiqueta()}"

    def actualizar(self, id_remitente, datos):
        remitente = self.obtener(id_remitente)
        if not remitente: return False, "No existe el remitente"
        error = self.validar(datos, id_remitente)
        if error: return False, error
        for k, v in datos.items():
            val = str(v).strip()
            if k in ("nombre", "apellido"): val = val.title()
            elif k == "email": val = val.lower()
            setattr(remitente, k, val)
        self.guardar()
        return True, f"Remitente {id_remitente} actualizado"

    def eliminar(self, id_remitente):
        remitente = self.obtener(id_remitente)
        if not remitente: return False, "No existe"
        self.lista.remove(remitente)
        self.guardar()
        return True, f"Remitente {id_remitente} eliminado"


class ZonaEnvioController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "zonas_envio.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [ZonaEnvio.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([z.a_diccionario() for z in self.lista])

    def codigos_postales_registrados(self, excepto_id=None):
        return {z.codigo_postal.strip().upper() for z in self.lista if z.id != excepto_id and z.codigo_postal}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre_zona", "codigo_postal", "tarifa_base_kg"):
                if str(datos.get(campo, "")).strip() == "": return f"El campo {campo} es obligatorio"
        if "codigo_postal" in datos:
            cp = str(datos["codigo_postal"]).strip().upper()
            if cp in self.codigos_postales_registrados(id_actual): return f"El código postal '{cp}' ya existe"
        return None

    def leer(self): return self.lista
    def obtener(self, id_zona):
        for z in self.lista:
            if z.id == id_zona: return z
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [z for z in self.lista if t in z.nombre_zona.lower() or t in z.codigo_postal.lower()]

    def siguiente(self):
        return max([z.id for z in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        zona = ZonaEnvio(
            self.siguiente(), str(datos["nombre_zona"]).strip().title(),
            str(datos["codigo_postal"]).strip().upper(), float(datos["tarifa_base_kg"])
        )
        self.lista.append(zona)
        self.guardar()
        return True, f"Zona registrada: {zona.etiqueta()}"

    def actualizar(self, id_zona, datos):
        zona = self.obtener(id_zona)
        if not zona: return False, "No existe"
        error = self.validar(datos, id_zona)
        if error: return False, error
        if "nombre_zona" in datos: zona.nombre_zona = str(datos["nombre_zona"]).strip().title()
        if "codigo_postal" in datos: zona.codigo_postal = str(datos["codigo_postal"]).strip().upper()
        if "tarifa_base_kg" in datos and str(datos["tarifa_base_kg"]).strip() != "":
            zona.tarifa_base_kg = float(datos["tarifa_base_kg"])
        self.guardar()
        return True, f"Zona {id_zona} actualizada"

    def eliminar(self, id_zona):
        zona = self.obtener(id_zona)
        if not zona: return False, "No existe"
        self.lista.remove(zona)
        self.guardar()
        return True, "Zona eliminada"


class PaqueteEnvioController(CrudBase):
    def __init__(self, remitentes, zonas, archivo=None):
        self.remitentes = remitentes
        self.zonas = zonas
        ruta = archivo or os.path.join(DATA_DIR, "paquetes_envio.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [PaqueteEnvio.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([p.a_diccionario() for p in self.lista])

    def validar(self, datos):
        try:
            rem_id = int(datos.get("remitente_id", 0))
            zon_id = int(datos.get("zona_id", 0))
            peso = float(datos.get("peso_kg", 0.0))
        except (TypeError, ValueError):
            return "Datos numéricos inválidos"
        if not self.remitentes.obtener(rem_id): return "No existe el remitente"
        zona = self.zonas.obtener(zon_id)
        if not zona: return "No existe la zona de envío"
        if not ZonaEnvio.es_peso_valido(peso):
            return f"El peso debe ser mayor a 0 y hasta {ZonaEnvio.PESO_MAXIMO_PERMITIDO} kg"
        return None

    def leer(self): return self.lista
    def obtener(self, id_paquete):
        for p in self.lista:
            if p.id == id_paquete: return p
        return None

    def buscar(self, t):
        return [p for p in self.lista if t.strip() in p.descripcion.lower() or t.strip() in p.fecha_envio]

    def siguiente(self):
        return max([p.id for p in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        zona = self.zonas.obtener(int(datos["zona_id"]))
        peso = float(datos["peso_kg"])

        costo_total = ZonaEnvio.calcular_costo_envio(zona.tarifa_base_kg, peso)

        paquete = PaqueteEnvio(
            self.siguiente(), int(datos["remitente_id"]), zona.id,
            peso, str(datos.get("descripcion", "")).strip(), costo_total
        )
        self.lista.append(paquete)
        self.guardar()
        return True, f"Guía de Envío #{paquete.id} generada con éxito. Costo total: ${costo_total:.2f}"

    def actualizar(self, id_paquete, datos): return False, "Las guías de envío no se modifican"

    def eliminar(self, id_paquete):
        paquete = self.obtener(id_paquete)
        if not paquete: return False, "No existe"
        self.lista.remove(paquete)
        self.guardar()
        return True, "Envío cancelado del sistema"

    def comprobante_envio(self, id_paquete):
        paquete = self.obtener(id_paquete)
        if not paquete: return None
        rem = self.remitentes.obtener(paquete.remitente_id)
        zon = self.zonas.obtener(paquete.zona_id)
        texto = f"GUÍA DE COURIER / ENVÍO #{paquete.id}   Fecha: {paquete.fecha_envio}\n"
        texto += f"Remitente  : {rem.nombre_completo() if rem else 'N/A'}   (RUC/Céd: {rem.ruc_cedula if rem else 'N/A'})\n"
        texto += f"Zona Destino: {zon.nombre_zona if zon else 'N/A'} (CP: {zon.codigo_postal if zon else 'N/A'})\n"
        texto += f"Detalles   : {paquete.descripcion or 'Sin detalle'}   ·   Peso: {paquete.peso_kg} kg\n"
        texto += "-" * 50 + f"\nCOSTO TOTAL ENVÍO: ${paquete.costo_total:.2f}"
        return texto

    def total_recaudado(self):
        return round(sum(p.costo_total for p in self.lista), 2)