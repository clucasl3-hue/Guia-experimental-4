from datetime import date


class ModeloBase:
    """Padre de todos los modelos. Guarda el id y define el comportamiento común."""

    def __init__(self, id_registro):
        self.id = int(id_registro)

    @classmethod
    def desde_diccionario(cls, datos):
        """Diccionario -> objeto. Escrito UNA vez y usado por los modelos."""
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


class Paciente(Persona):
    """Paciente ES UNA Persona, con cédula y tipo de sangre."""

    def __init__(self, id_registro, nombre, apellido, email, cedula="", tipo_sangre=""):
        super().__init__(id_registro, nombre, apellido, email)
        self.cedula = cedula
        self.tipo_sangre = tipo_sangre

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["cedula"] = self.cedula
        datos["tipo_sangre"] = self.tipo_sangre
        return datos

    def etiqueta(self):
        return f"{super().etiqueta()} · Cédula: {self.cedula} · Sangre: {self.tipo_sangre or 'N/D'}"


class Doctor(ModeloBase):
    """Doctor ES UN ModeloBase. Aquí van los atributos y métodos estáticos."""

    COSTO_BASE = 50.0          # Atributo estático (Costo estándar de consulta)
    TOTAL_DOCTORES = 0         # Contador compartido

    def __init__(self, id_registro, nombre_doctor, especialidad, consultorio, costo=50.0):
        super().__init__(id_registro)
        self.nombre_doctor = nombre_doctor
        self.especialidad = especialidad
        self.consultorio = consultorio
        self.costo = float(costo) if costo != "" else Doctor.COSTO_BASE
        Doctor.TOTAL_DOCTORES += 1

    @staticmethod
    def es_costo_valido(valor):
        try:
            return float(valor) > 0
        except (TypeError, ValueError):
            return False

    @staticmethod
    def calcular_con_descuento_tercera_edad(costo, es_tercera_edad=False):
        if es_tercera_edad:
            return round(costo * 0.5, 2)  # 50% de descuento
        return round(costo, 2)

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["nombre_doctor"] = self.nombre_doctor
        datos["especialidad"] = self.especialidad
        datos["consultorio"] = self.consultorio
        datos["costo"] = self.costo
        return datos

    def etiqueta(self):
        return f"Dr(a). {self.nombre_doctor} ({self.especialidad}) · Consultorio: {self.consultorio} · ${self.costo:.2f}"


class CitaMedica(ModeloBase):
    """Cita médica: un paciente, un doctor, fecha y síntomas."""

    def __init__(self, id_registro, paciente_id, doctor_id, fecha, sintomas="", valor_pagado=0.0):
        super().__init__(id_registro)
        self.paciente_id = int(paciente_id)
        self.doctor_id = int(doctor_id)
        self.fecha = fecha
        self.sintomas = sintomas
        self.valor_pagado = float(valor_pagado) if valor_pagado != "" else 0.0

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["paciente_id"] = self.paciente_id
        datos["doctor_id"] = self.doctor_id
        datos["fecha"] = self.fecha
        datos["sintomas"] = self.sintomas
        datos["valor_pagado"] = self.valor_pagado
        return datos

    def etiqueta(self):
        return (f"{self.fecha} · Paciente ID: {self.paciente_id} · "
                f"Doctor ID: {self.doctor_id} · Pagado: ${self.valor_pagado:.2f}")