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


class Conductor(Persona):
    """Conductor ES UNA Persona, con número de licencia y tipo de sangre."""

    def __init__(self, id_registro, nombre, apellido, email, licencia="", tipo_sangre=""):
        super().__init__(id_registro, nombre, apellido, email)
        self.licencia = str(licencia).upper()
        self.tipo_sangre = str(tipo_sangre).upper()

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["licencia"] = self.licencia
        datos["tipo_sangre"] = self.tipo_sangre
        return datos

    def etiqueta(self):
        return f"{super().etiqueta()} · Licencia: {self.licencia} · Sangre: {self.tipo_sangre or 'N/D'}"


class TipoTramite(ModeloBase):
    """TipoTramite ES UN ModeloBase. Contiene atributos y métodos estáticos de multas."""

    COSTO_MULTA_ATRASO = 15.0  # Atributo estático
    TOTAL_TRAMITES = 0

    def __init__(self, id_registro, nombre_tramite, codigo, costo_base):
        super().__init__(id_registro)
        self.nombre_tramite = nombre_tramite
        self.codigo = str(codigo).upper()
        self.costo_base = float(costo_base) if costo_base != "" else 30.0
        TipoTramite.TOTAL_TRAMITES += 1

    @staticmethod
    def calcular_total_con_multa(costo_base, dias_atraso=0):
        try:
            base = float(costo_base)
            multa = int(dias_atraso) * TipoTramite.COSTO_MULTA_ATRASO
            return round(base + multa, 2)
        except (TypeError, ValueError):
            return 0.0

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["nombre_tramite"] = self.nombre_tramite
        datos["codigo"] = self.codigo
        datos["costo_base"] = self.costo_base
        return datos

    def etiqueta(self):
        return f"{self.nombre_tramite} ({self.codigo}) · Base: ${self.costo_base:.2f}"


class TurnoLicencia(ModeloBase):
    """Turno: une un conductor y un trámite con fecha asignada y total calculado."""

    def __init__(self, id_registro, conductor_id, tramite_id, fecha_asignada="", dias_atraso=0, total_pagado=0.0, estado_pago="Pendiente"):
        super().__init__(id_registro)
        self.conductor_id = int(conductor_id)
        self.tramite_id = int(tramite_id)
        self.fecha_asignada = fecha_asignada or date.today().isoformat()
        self.dias_atraso = int(dias_atraso) if dias_atraso != "" else 0
        self.total_pagado = float(total_pagado) if total_pagado != "" else 0.0
        self.estado_pago = estado_pago

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["conductor_id"] = self.conductor_id
        datos["tramite_id"] = self.tramite_id
        datos["fecha_asignada"] = self.fecha_asignada
        datos["dias_atraso"] = self.dias_atraso
        datos["total_pagado"] = self.total_pagado
        datos["estado_pago"] = self.estado_pago
        return datos

    def etiqueta(self):
        return f"Turno #{self.id} [{self.estado_pago}] · Conductor ID: {self.conductor_id} · Trámite ID: {self.tramite_id} · Total: ${self.total_pagado:.2f}"