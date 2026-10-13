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


class Inquilino(Persona):
    """Inquilino ES UNA Persona, con teléfono y número de documento único."""

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


class Propiedad(ModeloBase):
    """Propiedad ES UN ModeloBase. Contiene atributos y métodos estáticos de depósito."""

    MESES_DEPOSITO_GARANTIA = 2  # Atributo estático (Se piden 2 meses por adelantado)
    TOTAL_PROPIEDADES = 0

    def __init__(self, id_registro, codigo_propiedad, tipo, direccion, precio_mes, disponible=True):
        super().__init__(id_registro)
        self.codigo_propiedad = str(codigo_propiedad).upper()
        self.tipo = str(tipo).title()  # Departamento, Casa, Local Comercial
        self.direccion = str(direccion).title()
        self.precio_mes = float(precio_mes) if precio_mes != "" else 300.0
        self.disponible = disponible if isinstance(disponible, bool) else (str(disponible).lower() == 'true')
        Propiedad.TOTAL_PROPIEDADES += 1

    @staticmethod
    def calcular_pago_inicial(precio_mes, meses_contrato):
        try:
            meses = int(meses_contrato)
            precio = float(precio_mes)
            # Pago inicial = (Meses de contrato + meses de depósito de garantía) * precio mensual
            total_meses = meses + Propiedad.MESES_DEPOSITO_GARANTIA
            return round(precio * total_meses, 2)
        except (TypeError, ValueError):
            return 0.0

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["codigo_propiedad"] = self.codigo_propiedad
        datos["tipo"] = self.tipo
        datos["direccion"] = self.direccion
        datos["precio_mes"] = self.precio_mes
        datos["disponible"] = self.disponible
        return datos

    def etiqueta(self):
        estado = "Disponible" if self.disponible else "Alquilada"
        return f"[{self.codigo_propiedad}] {self.tipo} en {self.direccion} · ${self.precio_mes:.2f}/mes · [{estado}]"


class ContratoAlquiler(ModeloBase):
    """Contrato: une un inquilino y una propiedad con meses de contrato y total inicial."""

    def __init__(self, id_registro, inquilino_id, propiedad_id, meses_contrato=12, total_inicial=0.0, fecha_inicio=""):
        super().__init__(id_registro)
        self.inquilino_id = int(inquilino_id)
        self.propiedad_id = int(propiedad_id)
        self.meses_contrato = int(meses_contrato) if meses_contrato != "" else 12
        self.total_inicial = float(total_inicial) if total_inicial != "" else 0.0
        self.fecha_inicio = fecha_inicio or date.today().isoformat()

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["inquilino_id"] = self.inquilino_id
        datos["propiedad_id"] = self.propiedad_id
        datos["meses_contrato"] = self.meses_contrato
        datos["total_inicial"] = self.total_inicial
        datos["fecha_inicio"] = self.fecha_inicio
        return datos

    def etiqueta(self):
        return f"Contrato #{self.id} · Inquilino ID: {self.inquilino_id} · Propiedad ID: {self.propiedad_id} · Total Inicial: ${self.total_inicial:.2f}"