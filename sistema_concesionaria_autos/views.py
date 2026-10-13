from abc import ABC, abstractmethod
import os

from models import Comprador, Vehiculo, VentaVehiculo
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


class CompradorController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "compradores.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Comprador.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([c.a_diccionario() for c in self.lista])

    def cedulas_registradas(self, excepto_id=None):
        """CONJUNTO para verificar cédulas únicas instantáneamente."""
        return {c.cedula.strip() for c in self.lista if c.id != excepto_id and c.cedula}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "apellido", "email", "cedula"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"

        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            if not es_email_valido(email): return f"Email inválido: '{email}'"
            if email in {c.email for c in self.lista if c.id != id_actual}:
                return "Ese email ya está registrado"

        if "cedula" in datos:
            cedula = str(datos["cedula"]).strip()
            if cedula in self.cedulas_registradas(id_actual):
                return f"La cédula '{cedula}' ya está registrada"
        return None

    def leer(self): return self.lista

    def obtener(self, id_comprador):
        for c in self.lista:
            if c.id == id_comprador: return c
        return None

    def buscar(self, t):
        t = t.strip().lower()
        if not t: return []
        return [c for c in self.lista if t in c.nombre.lower() or t in c.apellido.lower() or t in c.cedula.lower()]

    def siguiente(self):
        return max([c.id for c in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        comprador = Comprador(
            self.siguiente(), str(datos["nombre"]).strip().title(),
            str(datos["apellido"]).strip().title(), str(datos["email"]).strip().lower(),
            str(datos["cedula"]).strip(), float(datos.get("presupuesto", 0.0))
        )
        self.lista.append(comprador)
        self.guardar()
        return True, f"Comprador registrado: {comprador.etiqueta()}"

    def actualizar(self, id_comprador, datos):
        comprador = self.obtener(id_comprador)
        if not comprador: return False, "No existe el comprador"
        error = self.validar(datos, id_comprador)
        if error: return False, error
        for k, v in datos.items():
            val = str(v).strip()
            if k in ("nombre", "apellido"): val = val.title()
            elif k == "email": val = val.lower()
            elif k == "presupuesto": val = float(v)
            setattr(comprador, k, val)
        self.guardar()
        return True, f"Comprador {id_comprador} actualizado"

    def eliminar(self, id_comprador):
        comprador = self.obtener(id_comprador)
        if not comprador: return False, "No existe"
        self.lista.remove(comprador)
        self.guardar()
        return True, f"Comprador {id_comprador} eliminado"


class VehiculoController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "vehiculos.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Vehiculo.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([v.a_diccionario() for v in self.lista])

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("marca", "modelo", "anio", "precio_base"):
                if str(datos.get(campo, "")).strip() == "": return f"El campo {campo} es obligatorio"
        if "marca" in datos:
            marca = str(datos["marca"]).strip().upper()
            if not Vehiculo.es_marca_valida(marca):
                return f"Marca no permitida. Marcas válidas: {', '.join(Vehiculo.MARCAS_PERMITIDAS)}"
        return None

    def leer(self): return self.lista
    def obtener(self, id_vehiculo):
        for v in self.lista:
            if v.id == id_vehiculo: return v
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [v for v in self.lista if t in v.marca.lower() or t in v.modelo.lower()]

    def siguiente(self):
        return max([v.id for v in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        vehiculo = Vehiculo(
            self.siguiente(), str(datos["marca"]).strip().upper(),
            str(datos["modelo"]).strip().title(), int(datos["anio"]),
            float(datos["precio_base"]),
            int(datos["stock"]) if str(datos.get("stock", "")).strip() != "" else 1
        )
        self.lista.append(vehiculo)
        self.guardar()
        return True, f"Vehículo registrado: {vehiculo.etiqueta()}"

    def actualizar(self, id_vehiculo, datos):
        vehiculo = self.obtener(id_vehiculo)
        if not vehiculo: return False, "No existe"
        error = self.validar(datos, id_vehiculo)
        if error: return False, error
        if "marca" in datos: vehiculo.marca = str(datos["marca"]).strip().upper()
        if "modelo" in datos: vehiculo.modelo = str(datos["modelo"]).strip().title()
        if "anio" in datos: vehiculo.anio = int(datos["anio"])
        if "precio_base" in datos and str(datos["precio_base"]).strip() != "": vehiculo.precio_base = float(datos["precio_base"])
        if "stock" in datos and str(datos["stock"]).strip() != "": vehiculo.stock = int(datos["stock"])
        self.guardar()
        return True, f"Vehículo {id_vehiculo} actualizado"

    def eliminar(self, id_vehiculo):
        vehiculo = self.obtener(id_vehiculo)
        if not vehiculo: return False, "No existe"
        self.lista.remove(vehiculo)
        self.guardar()
        return True, "Vehículo eliminado"

    def vehiculos_disponibles(self):
        return [v for v in self.lista if v.hay_stock()]


class VentaVehiculoController(CrudBase):
    def __init__(self, compradores, vehiculos, archivo=None):
        self.compradores = compradores
        self.vehiculos = vehiculos
        ruta = archivo or os.path.join(DATA_DIR, "ventas_autos.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [VentaVehiculo.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([v.a_diccionario() for v in self.lista])

    def validar(self, datos):
        try:
            com_id = int(datos.get("comprador_id", 0))
            veh_id = int(datos.get("vehiculo_id", 0))
        except (TypeError, ValueError):
            return "IDs inválidos"
        
        comprador = self.compradores.obtener(com_id)
        if not comprador: return "No existe el comprador"
        vehiculo = self.vehiculos.obtener(veh_id)
        if not vehiculo: return "No existe el vehículo"
        if not vehiculo.hay_stock(): return f"El vehículo {vehiculo.marca} {vehiculo.modelo} no tiene stock disponible"
        
        if comprador.presupuesto > 0 and comprador.presupuesto < vehiculo.precio_base:
            return f"Presupuesto insuficiente (${comprador.presupuesto:,.2f}) para este vehículo (${vehiculo.precio_base:,.2f})"
        return None

    def leer(self): return self.lista
    def obtener(self, id_venta):
        for v in self.lista:
            if v.id == id_venta: return v
        return None

    def buscar(self, t):
        return [v for v in self.lista if t.strip() in v.anio_venta]

    def siguiente(self):
        return max([v.id for v in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        vehiculo = self.vehiculos.obtener(int(datos["vehiculo_id"]))
        
        venta = VentaVehiculo(
            self.siguiente(), int(datos["comprador_id"]), vehiculo.id,
            "", vehiculo.precio_base
        )
        vehiculo.descontar_stock()
        self.vehiculos.guardar()
        self.lista.append(venta)
        self.guardar()
        return True, f"Venta #{venta.id} registrada con éxito. Stock descontado. Total: ${vehiculo.precio_base:,.2f}"

    def actualizar(self, id_venta, datos): return False, "Las ventas no se modifican"

    def eliminar(self, id_venta):
        venta = self.obtener(id_venta)
        if not venta: return False, "No existe"
        vehiculo = self.vehiculos.obtener(venta.vehiculo_id)
        if vehiculo:
            vehiculo.aumentar_stock()
            self.vehiculos.guardar()
        self.lista.remove(venta)
        self.guardar()
        return True, "Venta anulada y stock devuelto al inventario"

    def factura_venta(self, id_venta):
        venta = self.obtener(id_venta)
        if not venta: return None
        com = self.compradores.obtener(venta.comprador_id)
        veh = self.vehiculos.obtener(venta.vehiculo_id)
        texto = f"FACTURA CONCESIONARIA - VENTA #{venta.id}   Fecha: {venta.anio_venta}\n"
        texto += f"Comprador: {com.nombre_completo() if com else 'N/A'}   (Cédula: {com.cedula if com else 'N/A'})\n"
        texto += f"Vehículo : {veh.marca if veh else 'N/A'} {veh.modelo if veh else 'N/A'} ({veh.anio if veh else 'N/A'})\n"
        texto += "-" * 45 + f"\nPRECIO FINAL PAGADO: ${venta.precio_final:,.2f}"
        return texto

    def total_recaudado(self):
        return round(sum(v.precio_final for v in self.lista), 2)