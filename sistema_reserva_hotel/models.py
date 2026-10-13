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


class Huesped(Persona):
    """Huésped ES UNA Persona, con pasaporte y país de origen."""

    def __init__(self, id_registro, nombre, apellido, email, pasaporte="", pais=""):
        super().__init__(id_registro, nombre, apellido, email)
        self.pasaporte = pasaporte
        self.pais = pais

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["pasaporte"] = self.pasaporte
        datos["pais"] = self.pais
        return datos

    def etiqueta(self):
        return f"{super().etiqueta()} · Pasaporte: {self.pasaporte} · País: {self.pais or 'N/D'}"


class Habitacion(ModeloBase):
    """Habitación ES UN ModeloBase. Contiene atributos y métodos estáticos."""

    IMPUESTO_HOTEL = 0.12      # Atributo estático (12% de impuesto)
    TOTAL_HABITACIONES = 0

    def __init__(self, id_registro, numero_habitacion, tipo, precio_noche, disponible=True):
        super().__init__(id_registro)
        self.numero_habitacion = str(numero_habitacion).upper()
        self.tipo = tipo            # Simple, Doble, Suite
        self.precio_noche = float(precio_noche) if precio_noche != "" else 50.0
        self.disponible = disponible if isinstance(disponible, bool) else (str(disponible).lower() == 'true')
        Habitacion.TOTAL_HABITACIONES += 1

    @staticmethod
    def calcular_subtotal(precio_noche, noches):
        try:
            return round(float(precio_noche) * int(noches), 2)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def calcular_total_con_impuesto(subtotal):
        return round(subtotal * (1 + Habitacion.IMPUESTO_HOTEL), 2)

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["numero_habitacion"] = self.numero_habitacion
        datos["tipo"] = self.tipo
        datos["precio_noche"] = self.precio_noche
        datos["disponible"] = self.disponible
        return datos

    def etiqueta(self):
        estado = "Disponible" if self.disponible else "Ocupada"
        return f"Habitación {self.numero_habitacion} ({self.tipo}) · ${self.precio_noche:.2f}/noche · [{estado}]"


class Reserva(ModeloBase):
    """Reserva: une un huésped y una habitación con número de noches y total."""

    def __init__(self, id_registro, huesped_id, habitacion_id, noches, fecha_inicio="", total=0.0):
        super().__init__(id_registro)
        self.huesped_id = int(huesped_id)
        self.habitacion_id = int(habitacion_id)
        self.noches = int(noches) if noches != "" else 1
        self.fecha_inicio = fecha_inicio or date.today().isoformat()
        self.total = float(total) if total != "" else 0.0

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["huesped_id"] = self.huesped_id
        datos["habitacion_id"] = self.habitacion_id
        datos["noches"] = self.noches
        datos["fecha_inicio"] = self.fecha_inicio
        datos["total"] = self.total
        return datos

    def etiqueta(self):
        return f"Reserva #{self.id} · Huésped ID: {self.huesped_id} · Hab. ID: {self.habitacion_id} · Total: ${self.total:.2f}"