from nodo import Nodo
import csv
class Conexion:
    conexiones_registradas = {}
    def __init__(self, origen: Nodo, destino: Nodo, tipo: str, distancia: float):
        Conexion.verificar_conexion(origen, destino)
        self.origen = origen
        self.destino = destino
        self.tipo = tipo
        self.distancia = distancia
        if self.origen not in Conexion.conexiones_registradas:
            Conexion.conexiones_registradas[self.origen] = {}
        if self.destino not in Conexion.conexiones_registradas[self.origen]:
            Conexion.conexiones_registradas[self.origen][self.destino] = {}
        if self.tipo in Conexion.conexiones_registradas[self.origen][self.destino]:
            raise ValueError(f"Ya existe una conexión {self.tipo} entre {self.origen} y {self.destino}")
        Conexion.conexiones_registradas[self.origen][self.destino][self.tipo] = self
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
class Fluvial(Conexion):
    def __init__(self, origen: Nodo, destino: Nodo, distancia: float, tasa_de_uso:str):
        super().__init__(origen, destino, "Fluvial", distancia)
        self.tasa_de_uso = tasa_de_uso
class Aerea(Conexion):
    def __init__(self, origen: Nodo, destino: Nodo, distancia: float,probabilidad:float):
        super().__init__(origen, destino, "Aerea", distancia)
        self.probabilidad = probabilidad
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
                if row[5]=='':
                    velocidad_maxima = 0
                else:
                    velocidad_maxima = int(row[5])
                conexion = Ferroviaria(origen, destino, distancia, velocidad_maxima)
            elif tipo == "Automotor":
                if row[5] == '':
                    carga_maxima = 0
                else:
                    carga_maxima = int(row[5])
                conexion = Automotor(origen, destino, distancia, carga_maxima)
            elif tipo == "Fluvial":
                if row[5] == '':
                    tasa_de_uso = 0
                else:
                    tasa_de_uso = row[5]
                conexion = Fluvial(origen, destino, distancia, tasa_de_uso)
            elif tipo == "Aerea":  
                if row[5] == '':
                    probabilidad = 0
                else:
                    probabilidad = float(row[5])
                conexion = Aerea(origen, destino, distancia, probabilidad)
            else:
                raise ValueError(f"Tipo de conexión desconocido: {tipo}")
            conexiones.append(conexion)
    return conexiones





