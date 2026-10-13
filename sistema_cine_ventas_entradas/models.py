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


class ClienteCine(Persona):
    """ClienteCine ES UNA Persona, con tarjeta de fidelidad única."""

    def __init__(self, id_registro, nombre, apellido, email, tarjeta_fidelidad=""):
        super().__init__(id_registro, nombre, apellido, email)
        self.tarjeta_fidelidad = tarjeta_fidelidad

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["tarjeta_fidelidad"] = self.tarjeta_fidelidad
        return datos

    def etiqueta(self):
        return f"{super().etiqueta()} · Tarjeta: {self.tarjeta_fidelidad or 'Sin tarjeta'}"


class Pelicula(ModeloBase):
    """Película ES UN ModeloBase. Contiene atributos y métodos estáticos."""

    PRECIO_GENERAL = 8.50      # Atributo estático
    TOTAL_PELICULAS = 0

    def __init__(self, id_registro, titulo, genero, duracion_min, asientos_disponibles=50):
        super().__init__(id_registro)
        self.titulo = titulo
        self.genero = genero
        self.duracion_min = int(duracion_min) if duracion_min != "" else 120
        self.asientos_disponibles = int(asientos_disponibles) if asientos_disponibles != "" else 50
        Pelicula.TOTAL_PELICULAS += 1

    @staticmethod
    def es_duracion_valida(minutos):
        try:
            return int(minutos) > 0
        except (TypeError, ValueError):
            return False

    def hay_asientos(self, cantidad=1):
        return self.asientos_disponibles >= cantidad

    def ocupar_asientos(self, cantidad):
        if self.hay_asientos(cantidad):
            self.asientos_disponibles -= cantidad

    def liberar_asientos(self, cantidad):
        self.asientos_disponibles += cantidad

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["titulo"] = self.titulo
        datos["genero"] = self.genero
        datos["duracion_min"] = self.duracion_min
        datos["asientos_disponibles"] = self.asientos_disponibles
        return datos

    def etiqueta(self):
        alerta = " ⚠ sala llena" if not self.hay_asientos() else ""
        return f"'{self.titulo}' ({self.genero}) · {self.duracion_min} min · Asientos: {self.asientos_disponibles}{alerta}"


class Boleto(ModeloBase):
    """Boleto: une un cliente y una película con cantidad de boletos y sala."""

    def __init__(self, id_registro, cliente_id, pelicula_id, cantidad_boletos=1, sala="Sala 1", total_pagado=0.0):
        super().__init__(id_registro)
        self.cliente_id = int(cliente_id)
        self.pelicula_id = int(pelicula_id)
        self.cantidad_boletos = int(cantidad_boletos) if cantidad_boletos != "" else 1
        self.sala = sala
        self.total_pagado = float(total_pagado) if total_pagado != "" else 0.0

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["cliente_id"] = self.cliente_id
        datos["pelicula_id"] = self.pelicula_id
        datos["cantidad_boletos"] = self.cantidad_boletos
        datos["sala"] = self.sala
        datos["total_pagado"] = self.total_pagado
        return datos

    def etiqueta(self):
        return f"Boleto #{self.id} · Cliente ID: {self.cliente_id} · Película ID: {self.pelicula_id} · Cant: {self.cantidad_boletos} · Total: ${self.total_pagado:.2f}"