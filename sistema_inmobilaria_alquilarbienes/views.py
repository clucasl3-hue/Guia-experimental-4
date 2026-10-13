from abc import ABC, abstractmethod
import os

from models import Inquilino, Propiedad, ContratoAlquiler
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


class CrudBase(ABC):
    @abstractmethod
    def leer(self): pass
    @abstractmethod
    def obtener(self, id_registro): pass
    @abstractmethod
    def buscar(self, texto): pass
    @abstractmethod
    def siguiente(self): pass
    @abstractmethod
    def crear(self, datos): pass
    @abstractmethod
    def actualizar(self, id_registro, datos): pass
    @abstractmethod
    def eliminar(self, id_registro): pass


class InquilinoController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "inquilinos.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Inquilino.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([i.a_diccionario() for i in self.lista])

    def documentos_registrados(self, excepto_id=None):
        return {i.documento.strip() for i in self.lista if i.id != excepto_id and i.documento}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "apellido", "email", "documento"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"
        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            if not es_email_valido(email): return f"Email inválido: '{email}'"
            if email in {i.email for i in self.lista if i.id != id_actual}:
                return "Ese email ya está registrado"
        if "documento" in datos:
            doc = str(datos["documento"]).strip()
            if doc in self.documentos_registrados(id_actual):
                return f"El documento '{doc}' ya está registrado"
        return None

    def leer(self): return self.lista
    def obtener(self, id_i):
        for i in self.lista:
            if i.id == id_i: return i
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [i for i in self.lista if t in i.nombre.lower() or t in i.apellido.lower() or t in i.documento.lower()]

    def siguiente(self):
        return max([i.id for i in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        inquilino = Inquilino(
            self.siguiente(), str(datos["nombre"]).strip().title(),
            str(datos["apellido"]).strip().title(), str(datos["email"]).strip().lower(),
            str(datos["documento"]).strip(), str(datos.get("telefono", "")).strip()
        )
        self.lista.append(inquilino)
        self.guardar()
        return True, f"Inquilino registrado: {inquilino.etiqueta()}"

    def actualizar(self, id_i, datos):
        i = self.obtener(id_i)
        if not i: return False, "No existe"
        error = self.validar(datos, id_i)
        if error: return False, error
        for k, v in datos.items():
            val = str(v).strip()
            if k in ("nombre", "apellido"): val = val.title()
            elif k == "email": val = val.lower()
            setattr(i, k, val)
        self.guardar()
        return True, f"Inquilino {id_i} actualizado"

    def eliminar(self, id_i):
        i = self.obtener(id_i)
        if not i: return False, "No existe"
        self.lista.remove(i)
        self.guardar()
        return True, "Inquilino eliminado"


class PropiedadController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "propiedades.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Propiedad.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([p.a_diccionario() for p in self.lista])

    def codigos_registrados(self, excepto_id=None):
        return {p.codigo_propiedad.strip().upper() for p in self.lista if p.id != excepto_id and p.codigo_propiedad}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("codigo_propiedad", "tipo", "direccion", "precio_mes"):
                if str(datos.get(campo, "")).strip() == "": return f"El campo {campo} es obligatorio"
        if "codigo_propiedad" in datos:
            cod = str(datos["codigo_propiedad"]).strip().upper()
            if cod in self.codigos_registrados(id_actual): return f"El código '{cod}' ya existe"
        return None

    def leer(self): return self.lista
    def obtener(self, id_p):
        for p in self.lista:
            if p.id == id_p: return p
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [p for p in self.lista if t in p.codigo_propiedad.lower() or t in p.tipo.lower() or t in p.direccion.lower()]

    def siguiente(self):
        return max([p.id for p in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        propiedad = Propiedad(
            self.siguiente(), str(datos["codigo_propiedad"]).strip().upper(),
            str(datos["tipo"]).strip().title(), str(datos["direccion"]).strip().title(),
            float(datos["precio_mes"]), True
        )
        self.lista.append(propiedad)
        self.guardar()
        return True, f"Propiedad registrada: {propiedad.etiqueta()}"

    def actualizar(self, id_p, datos):
        p = self.obtener(id_p)
        if not p: return False, "No existe"
        error = self.validar(datos, id_p)
        if error: return False, error
        if "codigo_propiedad" in datos: p.codigo_propiedad = str(datos["codigo_propiedad"]).strip().upper()
        if "tipo" in datos: p.tipo = str(datos["tipo"]).strip().title()
        if "direccion" in datos: p.direccion = str(datos["direccion"]).strip().title()
        if "precio_mes" in datos and str(datos["precio_mes"]).strip() != "": p.precio_mes = float(datos["precio_mes"])
        self.guardar()
        return True, "Propiedad actualizada"

    def eliminar(self, id_p):
        p = self.obtener(id_p)
        if not p: return False, "No existe"
        self.lista.remove(p)
        self.guardar()
        return True, "Propiedad eliminada"

    def propiedades_disponibles(self):
        return [p for p in self.lista if p.disponible]


class ContratoAlquilerController(CrudBase):
    def __init__(self, inquilinos, propiedades, archivo=None):
        self.inquilinos = inquilinos
        self.propiedades = propiedades
        ruta = archivo or os.path.join(DATA_DIR, "contratos.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [ContratoAlquiler.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([c.a_diccionario() for c in self.lista])

    def validar(self, datos):
        try:
            inq_id = int(datos.get("inquilino_id", 0))
            prop_id = int(datos.get("propiedad_id", 0))
            meses = int(datos.get("meses_contrato", 0))
        except (TypeError, ValueError):
            return "IDs o meses inválidos"
        if not self.inquilinos.obtener(inq_id): return "No existe el inquilino"
        propiedad = self.propiedades.obtener(prop_id)
        if not propiedad: return "No existe la propiedad"
        if not propiedad.disponible: return f"La propiedad {propiedad.codigo_propiedad} ya está alquilada"
        if meses <= 0: return "Los meses de contrato deben ser mayores a 0"
        return None

    def leer(self): return self.lista
    def obtener(self, id_c):
        for c in self.lista:
            if c.id == id_c: return c
        return None

    def buscar(self, t):
        return [c for c in self.lista if t.strip() in c.fecha_inicio]

    def siguiente(self):
        return max([c.id for c in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        propiedad = self.propiedades.obtener(int(datos["propiedad_id"]))
        meses = int(datos["meses_contrato"])

        total_inicial = Propiedad.calcular_pago_inicial(propiedad.precio_mes, meses)

        contrato = ContratoAlquiler(
            self.siguiente(), int(datos["inquilino_id"]), propiedad.id,
            meses, total_inicial, str(datos.get("fecha_inicio", "")).strip()
        )
        propiedad.disponible = False  # Ocupar propiedad
        self.propiedades.guardar()
        self.lista.append(contrato)
        self.guardar()
        return True, f"Contrato #{contrato.id} generado con éxito. Total inicial (incl. {Propiedad.MESES_DEPOSITO_GARANTIA} meses de garantía): ${total_inicial:.2f}"

    def actualizar(self, id_c, datos): return False, "Los contratos no se modifican"

    def eliminar(self, id_c):
        c = self.obtener(id_c)
        if not c: return False, "No existe"
        propiedad = self.propiedades.obtener(c.propiedad_id)
        if propiedad:
            propiedad.disponible = True  # Liberar propiedad
            self.propiedades.guardar()
        self.lista.remove(c)
        self.guardar()
        return True, "Contrato cancelado y propiedad liberada"

    def comprobante_contrato(self, id_c):
        c = self.obtener(id_c)
        if not c: return None
        i = self.inquilinos.obtener(c.inquilino_id)
        p = self.propiedades.obtener(c.propiedad_id)
        texto = f"CONTRATO DE ALQUILER #{c.id}   Fecha Inicio: {c.fecha_inicio}\n"
        texto += f"Inquilino: {i.nombre_completo() if i else 'N/A'}   (Doc: {i.documento if i else 'N/A'})\n"
        texto += f"Propiedad: [{p.codigo_propiedad if p else 'N/A'}] {p.tipo if p else 'N/A'} - {p.direccion if p else 'N/A'}\n"
        texto += f"Meses contrato: {c.meses_contrato}   ·   Depósito garantía: {Propiedad.MESES_DEPOSITO_GARANTIA} meses\n"
        texto += "-" * 50 + f"\nTOTAL INICIAL PAGADO: ${c.total_inicial:.2f}"
        return texto

    def total_recaudado(self):
        return round(sum(c.total_inicial for c in self.lista), 2)