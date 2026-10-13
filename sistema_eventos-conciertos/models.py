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


class Asistente(Persona):
    """Asistente ES UNA Persona, con teléfono y número de cédula único."""

    def __init__(self, id_registro, nombre, apellido, email, cedula="", telefono=""):
        super().__init__(id_registro, nombre, apellido, email)
        self.cedula = str(cedula).strip()
        self.telefono = str(telefono).strip()

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["cedula"] = self.cedula
        datos["telefono"] = self.telefono
        return datos

    def etiqueta(self):
        return f"{super().etiqueta()} · Cédula: {self.cedula} · Tel: {self.telefono or 'N/D'}"


class EventoConcierto(ModeloBase):
    """EventoConcierto ES UN ModeloBase. Contiene atributos y métodos estáticos de recargo VIP."""

    RECARGO_VIP = 25.0  # Atributo estático ($ adicional para zona VIP)
    TOTAL_EVENTOS = 0

    def __init__(self, id_registro, nombre_evento, codigo_evento, precio_base, aforo_maximo):
        super().__init__(id_registro)
        self.nombre_evento = str(nombre_evento).title()
        self.codigo_evento = str(codigo_evento).strip().upper()
        self.precio_base = float(precio_base) if precio_base != "" else 30.0
        self.aforo_maximo = int(aforo_maximo) if aforo_maximo != "" else 100
        EventoConcierto.TOTAL_EVENTOS += 1

    @staticmethod
    def calcular_costo_entrada(precio_base, es_vip=False):
        try:
            base = float(precio_base)
            extra = EventoConcierto.RECARGO_VIP if es_vip else 0.0
            return round(base + extra, 2)
        except (TypeError, ValueError):
            return 0.0

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["nombre_evento"] = self.nombre_evento
        datos["codigo_evento"] = self.codigo_evento
        datos["precio_base"] = self.precio_base
        datos["aforo_maximo"] = self.aforo_maximo
        return datos

    def etiqueta(self):
        return f"[{self.codigo_evento}] {self.nombre_evento} · Base: ${self.precio_base:.2f} · Aforo: {self.aforo_maximo}"


class EntradaConcierto(ModeloBase):
    """EntradaConcierto: une un asistente y un evento con tipo de localidad y costo final."""

    def __init__(self, id_registro, asistente_id, evento_id, tipo_localidad="General", costo_total=0.0, fecha_compra=""):
        super().__init__(id_registro)
        self.asistente_id = int(asistente_id)
        self.evento_id = int(evento_id)
        self.tipo_localidad = str(tipo_localidad).title()  # General o Vip
        self.costo_total = float(costo_total) if costo_total != "" else 0.0
        self.fecha_compra = fecha_compra or date.today().isoformat()

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["asistente_id"] = self.asistente_id
        datos["evento_id"] = self.evento_id
        datos["tipo_localidad"] = self.tipo_localidad
        datos["costo_total"] = self.costo_total
        datos["fecha_compra"] = self.fecha_compra
        return datos

    def etiqueta(self):
        return f"Entrada #{self.id} [{self.tipo_localidad}] · Asistente ID: {self.asistente_id} · Evento ID: {self.evento_id} · Total: ${self.costo_total:.2f}"