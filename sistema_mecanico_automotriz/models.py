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


class PropietarioAuto(Persona):
    """PropietarioAuto ES UNA Persona, con cédula y teléfono únicos."""

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


class ServicioTaller(ModeloBase):
    """ServicioTaller ES UN ModeloBase. Contiene atributos y métodos estáticos de mano de obra."""

    MANO_OBRA_BASE = 35.0  # Atributo estático
    TOTAL_SERVICIOS = 0

    def __init__(self, id_registro, nombre_servicio, codigo, costo_repuestos):
        super().__init__(id_registro)
        self.nombre_servicio = str(nombre_servicio).title()
        self.codigo = str(codigo).upper()
        self.costo_repuestos = float(costo_repuestos) if costo_repuestos != "" else 20.0
        ServicioTaller.TOTAL_SERVICIOS += 1

    @staticmethod
    def calcular_costo_reparacion(repuestos, urgencia_extra=0.0):
        try:
            return round(float(repuestos) + float(ServicioTaller.MANO_OBRA_BASE) + float(urgencia_extra), 2)
        except (TypeError, ValueError):
            return 0.0

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["nombre_servicio"] = self.nombre_servicio
        datos["codigo"] = self.codigo
        datos["costo_repuestos"] = self.costo_repuestos
        return datos

    def etiqueta(self):
        return f"{self.nombre_servicio} ({self.codigo}) · Repuestos: ${self.costo_repuestos:.2f}"


class OrdenReparacion(ModeloBase):
    """OrdenReparacion: une un propietario y un servicio con placa del vehículo y costo total."""

    def __init__(self, id_registro, propietario_id, servicio_id, placa_vehiculo="", costo_total=0.0, fecha=""):
        super().__init__(id_registro)
        self.propietario_id = int(propietario_id)
        self.servicio_id = int(servicio_id)
        self.placa_vehiculo = str(placa_vehiculo).upper()
        self.costo_total = float(costo_total) if costo_total != "" else 0.0
        self.fecha = fecha or date.today().isoformat()

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["propietario_id"] = self.propietario_id
        datos["servicio_id"] = self.servicio_id
        datos["placa_vehiculo"] = self.placa_vehiculo
        datos["costo_total"] = self.costo_total
        datos["fecha"] = self.fecha
        return datos

    def etiqueta(self):
        return f"Orden #{self.id} · Auto Placa: {self.placa_vehiculo} · Prop. ID: {self.propietario_id} · Total: ${self.costo_total:.2f}"