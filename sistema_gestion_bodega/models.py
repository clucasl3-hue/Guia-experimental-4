from datetime import date


class ModeloBase:
    """Padre de todos los modelos. Guarda el id y define el comportamiento común."""

    def __init__(self, id_registro):
        self.id = int(id_registro)

    @classmethod
    def desde_diccionario(cls, datos):
        datos = dict(datos)
        id_registro = datos.pop("id")
        return cls(id_registro, **datos)

    def a_diccionario(self):
        return {"id": self.id}

    def etiqueta(self):
        return f"registro {self.id}"

    def __str__(self):
        return f"[{self.id}] {self.etiqueta()}"


class Persona(ModeloBase):
    """Todo lo que tiene una persona del sistema."""

    def __init__(self, id_registro, nombre, apellido, email):
        super().__init__(id_registro)
        self.nombre = nombre
        self.apellido = apellido
        self.email = email

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["nombre"] = self.nombre
        datos["apellido"] = self.apellido
        datos["email"] = self.email
        return datos

    def etiqueta(self):
        return self.nombre_completo()


class Proveedor(Persona):
    """Proveedor ES UNA Persona, con RUC y teléfono."""

    def __init__(self, id_registro, nombre, apellido, email, ruc="", telefono=""):
        super().__init__(id_registro, nombre, apellido, email)
        self.ruc = str(ruc).strip()
        self.telefono = str(telefono).strip()

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["ruc"] = self.ruc
        datos["telefono"] = self.telefono
        return datos

    def etiqueta(self):
        return f"{super().etiqueta()} · RUC: {self.ruc} · Tel: {self.telefono or 'N/D'}"


class ProductoBodega(ModeloBase):
    """ProductoBodega ES UN ModeloBase. Contiene atributos y métodos estáticos de alerta de stock."""

    STOCK_MINIMO_ALERTA = 5  # Atributo estático
    TOTAL_PRODUCTOS = 0

    def __init__(self, id_registro, sku, nombre_producto, stock_actual, precio_costo):
        super().__init__(id_registro)
        self.sku = str(sku).upper()
        self.nombre_producto = str(nombre_producto).title()
        self.stock_actual = int(stock_actual) if stock_actual != "" else 0
        self.precio_costo = float(precio_costo) if precio_costo != "" else 10.0
        ProductoBodega.TOTAL_PRODUCTOS += 1

    @staticmethod
    def calcular_valor_total(precio, cantidad):
        try:
            return round(float(precio) * int(cantidad), 2)
        except (TypeError, ValueError):
            return 0.0

    def requiere_alerta(self):
        return self.stock_actual <= ProductoBodega.STOCK_MINIMO_ALERTA

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["sku"] = self.sku
        datos["nombre_producto"] = self.nombre_producto
        datos["stock_actual"] = self.stock_actual
        datos["precio_costo"] = self.precio_costo
        return datos

    def etiqueta(self):
        alerta = " ⚠ STOCK BAJO" if self.requiere_alerta() else ""
        return f"[{self.sku}] {self.nombre_producto} · Stock: {self.stock_actual} unids · Costo: ${self.precio_costo:.2f}{alerta}"


class MovimientoStock(ModeloBase):
    """MovimientoStock: registra entrada o salida de inventario cruzando proveedor y producto."""

    def __init__(self, id_registro, proveedor_id, producto_id, tipo_movimiento, cantidad, costo_total=0.0, fecha=""):
        super().__init__(id_registro)
        self.proveedor_id = int(proveedor_id)
        self.producto_id = int(producto_id)
        self.tipo_movimiento = str(tipo_movimiento).title()  # Entrada o Salida
        self.cantidad = int(cantidad) if cantidad != "" else 1
        self.costo_total = float(costo_total) if costo_total != "" else 0.0
        self.fecha = fecha or date.today().isoformat()

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["proveedor_id"] = self.proveedor_id
        datos["producto_id"] = self.producto_id
        datos["tipo_movimiento"] = self.tipo_movimiento
        datos["cantidad"] = self.cantidad
        datos["costo_total"] = self.costo_total
        datos["fecha"] = self.fecha
        return datos

    def etiqueta(self):
        return f"Movimiento #{self.id} [{self.tipo_movimiento}] · Prod ID: {self.producto_id} · Cant: {self.cantidad} · Total: ${self.costo_total:.2f}"