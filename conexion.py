from nodo import Nodo
import csv
class Conexion:
    """
    Clase base que representa una conexion entre dos nodos donde valida:
        - Que los nodos sean distintos.
        - Que la distancia sea positiva.
        - Que no exista ya la misma conexion entre los nodos.
    """
    conexiones_registradas = {}
    """
    Se utiliza un diccionario anidado para registrar las conexiones porque permite 
    acceder rapidamente a las conexiones existentes segun el nodo de origen, el destino
    y el tipo de transporte, evitando duplicados de manera eficiente y permitiendo
    consultas directas sin recorrer listas completas.
    """


    def __init__(self, origen: Nodo, destino: Nodo, tipo: str, distancia: float):
        Conexion.verificar_conexion(origen, destino)
        continuar = True
        if not isinstance(distancia, (int, float)) or distancia <= 0:
            raise ValueError("La distancia debe ser un numero positivo")
        if origen not in Conexion.conexiones_registradas:
            Conexion.conexiones_registradas[origen] = {}
        if destino not in Conexion.conexiones_registradas[origen]:
            Conexion.conexiones_registradas[origen][destino] = {}
        if tipo in Conexion.conexiones_registradas[origen][destino]:
            continuar = False
        self.origen = origen
        self.destino = destino
        self.tipo = tipo
        self.distancia = distancia
        if continuar:
            Conexion.conexiones_registradas[self.origen][self.destino][self.tipo] = self
            

    @staticmethod
    def verificar_conexion(origen, destino):
        """Verifica que los nodos de la conexion sean validos y distintos."""
        if not isinstance(origen, Nodo) or not isinstance(destino, Nodo):
            raise TypeError("Origen y destino deben ser instancias de Nodo")
        if origen == destino:
            raise ValueError("El origen y el destino no pueden ser el mismo nodo")

    def __str__(self):
        return f"Conexion de {self.origen} a {self.destino} de tipo {self.tipo} con distancia {self.distancia} km"


class Conexion_Tipo_Ferroviaria(Conexion):
    """o ferroviaria con velocidad maxima."""
    def __init__(self, origen: Nodo, destino: Nodo, tipo:str, distancia: float, velocidad_maxima: int):
        super().__init__(origen, destino, "Ferroviaria", distancia)
        if velocidad_maxima < 0:
            raise ValueError("La velocidad maxima no puede ser negativa")
        self.velocidad_maxima = velocidad_maxima

class Conexion_Tipo_Automotor(Conexion):
    """Conexion automotor con carga maxima."""
    def __init__(self, origen: Nodo, destino: Nodo, tipo:str, distancia: float, carga_maxima: int):
        super().__init__(origen, destino, "Automotor", distancia)
        if carga_maxima < 0:
            raise ValueError("La carga maxima no puede ser negativa")
        self.carga_maxima = carga_maxima

class Conexion_Tipo_Naval(Conexion):
    """Conexion naval con tasa de uso."""
    def __init__(self, origen: Nodo, destino: Nodo, tipo:str, distancia: float, tasa_de_uso:str):
        super().__init__(origen, destino, tipo.title(), distancia)
        self.tasa_de_uso = tasa_de_uso  # validar segun como lo uses luego

class Conexion_Tipo_Aerea(Conexion):
    """Conexion aerea con probabilidad de mal clima."""
    def __init__(self, origen: Nodo, destino: Nodo, tipo:str, distancia: float, probabilidad:float):
        super().__init__(origen, destino, "Aerea", distancia)
        if not 0 <= probabilidad <= 1:
            raise ValueError("La probabilidad debe estar entre 0 y 1")
        self.probabilidad = probabilidad
        
        
def crear_conexiones_desde_csv(archivo_csv: str, nodos: dict[str, Nodo]):
    """
    Lee un archivo csv con los datos de las conexiones, busca los nodos origen y destino 
    en el diccionario de nodos, crea las conexiones correspondientes segun el tipo 
    (ferroviaria, automotor, naval o aerea), valida los datos.
    """
    try:
        with open(archivo_csv, mode='r', newline='') as file:
            reader = csv.reader(file)
            try:
                next(reader)
            except StopIteration:
                raise ValueError("El archivo CSV esta vacio")

            for row in reader:
                if not row or len(row) < 6:
                    print(f"Fila del CSV incompleta o mal formada : {row}")
                    continue
                
                nombre_origen, nombre_destino, tipo, distancia_str, _, valor_extra_str = row
                for campo in [nombre_origen, nombre_destino, tipo]:
                    if not isinstance(campo, str):
                        print(f"El campo {campo} debe ser un string.")
                        continue
                tipo = tipo.strip().lower()
                nombre_origen = nombre_origen.strip()
                nombre_destino = nombre_destino.strip()

                if not nombre_origen or not nombre_destino:
                    print("Nombre de nodo origen/destino vacio")
                    continue
                origen = nodos.get(nombre_origen)
                destino = nodos.get(nombre_destino)
                if not origen or not destino:
                    print(f"Nodo no encontrado: {nombre_origen} o {nombre_destino}")
                    continue
                try:
                    distancia = float(distancia_str)
                except:
                    print(f"Distancia invalida: {distancia_str}")
                    continue

                if distancia <= 0:
                    print("La distancia debe ser mayor a 0 km")
                    continue

                if tipo == "ferroviaria":
                    velocidad_maxima = int(valor_extra_str) if valor_extra_str else 0
                    Conexion_Tipo_Ferroviaria(origen, destino, 'Ferroviaria', distancia, velocidad_maxima)
                    Conexion_Tipo_Ferroviaria( destino,origen, 'Ferroviaria', distancia, velocidad_maxima)

                elif tipo == "automotor":
                    carga_maxima = int(valor_extra_str) if valor_extra_str else 0
                    Conexion_Tipo_Automotor(origen, destino, 'Automotor', distancia, carga_maxima)
                    Conexion_Tipo_Automotor(destino, origen, 'Automotor', distancia, carga_maxima)

                elif tipo in {"fluvial", "maritima"}:
                    tasa_de_uso = valor_extra_str or "N/A" 
                    Conexion_Tipo_Naval(origen, destino, tipo.title(), distancia, tasa_de_uso)
                    Conexion_Tipo_Naval(destino, origen, tipo.title(), distancia, tasa_de_uso)

                elif tipo == "aerea":
                    probabilidad = float(valor_extra_str) if valor_extra_str else 0
                    Conexion_Tipo_Aerea(origen, destino, 'Aerea', distancia, probabilidad)
                    Conexion_Tipo_Aerea(destino, origen, 'Aerea', distancia, probabilidad)

                else:
                    raise ValueError(f"Tipo de conexion desconocido: {tipo}")
                    continue
    except FileNotFoundError:
        raise FileNotFoundError(f"El archivo {archivo_csv} no existe.")
    except Exception as e:
        raise ValueError(f"Error al procesar el archivo CSV: {e}")





