import csv
from collections import deque

def leer_solicitudes_csv():
    """
    Lee el archivo 'solicitudes.csv' y devuelve una cola FIFO (deque) de solicitudes.
    Cada solicitud tiene el formato: [id_carga, peso_kg, origen, destino]
    """
    cola_solicitudes = deque()
    try:
        with open('solicitudes.csv', mode='r', newline='') as archivo:
            reader = csv.reader(archivo)
            next(reader)  # Salta el encabezado
            for fila in reader:
                if len(fila) < 4:
                    continue  # Ignora filas incompletas
                id_carga = fila[0].strip()
                try:
                    peso_kg = float(fila[1])
                except ValueError:
                    peso_kg = 0  # Valor por defecto si el campo es inválido
                origen = fila[2].strip()
                destino = fila[3].strip()
                cola_solicitudes.append([id_carga, peso_kg, origen, destino])
        return cola_solicitudes
    except FileNotFoundError:
        print('Archivo "solicitudes.csv" no encontrado.')
        return deque()
