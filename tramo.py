from conexion import Conexion
from conexion import Automotor
from conexion import Ferroviaria
from vehiculos import Vehiculo

class Tramo:
    def __init__(self, conexion, vehiculo, carga_kg: float):
        # Validaciones
        if vehiculo.modo != conexion.tipo:
            raise ValueError(
                f"El vehículo de modo '{vehiculo.modo}' no puede circular por una conexión de tipo '{conexion.tipo}'."
            )

        if carga_kg > vehiculo.capacidad_kg:
            raise ValueError(
                f"La carga de {carga_kg} kg excede la capacidad del vehículo ({vehiculo.capacidad_kg} kg)."
            )

        # Validaciones específicas según tipo de conexión
        if isinstance(Conexion, Automotor) and carga_kg > conexion.carga_maxima:
            raise ValueError(
                f"La carga de {carga_kg} kg excede la carga máxima permitida por la conexión automotor ({conexion.carga_maxima} kg)."
            )

        if isinstance(Conexion, Ferroviaria):
            velocidad_max = conexion.velocidad_maxima
        else:
            velocidad_max = None  # Sin límite explícito

        # Guardar atributos
        self.origen = conexion.origen
        self.destino = conexion.destino
        self.tipo_conexion = conexion.tipo
        self.vehiculo = vehiculo
        self.distancia = conexion.distancia
        self.carga_kg = carga_kg

        # Determinar velocidad efectiva
        self.velocidad_utilizada = (
            min(vehiculo.velocidad_kmh, velocidad_max)
            if velocidad_max is not None
            else vehiculo.velocidad_kmh
        )

        # Cálculo del costo del tramo
        self.costo_fijo = vehiculo.costo_fijo
        self.costo_km = vehiculo.costo_por_km * self.distancia
        self.costo_kg = vehiculo.costo_por_kg * carga_kg
        self.costo = self.costo_fijo + self.costo_km + self.costo_kg

    def __repr__(self):
        return (
            f"<Tramo {self.origen.nombre} → {self.destino.nombre} | "
            f"tipo: {self.tipo_conexion}, vehículo: {self.vehiculo.__class__.__name__}, "
            f"distancia: {self.distancia} km, velocidad: {self.velocidad_utilizada} km/h, "
            f"costo total: ${self.costo:.2f}>"
        )

