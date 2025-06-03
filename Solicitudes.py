import csv

def leer_solicitudes_csv():
    solicitudes = []
    with open('solicitudes.csv', mode='r', newline='') as archivo:
        reader = csv.reader(archivo)
        next(reader)
        for fila in reader:
            id_carga = fila[0]
            peso_kg = float(fila[1])
            origen = fila[2]
            destino = fila[3]
            solicitudes.append([id_carga, peso_kg, origen, destino])
    return solicitudes