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


class Remitente(Persona):
    """Remitente ES UNA Persona, con RUC/Cédula y teléfono."""

    def __init__(self, id_registro, nombre, apellido, email, ruc_cedula="", telefono=""):
        super().__init__(id_registro, nombre, apellido, email)
        self.ruc_cedula = str(ruc_cedula).strip()
        self.telefono = str(telefono).strip()

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["ruc_cedula"] = self.ruc_cedula
        datos["telefono"] = self.telefono
        return datos

    def etiqueta(self):
        return f"{super().etiqueta()} · RUC/Cédula: {self.ruc_cedula} · Tel: {self.telefono or 'N/D'}"


class ZonaEnvio(ModeloBase):
    """ZonaEnvio ES UN ModeloBase. Contiene peso máximo estático y tarifa por kg."""

    PESO_MAXIMO_PERMITIDO = 50.0  # Atributo estático (kg)
    TOTAL_ZONAS = 0

    def __init__(self, id_registro, nombre_zona, codigo_postal, tarifa_base_kg):
        super().__init__(id_registro)
        self.nombre_zona = str(nombre_zona).title()
        self.codigo_postal = str(codigo_postal).upper()
        self.tarifa_base_kg = float(tarifa_base_kg) if tarifa_base_kg != "" else 3.50
        ZonaEnvio.TOTAL_ZONAS += 1

    @staticmethod
    def es_peso_valido(peso):
        try:
            val = float(peso)
            return 0 < val <= ZonaEnvio.PESO_MAXIMO_PERMITIDO
        except (TypeError, ValueError):
            return False

    @staticmethod
    def calcular_costo_envio(tarifa, peso):
        try:
            return round(float(tarifa) * float(peso), 2)
        except (TypeError, ValueError):
            return 0.0

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["nombre_zona"] = self.nombre_zona
        datos["codigo_postal"] = self.codigo_postal
        datos["tarifa_base_kg"] = self.tarifa_base_kg
        return datos

    def etiqueta(self):
        return f"Zona: {self.nombre_zona} ({self.codigo_postal}) · Tarifa/kg: ${self.tarifa_base_kg:.2f}"


class PaqueteEnvio(ModeloBase):
    """Paquete: une un remitente y una zona con peso, descripción y costo final."""

    def __init__(self, id_registro, remitente_id, zona_id, peso_kg, descripcion="", costo_total=0.0, fecha_envio=""):
        super().__init__(id_registro)
        self.remitente_id = int(remitente_id)
        self.zona_id = int(zona_id)
        self.peso_kg = float(peso_kg) if peso_kg != "" else 1.0
        self.descripcion = str(descripcion).capitalize()
        self.costo_total = float(costo_total) if costo_total != "" else 0.0
        self.fecha_envio = fecha_envio or date.today().isoformat()

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["remitente_id"] = self.remitente_id
        datos["zona_id"] = self.zona_id
        datos["peso_kg"] = self.peso_kg
        datos["descripcion"] = self.descripcion
        datos["costo_total"] = self.costo_total
        datos["fecha_envio"] = self.fecha_envio
        return datos

    def etiqueta(self):
        return f"Paquete #{self.id} · Remitente ID: {self.remitente_id} · Peso: {self.peso_kg}kg · Total: ${self.costo_total:.2f}"