import matplotlib.pyplot as plt
import numpy as np
from nodo import Nodo
from conexion import Conexion
from tramo import Planificador  # Para acceder a los conteos

def _calcular_distancia(ruta_ciudades: list[str]) -> float:
    '''Calcula la distancia total de una ruta dada por una lista de ciudades.'''
    distancia = 0
    for origen, destino in zip(ruta_ciudades, ruta_ciudades[1:]):
        o = Nodo.nodos_registrados[origen]
        d = Nodo.nodos_registrados[destino]
        conexion = next(iter(Conexion.conexiones_registradas[o][d].values()))
        distancia += conexion.distancia
    return distancia

def graficar_itinerario_por_carga(carga_dict: dict, id_carga: str):
    '''Genera graficos de distancia vs tiempo y costo vs distancia para una carga especifica.'''
    distancias = []
    tiempos = []
    costos = []

    for tramos in carga_dict.values():
        for tramo in tramos:
            distancias.append(_calcular_distancia(tramo.ruta))
            tiempos.append(tramo.tiempo_total)
            costos.append(tramo.costo)

    if not distancias or not tiempos or not costos:
        print(f"No hay datos para graficar la carga {id_carga}")
        return

    dist_acum = np.cumsum(distancias)
    time_acum = np.cumsum(tiempos)
    cost_acum = np.cumsum(costos)

    fig1 = plt.figure()
    plt.plot(time_acum, dist_acum, marker="o")
    plt.xlabel("Tiempo acumulado (min)")
    plt.ylabel("Distancia acumulada (km)")
    plt.title(f"Distancia vs Tiempo - {id_carga}")

    fig2 = plt.figure()
    plt.plot(dist_acum, cost_acum, marker="o", color="blue")
    plt.xlabel("Distancia acumulada (km)")
    plt.ylabel("Costo acumulado ($)")
    plt.title(f"Costo vs Distancia - {id_carga}")

    plt.tight_layout()
    plt.show()
    return fig2  # Para que el main cierre la ventana si hace falta

def graficar_trafico_red():
    '''Grafica un mapa de calor de la red segun la cantidad de veces que se uso cada conexion.'''
    conteo = Planificador.conteo_de_conexiones
    if not conteo:
        print("No hay trafico registrado para graficar.")
        return

    etiquetas = []
    valores = []

    for (origen, destino, tipo), uso in conteo.items():
        etiquetas.append(f"{origen} -> {destino} ({tipo})")
        valores.append(uso)

    plt.figure(figsize=(12, 6))
    plt.barh(etiquetas, valores, color="indianred")
    plt.xlabel("Cantidad de veces utilizada")
    plt.title("Trafico de la red por conexion y tipo de transporte")
    plt.tight_layout()
    plt.show()

def graficar_vehiculos_usados():
    '''Grafica una barra vertical con la cantidad total de vehiculos usados por tipo.'''
    conteo = Planificador.conteo_vehiculos_por_tipo
    if not conteo or sum(conteo.values()) == 0:
        print("No hay vehiculos registrados para graficar.")
        return

    tipos = list(conteo.keys())
    cantidades = list(conteo.values())

    plt.figure(figsize=(8, 5))
    plt.bar(tipos, cantidades, color="steelblue")
    plt.xlabel("Tipo de vehiculo")
    plt.ylabel("Cantidad total de vehiculos utilizados")
    plt.title("Vehiculos utilizados por tipo en todas las solicitudes")
    plt.tight_layout()
    plt.show()
