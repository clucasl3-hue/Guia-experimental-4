from abc import ABC, abstractmethod
import os

from models import Proveedor, ProductoBodega, MovimientoStock
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


class ProveedorController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "proveedores.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Proveedor.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([p.a_diccionario() for p in self.lista])

    def rucs_registrados(self, excepto_id=None):
        return {p.ruc.strip() for p in self.lista if p.id != excepto_id and p.ruc}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "apellido", "email", "ruc"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"
        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            if not es_email_valido(email): return f"Email inválido: '{email}'"
            if email in {p.email for p in self.lista if p.id != id_actual}:
                return "Ese email ya está registrado"
        if "ruc" in datos:
            ruc = str(datos["ruc"]).strip()
            if ruc in self.rucs_registrados(id_actual):
                return f"El RUC '{ruc}' ya está registrado"
        return None

    def leer(self): return self.lista
    def obtener(self, id_p):
        for p in self.lista:
            if p.id == id_p: return p
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [p for p in self.lista if t in p.nombre.lower() or t in p.apellido.lower() or t in p.ruc.lower()]

    def siguiente(self):
        return max([p.id for p in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        proveedor = Proveedor(
            self.siguiente(), str(datos["nombre"]).strip().title(),
            str(datos["apellido"]).strip().title(), str(datos["email"]).strip().lower(),
            str(datos["ruc"]).strip(), str(datos.get("telefono", "")).strip()
        )
        self.lista.append(proveedor)
        self.guardar()
        return True, f"Proveedor registrado: {proveedor.etiqueta()}"

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
        return True, f"Proveedor {id_p} actualizado"

    def eliminar(self, id_p):
        p = self.obtener(id_p)
        if not p: return False, "No existe"
        self.lista.remove(p)
        self.guardar()
        return True, "Proveedor eliminado"


class ProductoBodegaController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "productos_bodega.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [ProductoBodega.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([p.a_diccionario() for p in self.lista])

    def skus_registrados(self, excepto_id=None):
        return {p.sku.strip().upper() for p in self.lista if p.id != excepto_id and p.sku}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("sku", "nombre_producto", "stock_actual", "precio_costo"):
                if str(datos.get(campo, "")).strip() == "": return f"El campo {campo} es obligatorio"
        if "sku" in datos:
            sku = str(datos["sku"]).strip().upper()
            if sku in self.skus_registrados(id_actual): return f"El SKU '{sku}' ya existe"
        return None

    def leer(self): return self.lista
    def obtener(self, id_p):
        for p in self.lista:
            if p.id == id_p: return p
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [p for p in self.lista if t in p.sku.lower() or t in p.nombre_producto.lower()]

    def siguiente(self):
        return max([p.id for p in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        producto = ProductoBodega(
            self.siguiente(), str(datos["sku"]).strip().upper(),
            str(datos["nombre_producto"]).strip().title(), int(datos["stock_actual"]),
            float(datos["precio_costo"])
        )
        self.lista.append(producto)
        self.guardar()
        return True, f"Producto registrado: {producto.etiqueta()}"

    def actualizar(self, id_p, datos):
        p = self.obtener(id_p)
        if not p: return False, "No existe"
        error = self.validar(datos, id_p)
        if error: return False, error
        if "sku" in datos: p.sku = str(datos["sku"]).strip().upper()
        if "nombre_producto" in datos: p.nombre_producto = str(datos["nombre_producto"]).strip().title()
        if "stock_actual" in datos and str(datos["stock_actual"]).strip() != "": p.stock_actual = int(datos["stock_actual"])
        if "precio_costo" in datos and str(datos["precio_costo"]).strip() != "": p.precio_costo = float(datos["precio_costo"])
        self.guardar()
        return True, "Producto actualizado"

    def eliminar(self, id_p):
        p = self.obtener(id_p)
        if not p: return False, "No existe"
        self.lista.remove(p)
        self.guardar()
        return True, "Producto eliminado"


class MovimientoStockController(CrudBase):
    def __init__(self, proveedores, productos, archivo=None):
        self.proveedores = proveedores
        self.productos = productos
        ruta = archivo or os.path.join(DATA_DIR, "movimientos_stock.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [MovimientoStock.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([m.a_diccionario() for m in self.lista])

    def validar(self, datos):
        try:
            prov_id = int(datos.get("proveedor_id", 0))
            prod_id = int(datos.get("producto_id", 0))
            cant = int(datos.get("cantidad", 0))
        except (TypeError, ValueError):
            return "IDs o cantidades inválidas"
        if not self.proveedores.obtener(prov_id): return "No existe el proveedor"
        producto = self.productos.obtener(prod_id)
        if not producto: return "No existe el producto"
        if cant <= 0: return "La cantidad debe ser mayor a 0"
        
        tipo = str(datos.get("tipo_movimiento", "")).title()
        if tipo == "Salida" and producto.stock_actual < cant:
            return f"Stock insuficiente. Stock actual de {producto.nombre_producto}: {producto.stock_actual}"
        return None

    def leer(self): return self.lista
    def obtener(self, id_m):
        for m in self.lista:
            if m.id == id_m: return m
        return None

    def buscar(self, t):
        return [m for m in self.lista if t.strip() in m.tipo_movimiento.lower() or t.strip() in m.fecha]

    def siguiente(self):
        return max([m.id for m in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        producto = self.productos.obtener(int(datos["producto_id"]))
        cant = int(datos["cantidad"])
        tipo = str(datos["tipo_movimiento"]).title()

        costo_total = ProductoBodega.calcular_valor_total(producto.precio_costo, cant)

        movimiento = MovimientoStock(
            self.siguiente(), int(datos["proveedor_id"]), producto.id,
            tipo, cant, costo_total, str(datos.get("fecha", "")).strip()
        )

        # Actualizar stock del producto según el tipo de movimiento
        if tipo == "Entrada":
            producto.stock_actual += cant
        elif tipo == "Salida":
            producto.stock_actual -= cant

        self.productos.guardar()
        self.lista.append(movimiento)
        self.guardar()
        return True, f"Movimiento #{movimiento.id} [{tipo}] registrado. Stock actualizado de {producto.nombre_producto}: {producto.stock_actual} unids."

    def actualizar(self, id_m, datos): return False, "Los movimientos de inventario no se modifican"

    def eliminar(self, id_m):
        m = self.obtener(id_m)
        if not m: return False, "No existe"
        
        # Revertir stock al eliminar el movimiento
        producto = self.productos.obtener(m.producto_id)
        if producto:
            if m.tipo_movimiento == "Entrada":
                producto.stock_actual -= m.cantidad
            elif m.tipo_movimiento == "Salida":
                producto.stock_actual += m.cantidad
            self.productos.guardar()

        self.lista.remove(m)
        self.guardar()
        return True, "Movimiento eliminado y stock revertido"

    def comprobante_movimiento(self, id_m):
        m = self.obtener(id_m)
        if not m: return None
        p = self.proveedores.obtener(m.proveedor_id)
        prod = self.productos.obtener(m.producto_id)
        texto = f"COMPROBANTE DE BODEGA - MOVIMIENTO #{m.id}   Fecha: {m.fecha}\n"
        texto += f"Proveedor : {p.nombre_completo() if p else 'N/A'}   (RUC: {p.ruc if p else 'N/A'})\n"
        texto += f"Producto  : [{prod.sku if prod else 'N/A'}] {prod.nombre_producto if prod else 'N/A'}\n"
        texto += f"Tipo      : {m.tipo_movimiento}   ·   Cantidad: {m.cantidad} unidades\n"
        texto += "-" * 50 + f"\nVALOR TOTAL: ${m.costo_total:.2f}"
        return texto

    def total_invertido(self):
        return round(sum(m.costo_total for m in self.lista if m.tipo_movimiento == "Entrada"), 2)