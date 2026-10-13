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


class Duenio(Persona):
    """Dueño ES UNA Persona, con teléfono y dirección."""

    def __init__(self, id_registro, nombre, apellido, email, telefono="", direccion=""):
        super().__init__(id_registro, nombre, apellido, email)
        self.telefono = telefono
        self.direccion = direccion

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["telefono"] = self.telefono
        datos["direccion"] = self.direccion
        return datos

    def etiqueta(self):
        return f"{super().etiqueta()} · Tel: {self.telefono or 'N/D'} · Dir: {self.direccion or 'N/D'}"


class ServicioVeterinario(ModeloBase):
    """ServicioVeterinario ES UN ModeloBase. Contiene atributos y métodos estáticos."""

    DESCUENTO_AFILIADO = 0.15  # Atributo estático (15% de descuento)
    TOTAL_SERVICIOS = 0

    def __init__(self, id_registro, nombre_servicio, codigo, costo):
        super().__init__(id_registro)
        self.nombre_servicio = nombre_servicio
        self.codigo = str(codigo).upper()
        self.costo = float(costo) if costo != "" else 20.0
        ServicioVeterinario.TOTAL_SERVICIOS += 1

    @staticmethod
    def calcular_costo_final(costo_base, es_afiliado=False):
        try:
            base = float(costo_base)
            if es_afiliado:
                return round(base * (1 - ServicioVeterinario.DESCUENTO_AFILIADO), 2)
            return round(base, 2)
        except (TypeError, ValueError):
            return 0.0

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["nombre_servicio"] = self.nombre_servicio
        datos["codigo"] = self.codigo
        datos["costo"] = self.costo
        return datos

    def etiqueta(self):
        return f"{self.nombre_servicio} ({self.codigo}) · Costo base: ${self.costo:.2f}"


class HistorialAtencion(ModeloBase):
    """Historial: une un dueño y un servicio médico veterinario para una mascota."""

    def __init__(self, id_registro, duenio_id, servicio_id, nombre_mascota="", especie="", observaciones="", costo_final=0.0, fecha=""):
        super().__init__(id_registro)
        self.duenio_id = int(duenio_id)
        self.servicio_id = int(servicio_id)
        self.nombre_mascota = nombre_mascota
        self.especie = especie
        self.observaciones = observaciones
        self.costo_final = float(costo_final) if costo_final != "" else 0.0
        self.fecha = fecha or date.today().isoformat()

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["duenio_id"] = self.duenio_id
        datos["servicio_id"] = self.servicio_id
        datos["nombre_mascota"] = self.nombre_mascota
        datos["especie"] = self.especie
        datos["observaciones"] = self.observaciones
        datos["costo_final"] = self.costo_final
        datos["fecha"] = self.fecha
        return datos

    def etiqueta(self):
        return (f"Atención #{self.id} · Mascota: {self.nombre_mascota} ({self.especie}) · "
                f"Dueño ID: {self.duenio_id} · Total: ${self.costo_final:.2f} [{self.fecha}]")