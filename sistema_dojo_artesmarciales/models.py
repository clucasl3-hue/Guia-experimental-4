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


class AtletaDojo(Persona):
    """AtletaDojo ES UNA Persona, con cinturón y número de socio único."""

    def __init__(self, id_registro, nombre, apellido, email, cinturon="Blanco", socio_id=""):
        super().__init__(id_registro, nombre, apellido, email)
        self.cinturon = str(cinturon).title()
        self.socio_id = str(socio_id).strip().upper()

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["cinturon"] = self.cinturon
        datos["socio_id"] = self.socio_id
        return datos

    def etiqueta(self):
        return f"{super().etiqueta()} · Cinturón: {self.cinturon} · Socio ID: {self.socio_id or 'N/D'}"


class ClaseMarcial(ModeloBase):
    """ClaseMarcial ES UN ModeloBase. Contiene atributos y métodos estáticos de descuento."""

    DESCUENTO_PROMOCION = 0.15  # Atributo estático (15% de descuento en matrícula)
    TOTAL_CLASES = 0

    def __init__(self, id_registro, nombre_clase, estilo, costo_mensual):
        super().__init__(id_registro)
        self.nombre_clase = str(nombre_clase).title()
        self.estilo = str(estilo).title()  # Karate, Judo, Taekwondo, BJJ
        self.costo_mensual = float(costo_mensual) if costo_mensual != "" else 50.0
        ClaseMarcial.TOTAL_CLASES += 1

    @staticmethod
    def calcular_costo_inscripcion(costo_base, con_promo=False):
        try:
            base = float(costo_base)
            if con_promo:
                return round(base * (1 - ClaseMarcial.DESCUENTO_PROMOCION), 2)
            return round(base, 2)
        except (TypeError, ValueError):
            return 0.0

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["nombre_clase"] = self.nombre_clase
        datos["estilo"] = self.estilo
        datos["costo_mensual"] = self.costo_mensual
        return datos

    def etiqueta(self):
        return f"{self.nombre_clase} [{self.estilo}] · Mensualidad: ${self.costo_mensual:.2f}"


class InscripcionDojo(ModeloBase):
    """InscripcionDojo: une un atleta y una clase con el monto final y fecha."""

    def __init__(self, id_registro, atleta_id, clase_id, total_pagar=0.0, fecha_inscripcion=""):
        super().__init__(id_registro)
        self.atleta_id = int(atleta_id)
        self.clase_id = int(clase_id)
        self.total_pagar = float(total_pagar) if total_pagar != "" else 0.0
        self.fecha_inscripcion = fecha_inscripcion or date.today().isoformat()

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["atleta_id"] = self.atleta_id
        datos["clase_id"] = self.clase_id
        datos["total_pagar"] = self.total_pagar
        datos["fecha_inscripcion"] = self.fecha_inscripcion
        return datos

    def etiqueta(self):
        return f"Inscripción #{self.id} · Atleta ID: {self.atleta_id} · Clase ID: {self.clase_id} · Total: ${self.total_pagar:.2f}"