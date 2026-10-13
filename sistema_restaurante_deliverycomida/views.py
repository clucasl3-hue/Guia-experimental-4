from abc import ABC, abstractmethod
import os

from models import Comensal, PlatilloMenu, PedidoRestaurante
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


class ComensalController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "comensales.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Comensal.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([c.a_diccionario() for c in self.lista])

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "apellido", "email"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"
        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            if not es_email_valido(email): return f"Email inválido: '{email}'"
            if email in {c.email for c in self.lista if c.id != id_actual}:
                return "Ese email ya está registrado"
        return None

    def leer(self): return self.lista
    def obtener(self, id_c):
        for c in self.lista:
            if c.id == id_c: return c
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [c for c in self.lista if t in c.nombre.lower() or t in c.apellido.lower() or t in c.email.lower()]

    def siguiente(self):
        return max([c.id for c in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        comensal = Comensal(
            self.siguiente(), str(datos["nombre"]).strip().title(),
            str(datos["apellido"]).strip().title(), str(datos["email"]).strip().lower(),
            str(datos.get("direccion", "")).strip(), str(datos.get("telefono", "")).strip()
        )
        self.lista.append(comensal)
        self.guardar()
        return True, f"Comensal registrado: {comensal.etiqueta()}"

    def actualizar(self, id_c, datos):
        c = self.obtener(id_c)
        if not c: return False, "No existe"
        error = self.validar(datos, id_c)
        if error: return False, error
        for k, v in datos.items():
            val = str(v).strip()
            if k in ("nombre", "apellido"): val = val.title()
            elif k == "email": val = val.lower()
            setattr(c, k, val)
        self.guardar()
        return True, f"Comensal {id_c} actualizado"

    def eliminar(self, id_c):
        c = self.obtener(id_c)
        if not c: return False, "No existe"
        self.lista.remove(c)
        self.guardar()
        return True, "Comensal eliminado"


class PlatilloMenuController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "platillos.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [PlatilloMenu.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([p.a_diccionario() for p in self.lista])

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre_platillo", "categoria", "precio"):
                if str(datos.get(campo, "")).strip() == "": return f"El campo {campo} es obligatorio"
        return None

    def leer(self): return self.lista
    def obtener(self, id_p):
        for p in self.lista:
            if p.id == id_p: return p
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [p for p in self.lista if t in p.nombre_platillo.lower() or t in p.categoria.lower()]

    def siguiente(self):
        return max([p.id for p in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        platillo = PlatilloMenu(
            self.siguiente(), str(datos["nombre_platillo"]).strip().title(),
            str(datos["categoria"]).strip().title(), float(datos["precio"])
        )
        self.lista.append(platillo)
        self.guardar()
        return True, f"Platillo registrado: {platillo.etiqueta()}"

    def actualizar(self, id_p, datos):
        p = self.obtener(id_p)
        if not p: return False, "No existe"
        error = self.validar(datos, id_p)
        if error: return False, error
        if "nombre_platillo" in datos: p.nombre_platillo = str(datos["nombre_platillo"]).strip().title()
        if "categoria" in datos: p.categoria = str(datos["categoria"]).strip().title()
        if "precio" in datos and str(datos["precio"]).strip() != "": p.precio = float(datos["precio"])
        self.guardar()
        return True, "Platillo actualizado"

    def eliminar(self, id_p):
        p = self.obtener(id_p)
        if not p: return False, "No existe"
        self.lista.remove(p)
        self.guardar()
        return True, "Platillo eliminado"


class PedidoRestauranteController(CrudBase):
    def __init__(self, comensales, platillos, archivo=None):
        self.comensales = comensales
        self.platillos = platillos
        ruta = archivo or os.path.join(DATA_DIR, "pedidos_restaurante.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [PedidoRestaurante.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([ped.a_diccionario() for ped in self.lista])

    def validar(self, datos):
        try:
            com_id = int(datos.get("comensal_id", 0))
            pla_id = int(datos.get("platillo_id", 0))
            cant = int(datos.get("cantidad", 0))
        except (TypeError, ValueError):
            return "IDs o cantidades inválidas"
        if not self.comensales.obtener(com_id): return "No existe el comensal"
        if not self.platillos.obtener(pla_id): return "No existe el platillo"
        if cant <= 0: return "La cantidad debe ser mayor a 0"
        return None

    def leer(self): return self.lista
    def obtener(self, id_ped):
        for ped in self.lista:
            if ped.id == id_ped: return ped
        return None

    def buscar(self, t):
        return [ped for ped in self.lista if t.strip() in ped.fecha]

    def siguiente(self):
        return max([ped.id for ped in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        platillo = self.platillos.obtener(int(datos["platillo_id"]))
        cant = int(datos["cantidad"])
        con_delivery = datos.get("con_delivery", True)

        costo_total = PlatilloMenu.calcular_total_pedido(platillo.precio, cant, con_delivery)

        pedido = PedidoRestaurante(
            self.siguiente(), int(datos["comensal_id"]), platillo.id,
            cant, costo_total
        )
        self.lista.append(pedido)
        self.guardar()
        return True, f"Pedido #{pedido.id} registrado con éxito. Total (incl. delivery): ${costo_total:.2f}"

    def actualizar(self, id_ped, datos): return False, "Los pedidos no se modifican"

    def eliminar(self, id_ped):
        ped = self.obtener(id_ped)
        if not ped: return False, "No existe"
        self.lista.remove(ped)
        self.guardar()
        return True, "Pedido cancelado"

    def comprobante_pedido(self, id_ped):
        ped = self.obtener(id_ped)
        if not ped: return None
        c = self.comensales.obtener(ped.comensal_id)
        p = self.platillos.obtener(ped.platillo_id)
        texto = f"COMPROBANTE RESTAURANTE - PEDIDO #{ped.id}   Fecha: {ped.fecha}\n"
        texto += f"Comensal: {c.nombre_completo() if c else 'N/A'}   (Dir: {c.direccion if c else 'N/A'})\n"
        texto += f"Platillo: {p.nombre_platillo if p else 'N/A'} x {ped.cantidad}\n"
        texto += f"Tarifa de Delivery fija: ${PlatilloMenu.TARIFA_DELIVERY:.2f}\n"
        texto += "-" * 50 + f"\nTOTAL PAGADO: ${ped.costo_total:.2f}"
        return texto

    def total_recaudado(self):
        return round(sum(ped.costo_total for ped in self.lista), 2)