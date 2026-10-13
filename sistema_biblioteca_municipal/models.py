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


class Lector(Persona):
    """Lector ES UNA Persona, con código de lector y teléfono."""

    def __init__(self, id_registro, nombre, apellido, email, codigo_lector="", telefono=""):
        super().__init__(id_registro, nombre, apellido, email)
        self.codigo_lector = codigo_lector
        self.telefono = telefono

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["codigo_lector"] = self.codigo_lector
        datos["telefono"] = self.telefono
        return datos

    def etiqueta(self):
        return f"{super().etiqueta()} · Código: {self.codigo_lector} · Tel: {self.telefono or 'N/D'}"


class Libro(ModeloBase):
    """Libro ES UN ModeloBase. Contiene atributos y métodos estáticos."""

    MAX_DIAS_PRESTAMO = 7      # Atributo estático: política de la biblioteca
    TOTAL_LIBROS_REGISTRADOS = 0

    def __init__(self, id_registro, titulo, isbn, autor, ejemplares_disponibles=1):
        super().__init__(id_registro)
        self.titulo = titulo
        self.isbn = str(isbn).upper()
        self.autor = autor
        self.ejemplares_disponibles = int(ejemplares_disponibles) if ejemplares_disponibles != "" else 1
        Libro.TOTAL_LIBROS_REGISTRADOS += 1

    @staticmethod
    def es_isbn_valido(isbn):
        # Validación básica de longitud o existencia de ISBN
        return len(str(isbn).strip()) >= 5

    def hay_ejemplares(self):
        return self.ejemplares_disponibles > 0

    def prestar_ejemplar(self):
        if self.ejemplares_disponibles > 0:
            self.ejemplares_disponibles -= 1

    def devolver_ejemplar(self):
        self.ejemplares_disponibles += 1

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["titulo"] = self.titulo
        datos["isbn"] = self.isbn
        datos["autor"] = self.autor
        datos["ejemplares_disponibles"] = self.ejemplares_disponibles
        return datos

    def etiqueta(self):
        alerta = " ⚠ sin ejemplares" if not self.hay_ejemplares() else ""
        return f"'{self.titulo}' ({self.autor}) · ISBN: {self.isbn} · Disponibles: {self.ejemplares_disponibles}{alerta}"


class Prestamo(ModeloBase):
    """Préstamo: une un lector y un libro con fechas y estado."""

    def __init__(self, id_registro, lector_id, libro_id, fecha_prestamo="", fecha_devolucion="", estado="Activo"):
        super().__init__(id_registro)
        self.lector_id = int(lector_id)
        self.libro_id = int(libro_id)
        self.fecha_prestamo = fecha_prestamo or date.today().isoformat()
        self.fecha_devolucion = fecha_devolucion or "Pendiente"
        self.estado = estado  # "Activo" o "Devuelto"

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["lector_id"] = self.lector_id
        datos["libro_id"] = self.libro_id
        datos["fecha_prestamo"] = self.fecha_prestamo
        datos["fecha_devolucion"] = self.fecha_devolucion
        datos["estado"] = self.estado
        return datos

    def etiqueta(self):
        return (f"Préstamo #{self.id} [{self.estado}] · Lector ID: {self.lector_id} · "
                f"Libro ID: {self.libro_id} (Fecha: {self.fecha_prestamo})")