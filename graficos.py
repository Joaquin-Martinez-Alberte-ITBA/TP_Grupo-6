import matplotlib.pyplot as plt
import numpy as np
from nodo import Nodo
from conexion import Conexion

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
    '''Genera gráficos de distancia vs tiempo y costo vs distancia para una carga específica.'''
    distancias = []
    tiempos = []
    costos = []

    for tramos in carga_dict.values():
        for tramo in tramos:
            distancias.append(_calcular_distancia(tramo["ruta"]))
            tiempos.append(tramo["tiempo_total"])
            costos.append(tramo["costo"])

    dist_acum = np.cumsum(distancias)
    time_acum = np.cumsum(tiempos)
    cost_acum = np.cumsum(costos)

    plt.figure()
    plt.plot(time_acum, dist_acum, marker="o")
    plt.xlabel("Tiempo acumulado (min)")
    plt.ylabel("Distancia acumulada (km)")
    plt.title(f"Distancia vs Tiempo - {id_carga}")

    plt.figure()
    plt.plot(dist_acum, cost_acum, marker="o", color="red")
    plt.xlabel("Distancia acumulada (km)")
    plt.ylabel("Costo acumulado ($)")
    plt.title(f"Costo vs Distancia - {id_carga}")

    plt.tight_layout()
    plt.show()


