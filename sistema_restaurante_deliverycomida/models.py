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


class Comensal(Persona):
    """Comensal ES UNA Persona, con dirección de entrega y teléfono."""

    def __init__(self, id_registro, nombre, apellido, email, direccion="", telefono=""):
        super().__init__(id_registro, nombre, apellido, email)
        self.direccion = str(direccion).strip().title()
        self.telefono = str(telefono).strip()

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["direccion"] = self.direccion
        datos["telefono"] = self.telefono
        return datos

    def etiqueta(self):
        return f"{super().etiqueta()} · Dir: {self.direccion or 'N/D'} · Tel: {self.telefono or 'N/D'}"


class PlatilloMenu(ModeloBase):
    """PlatilloMenu ES UN ModeloBase. Contiene atributos y métodos estáticos de delivery."""

    TARIFA_DELIVERY = 3.50  # Atributo estático (Costo fijo de envío)
    TOTAL_PLATILLOS = 0

    def __init__(self, id_registro, nombre_platillo, categoria, precio):
        super().__init__(id_registro)
        self.nombre_platillo = str(nombre_platillo).title()
        self.categoria = str(categoria).title()
        self.precio = float(precio) if precio != "" else 5.0
        PlatilloMenu.TOTAL_PLATILLOS += 1

    @staticmethod
    def calcular_total_pedido(precio_platillo, cantidad, incluir_delivery=True):
        try:
            subtotal = float(precio_platillo) * int(cantidad)
            envio = PlatilloMenu.TARIFA_DELIVERY if incluir_delivery else 0.0
            return round(subtotal + envio, 2)
        except (TypeError, ValueError):
            return 0.0

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["nombre_platillo"] = self.nombre_platillo
        datos["categoria"] = self.categoria
        datos["precio"] = self.precio
        return datos

    def etiqueta(self):
        return f"{self.nombre_platillo} ({self.categoria}) · Precio: ${self.precio:.2f}"


class PedidoRestaurante(ModeloBase):
    """Pedido: une un comensal y un platillo con cantidad, costo total y estado."""

    def __init__(self, id_registro, comensal_id, platillo_id, cantidad=1, costo_total=0.0, fecha=""):
        super().__init__(id_registro)
        self.comensal_id = int(comensal_id)
        self.platillo_id = int(platillo_id)
        self.cantidad = int(cantidad) if cantidad != "" else 1
        self.costo_total = float(costo_total) if costo_total != "" else 0.0
        self.fecha = fecha or date.today().isoformat()

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["comensal_id"] = self.comensal_id
        datos["platillo_id"] = self.platillo_id
        datos["cantidad"] = self.cantidad
        datos["costo_total"] = self.costo_total
        datos["fecha"] = self.fecha
        return datos

    def etiqueta(self):
        return f"Pedido #{self.id} · Comensal ID: {self.comensal_id} · Platillo ID: {self.platillo_id} · Cant: {self.cantidad} · Total: ${self.costo_total:.2f}"