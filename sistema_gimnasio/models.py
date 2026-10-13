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


class Socio(Persona):
    """Socio ES UNA Persona, con número de socio y objetivo fitness."""

    def __init__(self, id_registro, nombre, apellido, email, nro_socio="", objetivo=""):
        super().__init__(id_registro, nombre, apellido, email)
        self.nro_socio = nro_socio
        self.objetivo = objetivo

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["nro_socio"] = self.nro_socio
        datos["objetivo"] = self.objetivo
        return datos

    def etiqueta(self):
        return f"{super().etiqueta()} · Socio #{self.nro_socio} · Objetivo: {self.objetivo or 'General'}"


class ClaseGrupal(ModeloBase):
    """ClaseGrupal ES UN ModeloBase. Contiene atributos y métodos estáticos de control."""

    LIMITE_TOTAL_CLASES = 20   # Atributo estático
    CUPOS_DEFAULT = 15

    def __init__(self, id_registro, nombre_clase, horario, instructor, cupos_maximos=15):
        super().__init__(id_registro)
        self.nombre_clase = nombre_clase
        self.horario = horario
        self.instructor = instructor
        self.cupos_maximos = int(cupos_maximos) if cupos_maximos != "" else ClaseGrupal.CUPOS_DEFAULT

    @staticmethod
    def es_horario_valido(horario):
        # Validación básica de formato de hora o texto de horario
        return len(str(horario).strip()) >= 3

    def hay_cupo(self):
        return self.cupos_maximos > 0

    def ocupar_cupo(self):
        if self.cupos_maximos > 0:
            self.cupos_maximos -= 1

    def liberar_cupo(self):
        self.cupos_maximos += 1

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["nombre_clase"] = self.nombre_clase
        datos["horario"] = self.horario
        datos["instructor"] = self.instructor
        datos["cupos_maximos"] = self.cupos_maximos
        return datos

    def etiqueta(self):
        alerta = " ⚠ sin cupos" if not self.hay_cupo() else ""
        return f"{self.nombre_clase} ({self.horario}) · Instr: {self.instructor} · Cupos: {self.cupos_maximos}{alerta}"


class InscripcionClase(ModeloBase):
    """Inscripción: une un socio y una clase grupal con fecha."""

    def __init__(self, id_registro, socio_id, clase_id, fecha_inscripcion=""):
        super().__init__(id_registro)
        self.socio_id = int(socio_id)
        self.clase_id = int(clase_id)
        self.fecha_inscripcion = fecha_inscripcion or date.today().isoformat()

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["socio_id"] = self.socio_id
        datos["clase_id"] = self.clase_id
        datos["fecha_inscripcion"] = self.fecha_inscripcion
        return datos

    def etiqueta(self):
        return f"Inscripción #{self.id} · Socio ID: {self.socio_id} · Clase ID: {self.clase_id} ({self.fecha_inscripcion})"