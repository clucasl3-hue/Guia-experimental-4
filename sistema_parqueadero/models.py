from datetime import datetime


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


class ConductorParque(Persona):
    """Conductor ES UNA Persona, con teléfono y número de placa único de su vehículo."""

    def __init__(self, id_registro, nombre, apellido, email, placa="", telefono=""):
        super().__init__(id_registro, nombre, apellido, email)
        self.placa = str(placa).strip().upper()
        self.telefono = str(telefono).strip()

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["placa"] = self.placa
        datos["telefono"] = self.telefono
        return datos

    def etiqueta(self):
        return f"{super().etiqueta()} · Placa Vehículo: {self.placa} · Tel: {self.telefono or 'N/D'}"


class EspacioParqueo(ModeloBase):
    """EspacioParqueo ES UN ModeloBase. Contiene atributos y métodos estáticos de tarifa por hora."""

    TARIFA_HORA = 1.50  # Atributo estático ($ por hora)
    TOTAL_ESPACIOS = 0

    def __init__(self, id_registro, numero_espacio, tipo_vehiculo="Automovil", disponible=True):
        super().__init__(id_registro)
        self.numero_espacio = str(numero_espacio).strip().upper()
        self.tipo_vehiculo = str(tipo_vehiculo).title()  # Automovil, Moto, SUV
        self.disponible = disponible if isinstance(disponible, bool) else (str(disponible).lower() == 'true')
        EspacioParqueo.TOTAL_ESPACIOS += 1

    @staticmethod
    def calcular_costo_estadia(horas):
        try:
            h = float(horas)
            return round(h * EspacioParqueo.TARIFA_HORA, 2)
        except (TypeError, ValueError):
            return 0.0

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["numero_espacio"] = self.numero_espacio
        datos["tipo_vehiculo"] = self.tipo_vehiculo
        datos["disponible"] = self.disponible
        return datos

    def etiqueta(self):
        estado = "Disponible" if self.disponible else "Ocupado"
        return f"Espacio #{self.numero_espacio} [{self.tipo_vehiculo}] · Tarifa/h: ${EspacioParqueo.TARIFA_HORA:.2f} · [{estado}]"


class TicketEstacionamiento(ModeloBase):
    """Ticket: une un conductor y un espacio con horas de estadía y costo total."""

    def __init__(self, id_registro, conductor_id, espacio_id, horas_estadia=1, total_pagar=0.0, fecha_ingreso=""):
        super().__init__(id_registro)
        self.conductor_id = int(conductor_id)
        self.espacio_id = int(espacio_id)
        self.horas_estadia = float(horas_estadia) if horas_estadia != "" else 1.0
        self.total_pagar = float(total_pagar) if total_pagar != "" else 0.0
        self.fecha_ingreso = fecha_ingreso or datetime.now().strftime("%Y-%m-%d %H:%M")

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["conductor_id"] = self.conductor_id
        datos["espacio_id"] = self.espacio_id
        datos["horas_estadia"] = self.horas_estadia
        datos["total_pagar"] = self.total_pagar
        datos["fecha_ingreso"] = self.fecha_ingreso
        return datos

    def etiqueta(self):
        return f"Ticket #{self.id} · Conductor ID: {self.conductor_id} · Espacio ID: {self.espacio_id} · {self.horas_estadia}h · Total: ${self.total_pagar:.2f}"