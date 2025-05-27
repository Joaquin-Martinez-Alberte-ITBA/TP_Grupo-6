from nodo import Nodo
from nodo import nodos_registrados
import csv
class Conexion:
    def __init__(self, origen: Nodo, destino: Nodo, tipo: str, distancia: float):
        Conexion.verificar_conexion(origen, destino)
        self.origen = origen
        self.destino = destino
        self.tipo = tipo
        self.distancia = distancia
    @staticmethod
    def verificar_conexion(origen, destino):
        if not isinstance(origen, Nodo) or not isinstance(destino, Nodo):
            raise TypeError("Origen y destino deben ser instancias de Nodo")
        if origen == destino:
            raise ValueError("El origen y el destino no pueden ser el mismo nodo")

    def __str__(self):
        return f"Conexión de {self.origen} a {self.destino} de tipo {self.tipo} con distancia {self.distancia} km"


class Ferroviaria(Conexion):
    def __init__(self, origen: Nodo, destino: Nodo, distancia: float, velocidad_maxima: int):
        super().__init__(origen, destino, "Ferroviaria", distancia)
        self.velocidad_maxima = velocidad_maxima


class Automotor(Conexion):
    def __init__(self, origen: Nodo, destino: Nodo, distancia: float, carga_maxima: int):
        super().__init__(origen, destino, "Automotor", distancia)
        self.carga_maxima = carga_maxima


class Maritima(Conexion):
    def __init__(self, origen: Nodo, destino: Nodo, distancia: float, tasa_de_uso:str):
        super().__init__(origen, destino, "Maritima", distancia)
        self.tasa_de_uso = tasa_de_uso


class Aerea(Conexion):
    def __init__(self, origen: Nodo, destino: Nodo, distancia: float):
        super().__init__(origen, destino, "Aerea", distancia)

def crear_conexiones_desde_csv(archivo_csv: str, nodos: dict[str, Nodo]) -> list[Conexion]:
    conexiones = []
    with open(archivo_csv, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            nombre_origen = row[0]
            nombre_destino = row[1]
            tipo = row[2]
            distancia = float(row[3])
            ###Necesito buscar el objeto Nodo en el diccionario nodos
            origen = Nodo.nodos_registrados.get(nombre_origen)
            destino = Nodo.nodos_registrados.get(nombre_destino)
            if not origen or not destino:
                raise ValueError(f"Nodo no encontrado: {nombre_origen} o {nombre_destino}")
            if tipo == "Ferroviaria":
                velocidad_maxima = int(row[5])
                conexion = Ferroviaria(origen, destino, distancia, velocidad_maxima)
            elif tipo == "Automotor":
                carga_maxima = int(row[5])
                conexion = Automotor(origen, destino, distancia, carga_maxima)
            elif tipo == "Maritima":
                tasa_de_uso = row[5]
                conexion = Maritima(origen, destino, distancia, tasa_de_uso)
            elif tipo == "Aerea":
                conexion = Aerea(origen, destino, distancia)
            else:
                raise ValueError(f"Tipo de conexión desconocido: {tipo}")
            conexiones.append(conexion)
    return conexiones
