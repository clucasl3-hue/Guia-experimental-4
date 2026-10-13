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


class EstudianteIdioma(Persona):
    """EstudianteIdioma ES UNA Persona, con teléfono y número de pasaporte o documento único."""

    def __init__(self, id_registro, nombre, apellido, email, documento="", telefono=""):
        super().__init__(id_registro, nombre, apellido, email)
        self.documento = str(documento).strip()
        self.telefono = str(telefono).strip()

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["documento"] = self.documento
        datos["telefono"] = self.telefono
        return datos

    def etiqueta(self):
        return f"{super().etiqueta()} · Doc: {self.documento} · Tel: {self.telefono or 'N/D'}"


class CursoIdioma(ModeloBase):
    """CursoIdioma ES UN ModeloBase. Contiene atributos y métodos estáticos de descuento por pronto pago."""

    DESCUENTO_PRONTO_PAGO = 0.10  # Atributo estático (10% de descuento)
    TOTAL_CURSOS = 0

    def __init__(self, id_registro, nombre_idioma, nivel, costo_curso):
        super().__init__(id_registro)
        self.nombre_idioma = str(nombre_idioma).title()  # Inglés, Francés, Alemán, etc.
        self.nivel = str(nivel).upper()  # A1, A2, B1, B2, C1, C2
        self.costo_curso = float(costo_curso) if costo_curso != "" else 120.0
        CursoIdioma.TOTAL_CURSOS += 1

    @staticmethod
    def calcular_costo_matricula(costo_base, pronto_pago=False):
        try:
            base = float(costo_base)
            if pronto_pago:
                return round(base * (1 - CursoIdioma.DESCUENTO_PRONTO_PAGO), 2)
            return round(base, 2)
        except (TypeError, ValueError):
            return 0.0

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["nombre_idioma"] = self.nombre_idioma
        datos["nivel"] = self.nivel
        datos["costo_curso"] = self.costo_curso
        return datos

    def etiqueta(self):
        return f"{self.nombre_idioma} - Nivel {self.nivel} · Costo Base: ${self.costo_curso:.2f}"


class MatriculaCurso(ModeloBase):
    """MatriculaCurso: une un estudiante y un curso con el monto final y fecha."""

    def __init__(self, id_registro, estudiante_id, curso_id, costo_total=0.0, fecha_matricula=""):
        super().__init__(id_registro)
        self.estudiante_id = int(estudiante_id)
        self.curso_id = int(curso_id)
        self.costo_total = float(costo_total) if costo_total != "" else 0.0
        self.fecha_matricula = fecha_matricula or date.today().isoformat()

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["estudiante_id"] = self.estudiante_id
        datos["curso_id"] = self.curso_id
        datos["costo_total"] = self.costo_total
        datos["fecha_matricula"] = self.fecha_matricula
        return datos

    def etiqueta(self):
        return f"Matrícula #{self.id} · Estudiante ID: {self.estudiante_id} · Curso ID: {self.curso_id} · Total: ${self.costo_total:.2f}"