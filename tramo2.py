import random
from conexion import Conexion, Aerea, Automotor
from vehiculos import Vehiculo, Camion, Tren, Avion


def validar_compatibilidad_modo(conexion: Conexion, vehiculo: Vehiculo) -> bool:
    return vehiculo.modo.lower() == conexion.tipo.lower()

def validar_peso_en_vehiculo(vehiculo: Vehiculo, carga_kg: float) -> bool:
    return carga_kg <= vehiculo.capacidad_kg

def validar_peso_en_conexion(conexion: Conexion, carga_kg: float) -> bool:
    if isinstance(conexion, Automotor):
        return carga_kg <= conexion.carga_maxima
    return True

def validar_longitud_tramo(conexion: Conexion) -> bool:
    return conexion.distancia > 0

def validar_clima(conexion: Conexion) -> bool:
    if isinstance(conexion, Aerea) and hasattr(conexion, "probabilidad"):
        return random.random() > conexion.probabilidad
    return True

class Tramo:
    def __init__(self, conexion: Conexion, vehiculo: Vehiculo, carga_kg: float):
        if not validar_compatibilidad_modo(conexion, vehiculo):
            raise ValueError("Modo del vehículo incompatible con la conexión.")
        if not validar_peso_en_vehiculo(vehiculo, carga_kg):
            raise ValueError("La carga excede la capacidad del vehículo.")
        if not validar_peso_en_conexion(conexion, carga_kg):
            raise ValueError("La carga excede el límite de la conexión.")
        if not validar_longitud_tramo(conexion):
            raise ValueError("La distancia de la conexión debe ser mayor a cero.")

        self.origen = conexion.origen
        self.destino = conexion.destino
        self.modo = conexion.tipo
        self.vehiculo = vehiculo
        self.distancia = conexion.distancia
        self.carga_kg = carga_kg
        self.hubo_mal_clima = False

        # Velocidad efectiva
        velocidad_maxima = getattr(conexion, "velocidad_maxima", None)

        if isinstance(vehiculo, Avion):
            if not validar_clima(conexion):
                self.hubo_mal_clima = True
                velocidad_base = Avion.velocidad_reducida
            else:
                velocidad_base = Vehiculo.velocidad_kmh
        else:
            velocidad_base = Vehiculo.velocidad_kmh

        self.velocidad_utilizada = min(velocidad_base, velocidad_maxima) if velocidad_maxima else velocidad_base
        self.tiempo = self.distancia / self.velocidad_utilizada

        # Costo fijo (ya definido al instanciar el vehículo)
        self.costo_fijo = vehiculo.costo_fijo

        # Costo por km
        if isinstance(vehiculo, Tren):
            self.costo_km = Tren.costo_km_corto if self.distancia < 200 else Tren.costo_km_largo
        else:
            self.costo_km = vehiculo.costo_por_km

        # Costo por kg
        if isinstance(vehiculo, Camion):
            self.costo_kg = Camion.costo_kg_liviano if self.carga_kg < 15000 else Camion.costo_kg_pesado
        else:
            self.costo_kg = vehiculo.costo_por_kg

        # Costo total
        self.costo = (
            self.costo_fijo +
            self.costo_km * self.distancia +
            self.costo_kg * self.carga_kg
        )

    def __repr__(self):
        clima_str = " (mal clima)" if self.hubo_mal_clima else ""
        return (
            f"<Tramo {self.origen.nombre} → {self.destino.nombre} | "
            f"modo: {self.modo}, vehículo: {self.vehiculo.__class__.__name__}{clima_str}, "
            f"distancia: {self.distancia} km, velocidad: {self.velocidad_utilizada:.1f} km/h, "
            f"tiempo: {self.tiempo:.2f} h, costo: ${self.costo:.2f}>"
        )
