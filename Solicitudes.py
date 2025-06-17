import csv
from nodo import Nodo
from collections import deque

def leer_solicitudes_csv() -> deque:
    """
    Lee el archivo 'solicitudes.csv' y devuelve una cola de solicitudes.

    Cada solicitud es una lista:
        [id_carga (str), peso_kg (float >= 0), origen (str), destino (str)]

    Validaciones por fila:
      1) Al menos 4 columnas.
      2) ID no vacio.
      3) Peso convertible a float y >= 0.
      4) Origen y destino no vacios.

    Comportamiento:
      - Filas invalidas se omiten con mensaje descriptivo.
      - Se continua procesando las demas filas.
      - Si el archivo no existe, se informa y retorna cola vacia.

    Que devuelve:
        deque: Para las solicitudes validas.
    """
    cola = deque()
    try:
        with open('solicitudes.csv', mode='r', newline='') as archivo:
            reader = csv.reader(archivo)
            next(reader)  # Salta encabezado
            for row in reader:
                try:
                    if len(row) < 4:
                        raise ValueError('Datos incompletos en la fila')

                    id_carga = row[0].strip()
                    if not id_carga:
                        raise ValueError('ID de carga vacio')

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
                    # Validar que origen y destino sean nodos registrados
                    if origen not in Nodo.nodos_registrados or destino not in Nodo.nodos_registrados:
                        raise ValueError(f'Origen o destino no registrado: {origen}, {destino}')
                    
                    cola.append([id_carga, peso, origen, destino])

                except ValueError as ve:
                    print(f"Solicitud '{id_carga if 'id_carga' in locals() and id_carga else 'desconocida'}' invalida: {ve}")
                    continue
                except Exception as e:
                    print(f"Error inesperado al procesar fila {row}: {e}")
                    continue
        return cola

    except FileNotFoundError:
        print("No se encontro el archivo de solicitudes 'solicitudes.csv'. Verifica la ruta.")
        return deque()
    except Exception as e:
        print(f"Ocurrio un error al leer 'solicitudes.csv': {e}")
        return deque()