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


class Pasajero(Persona):
    """Pasajero ES UNA Persona, con pasaporte y nacionalidad únicos."""

    def __init__(self, id_registro, nombre, apellido, email, pasaporte="", nacionalidad=""):
        super().__init__(id_registro, nombre, apellido, email)
        self.pasaporte = str(pasaporte).upper()
        self.nacionalidad = str(nacionalidad).title()

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["pasaporte"] = self.pasaporte
        datos["nacionalidad"] = self.nacionalidad
        return datos

    def etiqueta(self):
        return f"{super().etiqueta()} · Pasaporte: {self.pasaporte} · Nacionalidad: {self.nacionalidad or 'N/D'}"


class Vuelo(ModeloBase):
    """Vuelo ES UN ModeloBase. Contiene atributos y métodos estáticos de tasa de aeropuerto."""

    TASA_AEROPUERTO = 25.0  # Atributo estático
    TOTAL_VUELOS = 0

    def __init__(self, id_registro, codigo_vuelo, origen, destino, asientos_disponibles, precio_base):
        super().__init__(id_registro)
        self.codigo_vuelo = str(codigo_vuelo).upper()
        self.origen = str(origen).title()
        self.destino = str(destino).title()
        self.asientos_disponibles = int(asientos_disponibles) if asientos_disponibles != "" else 50
        self.precio_base = float(precio_base) if precio_base != "" else 100.0
        Vuelo.TOTAL_VUELOS += 1

    @staticmethod
    def calcular_total_vuelo(precio_base, tasa):
        try:
            return round(float(precio_base) + float(tasa), 2)
        except (TypeError, ValueError):
            return 0.0

    def hay_asientos(self):
        return self.asientos_disponibles > 0

    def descontar_asiento(self):
        if self.asientos_disponibles > 0:
            self.asientos_disponibles -= 1

    def aumentar_asiento(self):
        self.asientos_disponibles += 1

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["codigo_vuelo"] = self.codigo_vuelo
        datos["origen"] = self.origen
        datos["destino"] = self.destino
        datos["asientos_disponibles"] = self.asientos_disponibles
        datos["precio_base"] = self.precio_base
        return datos

    def etiqueta(self):
        alerta = " ⚠ vuelo lleno" if not self.hay_asientos() else ""
        return f"Vuelo {self.codigo_vuelo}: {self.origen} ➔ {self.destino} · ${self.precio_base:.2f} · Asientos: {self.asientos_disponibles}{alerta}"


class BoletoAvion(ModeloBase):
    """BoletoAvion: une un pasajero y un vuelo con clase de asiento y precio total."""

    def __init__(self, id_registro, pasajero_id, vuelo_id, clase_asiento="Economica", precio_unitario=0.0):
        super().__init__(id_registro)
        self.pasajero_id = int(pasajero_id)
        self.vuelo_id = int(vuelo_id)
        self.clase_asiento = str(clase_asiento).title()
        self.precio_unitario = float(precio_unitario) if precio_unitario != "" else 0.0

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["pasajero_id"] = self.pasajero_id
        datos["vuelo_id"] = self.vuelo_id
        datos["clase_asiento"] = self.clase_asiento
        datos["precio_unitario"] = self.precio_unitario
        return datos

    def etiqueta(self):
        return f"Boleto Avión #{self.id} [{self.clase_asiento}] · Pasajero ID: {self.pasajero_id} · Vuelo ID: {self.vuelo_id} · Total: ${self.precio_unitario:.2f}"