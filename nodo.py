import csv

class Nodo():
    nodos_registrados = {}
    
    def __init__(self, nombre_ciudad):
        if nombre_ciudad in Nodo.nodos_registrados:
            raise ValueError(f"El nodo {nombre_ciudad} ya está registrado.")
        elif not (isinstance(nombre_ciudad, str)):
            raise TypeError("El nombre de la ciudad debe ser una cadena de texto.")
        self.nombre_ciudad = nombre_ciudad
        Nodo.nodos_registrados[nombre_ciudad] = self

    def __str__(self):
        return f"Ciudad: {self.nombre_ciudad}"
    
def cargar_nodos_desde_csv(ruta_csv: str):
    try:
        with open(ruta_csv, mode='r', newline='') as archivo:
            reader = csv.reader(archivo)
            next(reader)
            for fila in reader:
                nombre = fila[0].strip()
                Nodo(nombre)
    except FileNotFoundError:
        print('El archivo no se encontró')


    