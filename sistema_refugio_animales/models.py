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


class Adoptante(Persona):
    """Adoptante ES UNA Persona, con teléfono y número de cédula único."""

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


class MascotaRefugio(ModeloBase):
    """MascotaRefugio ES UN ModeloBase. Contiene atributos y métodos estáticos de costo administrativo."""

    TARIFA_TRAMITE = 25.0  # Atributo estático (Costo fijo de esterilización y vacunas)
    TOTAL_MASCOTAS = 0

    def __init__(self, id_registro, chip_id, nombre_mascota, especie, edad_meses, disponible=True):
        super().__init__(id_registro)
        self.chip_id = str(chip_id).strip().upper()
        self.nombre_mascota = str(nombre_mascota).title()
        self.especie = str(especie).title()  # Perro, Gato, Conejo, etc.
        self.edad_meses = int(edad_meses) if edad_meses != "" else 12
        self.disponible = disponible if isinstance(disponible, bool) else (str(disponible).lower() == 'true')
        MascotaRefugio.TOTAL_MASCOTAS += 1

    @staticmethod
    def calcular_costo_total_adopcion(donacion_voluntaria=0.0):
        try:
            donacion = float(donacion_voluntaria)
            return round(MascotaRefugio.TARIFA_TRAMITE + donacion, 2)
        except (TypeError, ValueError):
            return MascotaRefugio.TARIFA_TRAMITE

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["chip_id"] = self.chip_id
        datos["nombre_mascota"] = self.nombre_mascota
        datos["especie"] = self.especie
        datos["edad_meses"] = self.edad_meses
        datos["disponible"] = self.disponible
        return datos

    def etiqueta(self):
        estado = "Disponible" if self.disponible else "Adoptado"
        return f"[{self.chip_id}] {self.nombre_mascota} ({self.especie}, {self.edad_meses} meses) · [{estado}]"


class ProcesoAdopcion(ModeloBase):
    """ProcesoAdopcion: une un adoptante y una mascota con el costo total y fecha."""

    def __init__(self, id_registro, adoptante_id, mascota_id, costo_total=0.0, fecha_adopcion=""):
        super().__init__(id_registro)
        self.adoptante_id = int(adoptante_id)
        self.mascota_id = int(mascota_id)
        self.costo_total = float(costo_total) if costo_total != "" else 0.0
        self.fecha_adopcion = fecha_adopcion or date.today().isoformat()

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["adoptante_id"] = self.adoptante_id
        datos["mascota_id"] = self.mascota_id
        datos["costo_total"] = self.costo_total
        datos["fecha_adopcion"] = self.fecha_adopcion
        return datos

    def etiqueta(self):
        return f"Adopción #{self.id} · Adoptante ID: {self.adoptante_id} · Mascota ID: {self.mascota_id} · Total: ${self.costo_total:.2f}"