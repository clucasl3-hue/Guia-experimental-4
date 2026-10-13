from abc import ABC, abstractmethod
import os

from models import PropietarioAuto, ServicioTaller, OrdenReparacion
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


class PropietarioAutoController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "propietarios.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [PropietarioAuto.desde_diccionario(d) for d in self.gestor.leer()]

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
        prop = PropietarioAuto(
            self.siguiente(), str(datos["nombre"]).strip().title(),
            str(datos["apellido"]).strip().title(), str(datos["email"]).strip().lower(),
            str(datos["cedula"]).strip(), str(datos.get("telefono", "")).strip()
        )
        self.lista.append(prop)
        self.guardar()
        return True, f"Propietario registrado: {prop.etiqueta()}"

    def actualizar(self, id_p, datos):
        p = self.obtener(id_p)
        if not p: return False, "No existe"
        error = self.validar(datos, id_p)
        if error: return False, error
        for k, v in datos.items():
            val = str(v).strip()
            if k in ("nombre", "apellido"): val = val.title()
            elif k == "email": val = val.lower()
            setattr(p, k, val)
        self.guardar()
        return True, f"Propietario {id_p} actualizado"

    def eliminar(self, id_p):
        p = self.obtener(id_p)
        if not p: return False, "No existe"
        self.lista.remove(p)
        self.guardar()
        return True, "Propietario eliminado"


class ServicioTallerController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "servicios_taller.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [ServicioTaller.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([s.a_diccionario() for s in self.lista])

    def codigos_registrados(self, excepto_id=None):
        return {s.codigo.strip().upper() for s in self.lista if s.id != excepto_id and s.codigo}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre_servicio", "codigo", "costo_repuestos"):
                if str(datos.get(campo, "")).strip() == "": return f"El campo {campo} es obligatorio"
        if "codigo" in datos:
            cod = str(datos["codigo"]).strip().upper()
            if cod in self.codigos_registrados(id_actual): return f"El código '{cod}' ya existe"
        return None

    def leer(self): return self.lista
    def obtener(self, id_s):
        for s in self.lista:
            if s.id == id_s: return s
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [s for s in self.lista if t in s.nombre_servicio.lower() or t in s.codigo.lower()]

    def siguiente(self):
        return max([s.id for s in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        servicio = ServicioTaller(
            self.siguiente(), str(datos["nombre_servicio"]).strip().title(),
            str(datos["codigo"]).strip().upper(), float(datos["costo_repuestos"])
        )
        self.lista.append(servicio)
        self.guardar()
        return True, f"Servicio registrado: {servicio.etiqueta()}"

    def actualizar(self, id_s, datos):
        s = self.obtener(id_s)
        if not s: return False, "No existe"
        error = self.validar(datos, id_s)
        if error: return False, error
        if "nombre_servicio" in datos: s.nombre_servicio = str(datos["nombre_servicio"]).strip().title()
        if "codigo" in datos: s.codigo = str(datos["codigo"]).strip().upper()
        if "costo_repuestos" in datos and str(datos["costo_repuestos"]).strip() != "": s.costo_repuestos = float(datos["costo_repuestos"])
        self.guardar()
        return True, "Servicio actualizado"

    def eliminar(self, id_s):
        s = self.obtener(id_s)
        if not s: return False, "No existe"
        self.lista.remove(s)
        self.guardar()
        return True, "Servicio eliminado"


class OrdenReparacionController(CrudBase):
    def __init__(self, propietarios, servicios, archivo=None):
        self.propietarios = propietarios
        self.servicios = servicios
        ruta = archivo or os.path.join(DATA_DIR, "ordenes_reparacion.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [OrdenReparacion.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([o.a_diccionario() for o in self.lista])

    def validar(self, datos):
        try:
            prop_id = int(datos.get("propietario_id", 0))
            serv_id = int(datos.get("servicio_id", 0))
        except (TypeError, ValueError):
            return "IDs inválidos"
        if not self.propietarios.obtener(prop_id): return "No existe el propietario"
        if not self.servicios.obtener(serv_id): return "No existe el servicio"
        if str(datos.get("placa_vehiculo", "")).strip() == "": return "La placa del vehículo es obligatoria"
        return None

    def leer(self): return self.lista
    def obtener(self, id_o):
        for o in self.lista:
            if o.id == id_o: return o
        return None

    def buscar(self, t):
        return [o for o in self.lista if t.strip().upper() in o.placa_vehiculo or t.strip() in o.fecha]

    def siguiente(self):
        return max([o.id for o in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        servicio = self.servicios.obtener(int(datos["servicio_id"]))
        urgencia = float(datos.get("urgencia_extra", 0.0))

        costo_total = ServicioTaller.calcular_costo_reparacion(servicio.costo_repuestos, urgencia)

        orden = OrdenReparacion(
            self.siguiente(), int(datos["propietario_id"]), servicio.id,
            str(datos["placa_vehiculo"]).strip().upper(), costo_total,
            str(datos.get("fecha", "")).strip()
        )
        self.lista.append(orden)
        self.guardar()
        return True, f"Orden de Reparación #{orden.id} generada con éxito. Total (incl. mano de obra base): ${costo_total:.2f}"

    def actualizar(self, id_o, datos): return False, "Las órdenes cerradas no se modifican"

    def eliminar(self, id_o):
        o = self.obtener(id_o)
        if not o: return False, "No existe"
        self.lista.remove(o)
        self.guardar()
        return True, "Orden de reparación cancelada"

    def comprobante_orden(self, id_o):
        o = self.obtener(id_o)
        if not o: return None
        p = self.propietarios.obtener(o.propietario_id)
        s = self.servicios.obtener(o.servicio_id)
        texto = f"ORDEN DE REPARACIÓN TALLER #{o.id}   Fecha: {o.fecha}\n"
        texto += f"Propietario : {p.nombre_completo() if p else 'N/A'}   (Cédula: {p.cedula if p else 'N/A'})\n"
        texto += f"Vehículo Placa: {o.placa_vehiculo}\n"
        texto += f"Servicio    : {s.nombre_servicio if s else 'N/A'} [{s.codigo if s else 'N/A'}]\n"
        texto += f"Mano de obra base: ${ServicioTaller.MANO_OBRA_BASE:.2f}\n"
        texto += "-" * 50 + f"\nTOTAL A PAGAR: ${o.costo_total:.2f}"
        return texto

    def total_recaudado(self):
        return round(sum(o.costo_total for o in self.lista), 2)