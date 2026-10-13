from datetime import date

class ModeloBase:
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


class PacienteDental(Persona):
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


class TratamientoDental(ModeloBase):
    DESCUENTO_SEGURO = 0.20  # Atributo estático (20% desc.)
    TOTAL_TRATAMIENTOS = 0

    def __init__(self, id_registro, nombre_tratamiento, codigo, costo_base):
        super().__init__(id_registro)
        self.nombre_tratamiento = str(nombre_tratamiento).title()
        self.codigo = str(codigo).upper()
        self.costo_base = float(costo_base) if costo_base != "" else 40.0
        TratamientoDental.TOTAL_TRATAMIENTOS += 1

    @staticmethod
    def calcular_costo_final(costo_base, con_seguro=False):
        try:
            base = float(costo_base)
            if con_seguro:
                return round(base * (1 - TratamientoDental.DESCUENTO_SEGURO), 2)
            return round(base, 2)
        except (TypeError, ValueError):
            return 0.0

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["nombre_tratamiento"] = self.nombre_tratamiento
        datos["codigo"] = self.codigo
        datos["costo_base"] = self.costo_base
        return datos

    def etiqueta(self):
        return f"{self.nombre_tratamiento} ({self.codigo}) · Base: ${self.costo_base:.2f}"


class CitaDental(ModeloBase):
    def __init__(self, id_registro, paciente_id, tratamiento_id, fecha_cita="", costo_final=0.0, estado="Confirmada"):
        super().__init__(id_registro)
        self.paciente_id = int(paciente_id)
        self.tratamiento_id = int(tratamiento_id)
        self.fecha_cita = fecha_cita or date.today().isoformat()
        self.costo_final = float(costo_final) if costo_final != "" else 0.0
        self.estado = estado

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["paciente_id"] = self.paciente_id
        datos["tratamiento_id"] = self.tratamiento_id
        datos["fecha_cita"] = self.fecha_cita
        datos["costo_final"] = self.costo_final
        datos["estado"] = self.estado
        return datos

    def etiqueta(self):
        return f"Cita #{self.id} [{self.estado}] · Paciente ID: {self.paciente_id} · Tratamiento ID: {self.tratamiento_id} · Total: ${self.costo_final:.2f}"