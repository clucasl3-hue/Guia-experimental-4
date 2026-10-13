from abc import ABC, abstractmethod
import os

from models import Adoptante, MascotaRefugio, ProcesoAdopcion
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


class AdoptanteController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "adoptantes.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Adoptante.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([a.a_diccionario() for a in self.lista])

    def cedulas_registradas(self, excepto_id=None):
        return {a.cedula.strip() for a in self.lista if a.id != excepto_id and a.cedula}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "apellido", "email", "cedula"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"
        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            if not es_email_valido(email): return f"Email inválido: '{email}'"
            if email in {a.email for a in self.lista if a.id != id_actual}:
                return "Ese email ya está registrado"
        if "cedula" in datos:
            ced = str(datos["cedula"]).strip()
            if ced in self.cedulas_registradas(id_actual):
                return f"La cédula '{ced}' ya está registrada"
        return None

    def leer(self): return self.lista
    def obtener(self, id_a):
        for a in self.lista:
            if a.id == id_a: return a
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [a for a in self.lista if t in a.nombre.lower() or t in a.apellido.lower() or t in a.cedula.lower()]

    def siguiente(self):
        return max([a.id for a in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        adoptante = Adoptante(
            self.siguiente(), str(datos["nombre"]).strip().title(),
            str(datos["apellido"]).strip().title(), str(datos["email"]).strip().lower(),
            str(datos["cedula"]).strip(), str(datos.get("telefono", "")).strip()
        )
        self.lista.append(adoptante)
        self.guardar()
        return True, f"Adoptante registrado: {adoptante.etiqueta()}"

    def actualizar(self, id_a, datos):
        a = self.obtener(id_a)
        if not a: return False, "No existe"
        error = self.validar(datos, id_a)
        if error: return False, error
        for k, v in datos.items():
            val = str(v).strip()
            if k in ("nombre", "apellido"): val = val.title()
            elif k == "email": val = val.lower()
            setattr(a, k, val)
        self.guardar()
        return True, f"Adoptante {id_a} actualizado"

    def eliminar(self, id_a):
        a = self.obtener(id_a)
        if not a: return False, "No existe"
        self.lista.remove(a)
        self.guardar()
        return True, "Adoptante eliminado"


class MascotaRefugioController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "mascotas_refugio.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [MascotaRefugio.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([m.a_diccionario() for m in self.lista])

    def chips_registrados(self, excepto_id=None):
        return {m.chip_id.strip().upper() for m in self.lista if m.id != excepto_id and m.chip_id}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("chip_id", "nombre_mascota", "especie", "edad_meses"):
                if str(datos.get(campo, "")).strip() == "": return f"El campo {campo} es obligatorio"
        if "chip_id" in datos:
            chip = str(datos["chip_id"]).strip().upper()
            if chip in self.chips_registrados(id_actual): return f"El chip '{chip}' ya existe"
        return None

    def leer(self): return self.lista
    def obtener(self, id_m):
        for m in self.lista:
            if m.id == id_m: return m
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [m for m in self.lista if t in m.chip_id.lower() or t in m.nombre_mascota.lower() or t in m.especie.lower()]

    def siguiente(self):
        return max([m.id for m in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        mascota = MascotaRefugio(
            self.siguiente(), str(datos["chip_id"]).strip().upper(),
            str(datos["nombre_mascota"]).strip().title(), str(datos["especie"]).strip().title(),
            int(datos["edad_meses"]), True
        )
        self.lista.append(mascota)
        self.guardar()
        return True, f"Mascota registrada: {mascota.etiqueta()}"

    def actualizar(self, id_m, datos):
        m = self.obtener(id_m)
        if not m: return False, "No existe"
        error = self.validar(datos, id_m)
        if error: return False, error
        if "chip_id" in datos: m.chip_id = str(datos["chip_id"]).strip().upper()
        if "nombre_mascota" in datos: m.nombre_mascota = str(datos["nombre_mascota"]).strip().title()
        if "especie" in datos: m.especie = str(datos["especie"]).strip().title()
        if "edad_meses" in datos and str(datos["edad_meses"]).strip() != "": m.edad_meses = int(datos["edad_meses"])
        self.guardar()
        return True, "Mascota actualizada"

    def eliminar(self, id_m):
        m = self.obtener(id_m)
        if not m: return False, "No existe"
        self.lista.remove(m)
        self.guardar()
        return True, "Mascota eliminada"

    def mascotas_disponibles(self):
        return [m for m in self.lista if m.disponible]


class ProcesoAdopcionController(CrudBase):
    def __init__(self, adoptantes, mascotas, archivo=None):
        self.adoptantes = adoptantes
        self.mascotas = mascotas
        ruta = archivo or os.path.join(DATA_DIR, "procesos_adopcion.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [ProcesoAdopcion.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([p.a_diccionario() for p in self.lista])

    def validar(self, datos):
        try:
            adp_id = int(datos.get("adoptante_id", 0))
            mas_id = int(datos.get("mascota_id", 0))
        except (TypeError, ValueError):
            return "IDs inválidos"
        if not self.adoptantes.obtener(adp_id): return "No existe el adoptante"
        mascota = self.mascotas.obtener(mas_id)
        if not mascota: return "No existe la mascota"
        if not mascota.disponible: return f"La mascota {mascota.nombre_mascota} ya fue adoptada"
        return None

    def leer(self): return self.lista
    def obtener(self, id_p):
        for p in self.lista:
            if p.id == id_p: return p
        return None

    def buscar(self, t):
        return [p for p in self.lista if t.strip() in p.fecha_adopcion]

    def siguiente(self):
        return max([p.id for p in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        mascota = self.mascotas.obtener(int(datos["mascota_id"]))
        donacion = float(datos.get("donacion_voluntaria", 0.0))

        costo_total = MascotaRefugio.calcular_costo_total_adopcion(donacion)

        proceso = ProcesoAdopcion(
            self.siguiente(), int(datos["adoptante_id"]), mascota.id,
            costo_total, str(datos.get("fecha_adopcion", "")).strip()
        )
        mascota.disponible = False  # Marcar como adoptada
        self.mascotas.guardar()
        self.lista.append(proceso)
        self.guardar()
        return True, f"Proceso de Adopción #{proceso.id} completado con éxito. Total cobrado (incl. tarifa fija de ${MascotaRefugio.TARIFA_TRAMITE}): ${costo_total:.2f}"

    def actualizar(self, id_p, datos): return False, "Los procesos de adopción no se modifican"

    def eliminar(self, id_p):
        p = self.obtener(id_p)
        if not p: return False, "No existe"
        mascota = self.mascotas.obtener(p.mascota_id)
        if mascota:
            mascota.disponible = True  # Liberar mascota de nuevo
            self.mascotas.guardar()
        self.lista.remove(p)
        self.guardar()
        return True, "Proceso cancelado y mascota devuelta a disponibilidad"

    def comprobante_adopcion(self, id_p):
        p = self.obtener(id_p)
        if not p: return None
        a = self.adoptantes.obtener(p.adoptante_id)
        m = self.mascotas.obtener(p.mascota_id)
        texto = f"CERTIFICADO DE ADOPCIÓN REFUGIO #{p.id}   Fecha: {p.fecha_adopcion}\n"
        texto += f"Adoptante: {a.nombre_completo() if a else 'N/A'}   (Cédula: {a.cedula if a else 'N/A'})\n"
        texto += f"Mascota  : [{m.chip_id if m else 'N/A'}] {m.nombre_mascota if m else 'N/A'} ({m.especie if m else 'N/A'})\n"
        texto += f"Tarifa trámite fija: ${MascotaRefugio.TARIFA_TRAMITE:.2f}\n"
        texto += "-" * 50 + f"\nTOTAL PAGADO: ${p.costo_total:.2f}"
        return texto

    def total_recaudado(self):
        return round(sum(p.costo_total for p in self.lista), 2)