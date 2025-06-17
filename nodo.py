import csv
class Nodo():
    """
    La clase Nodo representa cada ciudad de la red de transporte.
    Guarda el nombre de la ciudad y registra los nodos creados en un diccionario
    de clase para evitar duplicados y facilitar el acceso rapido a los nodos existentes.
    """

    nodos_registrados = {}

    def __init__(self, nombre_ciudad):
        if not isinstance(nombre_ciudad, str):
            raise TypeError("El nombre de la ciudad debe ser una cadena de texto.")
        nombre_ciudad = nombre_ciudad.strip()

        if not nombre_ciudad:
            raise ValueError("El nombre de la ciudad no puede estar vacio.")
        
        self.nombre_ciudad = nombre_ciudad

        if nombre_ciudad not in Nodo.nodos_registrados:
            Nodo.nodos_registrados[nombre_ciudad] = self



    def __str__(self):
        return f"Ciudad: {self.nombre_ciudad}"


def cargar_nodos_desde_csv(ruta_csv: str):
    """
    Lee el archivo csv y carga los nodos creando las instancias de Nodo,
    validando duplicados y registrandolos en el diccionario de la clase.
    """
    try:
        with open(ruta_csv, mode="r", newline="") as archivo:
            reader = csv.reader(archivo)
            next(reader, None)
            for fila in reader:
                if not fila:
                    continue
                nombre = fila[0].strip()
                try:
                    Nodo(nombre)
                except ValueError as e:
                    print(f"Error al cargar nodo '{nombre}': {e}")
    except FileNotFoundError:
        print("El archivo no se encontro")




    