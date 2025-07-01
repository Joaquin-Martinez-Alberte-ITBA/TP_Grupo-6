from collections import deque
import csv
from nodo import Nodo

def leer_solicitudes_csv() -> deque:
    """
    Lee el archivo 'solicitudes.csv' y devuelve una cola de solicitudes.

    Cada solicitud es una lista:
        [id_carga (str), peso_kg (float >= 0), origen (str), destino (str)]

    Validaciones por fila:
      1) Al menos 4 columnas.
      2) ID no vacio ni duplicado.
      3) Peso convertible a float y >= 0.
      4) Origen y destino no vacios ni iguales.
      5) Origen y destino deben existir en los nodos registrados.

    Comportamiento:
      - Filas invalidas o duplicadas se omiten con mensaje.
      - Se continua procesando las demas filas.
      - Si el archivo no existe, se informa y retorna cola vacia.
    """
    cola = deque()
    ids_vistos = set()

    try:
        with open('solicitudes.csv', mode='r', newline='') as archivo:
            reader = csv.reader(archivo)
            next(reader)

            for row in reader:
                try:
                    if len(row) < 4:
                        raise ValueError('Datos incompletos en la fila')

                    id_carga = row[0].strip()
                    if not id_carga:
                        raise ValueError('ID de carga vacio')
                    if id_carga in ids_vistos:
                        raise ValueError(f"ID de carga duplicado: {id_carga}")
                    
                    peso_str = row[1].strip()
                    try:
                        peso = float(peso_str)
                    except ValueError:
                        raise ValueError(f'Peso no es un numero valido: {peso_str}')
                    if peso < 0:
                        raise ValueError(f'Peso negativo: {peso}')
                    
                    origen = row[2].strip()
                    destino = row[3].strip()
                    if not origen or not destino:
                        raise ValueError('Origen o destino vacio')
                    if origen == destino:
                        raise ValueError('Origen y destino no pueden ser iguales')
                    if origen not in Nodo.nodos_registrados or destino not in Nodo.nodos_registrados:
                        raise ValueError(f'Origen o destino no registrado: {origen}, {destino}')
                    
                    cola.append([id_carga, peso, origen, destino])
                    ids_vistos.add(id_carga)

                except ValueError as ve:
                    print(f"Solicitud '{id_carga if 'id_carga' in locals() else 'desconocida'}' invalida: {ve}")
                    continue
                except Exception as e:
                    print(f"Error inesperado al procesar fila {row}: {e}")
                    continue

    except FileNotFoundError:
        print("No se encontro el archivo de solicitudes 'solicitudes.csv'. Verifica la ruta.")
    except Exception as e:
        print(f"Ocurrio un error al leer 'solicitudes.csv': {e}")
    
    return cola
