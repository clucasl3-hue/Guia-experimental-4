from abc import ABC, abstractmethod
import os

from models import ClienteCine, Pelicula, Boleto
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


class ClienteCineController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "clientes_cine.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [ClienteCine.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([c.a_diccionario() for c in self.lista])

    def tarjetas_registradas(self, excepto_id=None):
        """CONJUNTO para verificar tarjetas de fidelidad únicas de forma inmediata."""
        return {c.tarjeta_fidelidad.strip().upper() for c in self.lista if c.id != excepto_id and c.tarjeta_fidelidad}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "apellido", "email"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"

        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            if not es_email_valido(email): return f"Email inválido: '{email}'"
            if email in {c.email for c in self.lista if c.id != id_actual}:
                return "Ese email ya está registrado"

        tarjeta = str(datos.get("tarjeta_fidelidad", "")).strip().upper()
        if tarjeta and tarjeta in self.tarjetas_registradas(id_actual):
            return f"La tarjeta de fidelidad '{tarjeta}' ya está registrada"
        return None

    def leer(self): return self.lista

    def obtener(self, id_cliente):
        for c in self.lista:
            if c.id == id_cliente: return c
        return None

    def buscar(self, t):
        t = t.strip().lower()
        if not t: return []
        return [c for c in self.lista if t in c.nombre.lower() or t in c.apellido.lower() or t in c.tarjeta_fidelidad.lower()]

    def siguiente(self):
        return max([c.id for c in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        cliente = ClienteCine(
            self.siguiente(), str(datos["nombre"]).strip().title(),
            str(datos["apellido"]).strip().title(), str(datos["email"]).strip().lower(),
            str(datos.get("tarjeta_fidelidad", "")).strip().upper()
        )
        self.lista.append(cliente)
        self.guardar()
        return True, f"Cliente creado: {cliente.etiqueta()}"

    def actualizar(self, id_cliente, datos):
        cliente = self.obtener(id_cliente)
        if not cliente: return False, "No existe el cliente"
        error = self.validar(datos, id_cliente)
        if error: return False, error
        for k, v in datos.items():
            val = str(v).strip()
            if k in ("nombre", "apellido"): val = val.title()
            elif k == "email": val = val.lower()
            elif k == "tarjeta_fidelidad": val = val.upper()
            setattr(cliente, k, val)
        self.guardar()
        return True, f"Cliente {id_cliente} actualizado"

    def eliminar(self, id_cliente):
        cliente = self.obtener(id_cliente)
        if not cliente: return False, "No existe"
        self.lista.remove(cliente)
        self.guardar()
        return True, f"Cliente {id_cliente} eliminado"


class PeliculaController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "peliculas.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Pelicula.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([p.a_diccionario() for p in self.lista])

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("titulo", "genero", "duracion_min"):
                if str(datos.get(campo, "")).strip() == "": return f"El campo {campo} es obligatorio"
        if "duracion_min" in datos and str(datos["duracion_min"]).strip() != "":
            if not Pelicula.es_duracion_valida(datos["duracion_min"]):
                return "La duración en minutos debe ser mayor a 0"
        return None

    def leer(self): return self.lista
    def obtener(self, id_pelicula):
        for p in self.lista:
            if p.id == id_pelicula: return p
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [p for p in self.lista if t in p.titulo.lower() or t in p.genero.lower()]

    def siguiente(self):
        return max([p.id for p in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        pelicula = Pelicula(
            self.siguiente(), str(datos["titulo"]).strip().title(),
            str(datos["genero"]).strip().title(), int(datos["duracion_min"]),
            int(datos["asientos_disponibles"]) if str(datos.get("asientos_disponibles", "")).strip() != "" else 50
        )
        self.lista.append(pelicula)
        self.guardar()
        return True, f"Película registrada: {pelicula.etiqueta()}"

    def actualizar(self, id_pelicula, datos):
        pelicula = self.obtener(id_pelicula)
        if not pelicula: return False, "No existe"
        error = self.validar(datos, id_pelicula)
        if error: return False, error
        if "titulo" in datos: pelicula.titulo = str(datos["titulo"]).strip().title()
        if "genero" in datos: pelicula.genero = str(datos["genero"]).strip().title()
        if "duracion_min" in datos and str(datos["duracion_min"]).strip() != "":
            pelicula.duracion_min = int(datos["duracion_min"])
        if "asientos_disponibles" in datos and str(datos["asientos_disponibles"]).strip() != "":
            pelicula.asientos_disponibles = int(datos["asientos_disponibles"])
        self.guardar()
        return True, f"Película {id_pelicula} actualizada"

    def eliminar(self, id_pelicula):
        pelicula = self.obtener(id_pelicula)
        if not pelicula: return False, "No existe"
        self.lista.remove(pelicula)
        self.guardar()
        return True, "Película eliminada"

    def peliculas_con_espacio(self):
        return [p for p in self.lista if p.hay_asientos()]


class BoletoController(CrudBase):
    def __init__(self, clientes, peliculas, archivo=None):
        self.clientes = clientes
        self.peliculas = peliculas
        ruta = archivo or os.path.join(DATA_DIR, "boletos.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Boleto.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([b.a_diccionario() for b in self.lista])

    def validar(self, datos):
        try:
            cli_id = int(datos.get("cliente_id", 0))
            pel_id = int(datos.get("pelicula_id", 0))
            cant = int(datos.get("cantidad_boletos", 0))
        except (TypeError, ValueError):
            return "Datos numéricos inválidos"
        if not self.clientes.obtener(cli_id): return "No existe el cliente"
        pelicula = self.peliculas.obtener(pel_id)
        if not pelicula: return "No existe la película"
        if cant <= 0: return "La cantidad de boletos debe ser mayor a 0"
        if not pelicula.hay_asientos(cant):
            return f"No hay suficientes asientos disponibles (Quedan {pelicula.asientos_disponibles})"
        return None

    def leer(self): return self.lista
    def obtener(self, id_boleto):
        for b in self.lista:
            if b.id == id_boleto: return b
        return None

    def buscar(self, t):
        return [b for b in self.lista if t.strip() in b.sala]

    def siguiente(self):
        return max([b.id for b in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        pelicula = self.peliculas.obtener(int(datos["pelicula_id"]))
        cant = int(datos["cantidad_boletos"])
        sala = str(datos.get("sala", "Sala 1")).strip().title()

        total = round(cant * Pelicula.PRECIO_GENERAL, 2)

        boleto = Boleto(
            self.siguiente(), int(datos["cliente_id"]), pelicula.id,
            cant, sala, total
        )
        pelicula.ocupar_asientos(cant)
        self.peliculas.guardar()
        self.lista.append(boleto)
        self.guardar()
        return True, f"Boleto #{boleto.id} emitido con éxito. Total a pagar: ${total:.2f}"

    def actualizar(self, id_boleto, datos): return False, "Los boletos no se modifican"

    def eliminar(self, id_boleto):
        boleto = self.obtener(id_boleto)
        if not boleto: return False, "No existe"
        pelicula = self.peliculas.obtener(boleto.pelicula_id)
        if pelicula:
            pelicula.liberar_asientos(boleto.cantidad_boletos)
            self.peliculas.guardar()
        self.lista.remove(boleto)
        self.guardar()
        return True, "Boleto cancelado y asientos devueltos"

    def comprobante_boleto(self, id_boleto):
        boleto = self.obtener(id_boleto)
        if not boleto: return None
        cli = self.clientes.obtener(boleto.cliente_id)
        pel = self.peliculas.obtener(boleto.pelicula_id)
        texto = f"COMPROBANTE DE CINE - BOLETO #{boleto.id}\n"
        texto += f"Cliente : {cli.nombre_completo() if cli else 'N/A'}   (Tarjeta: {cli.tarjeta_fidelidad if cli else 'N/A'})\n"
        texto += f"Película: '{pel.titulo if pel else 'N/A'}' ({pel.genero if pel else 'N/A'})\n"
        texto += f"Sala    : {boleto.sala}   ·   Boletos: {boleto.cantidad_boletos}\n"
        texto += "-" * 42 + f"\nTOTAL PAGADO: ${boleto.total_pagado:.2f}"
        return texto

    def total_recaudado(self):
        return round(sum(b.total_pagado for b in self.lista), 2)