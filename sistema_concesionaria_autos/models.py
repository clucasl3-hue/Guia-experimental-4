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


class Comprador(Persona):
    """Comprador ES UNA Persona, con cédula y presupuesto."""

    def __init__(self, id_registro, nombre, apellido, email, cedula="", presupuesto=0.0):
        super().__init__(id_registro, nombre, apellido, email)
        self.cedula = cedula
        self.presupuesto = float(presupuesto) if presupuesto != "" else 0.0

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["cedula"] = self.cedula
        datos["presupuesto"] = self.presupuesto
        return datos

    def etiqueta(self):
        return f"{super().etiqueta()} · Cédula: {self.cedula} · Presupuesto: ${self.presupuesto:,.2f}"


class Vehiculo(ModeloBase):
    """Vehículo ES UN ModeloBase. Contiene tupla estática de marcas y control de stock."""

    MARCAS_PERMITIDAS = ("TOYOTA", "CHEVROLET", "HYUNDAI", "KIA", "FORD", "NISSAN")  # TUPLA ESTÁTICA
    TOTAL_VEHICULOS = 0

    def __init__(self, id_registro, marca, modelo, anio, precio_base, stock=1):
        super().__init__(id_registro)
        self.marca = str(marca).upper()
        self.modelo = modelo
        self.anio = int(anio) if anio != "" else 2026
        self.precio_base = float(precio_base) if precio_base != "" else 15000.0
        self.stock = int(stock) if stock != "" else 1
        Vehiculo.TOTAL_VEHICULOS += 1

    @staticmethod
    def es_marca_valida(marca):
        return str(marca).strip().upper() in Vehiculo.MARCAS_PERMITIDAS

    def hay_stock(self):
        return self.stock > 0

    def descontar_stock(self):
        if self.stock > 0:
            self.stock -= 1

    def aumentar_stock(self):
        self.stock += 1

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["marca"] = self.marca
        datos["modelo"] = self.modelo
        datos["anio"] = self.anio
        datos["precio_base"] = self.precio_base
        datos["stock"] = self.stock
        return datos

    def etiqueta(self):
        alerta = " ⚠ sin stock" if not self.hay_stock() else ""
        return f"{self.marca} {self.modelo} ({self.anio}) · Precio: ${self.precio_base:,.2f} · Stock: {self.stock}{alerta}"


class VentaVehiculo(ModeloBase):
    """Venta: une un comprador y un vehículo con año de venta y precio final."""

    def __init__(self, id_registro, comprador_id, vehiculo_id, anio_venta="", precio_final=0.0):
        super().__init__(id_registro)
        self.comprador_id = int(comprador_id)
        self.vehiculo_id = int(vehiculo_id)
        self.anio_venta = anio_venta or date.today().isoformat()
        self.precio_final = float(precio_final) if precio_final != "" else 0.0

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["comprador_id"] = self.comprador_id
        datos["vehiculo_id"] = self.vehiculo_id
        datos["anio_venta"] = self.anio_venta
        datos["precio_final"] = self.precio_final
        return datos

    def etiqueta(self):
        return f"Factura Venta #{self.id} · Comprador ID: {self.comprador_id} · Vehículo ID: {self.vehiculo_id} · Total: ${self.precio_final:,.2f}"