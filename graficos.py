import matplotlib.pyplot as plt
import numpy as np
from nodo import Nodo
from conexion import Conexion


def _calcular_distancia(ruta_ciudades: list[str]) -> float:
    """Calcula la distancia total de la ruta usando las conexiones ya cargadas."""
    distancia = 0
    for origen, destino in zip(ruta_ciudades, ruta_ciudades[1:]):
        o = Nodo.nodos_registrados[origen]
        d = Nodo.nodos_registrados[destino]
        # usa la primera conexión disponible entre ambos nodos
        conexion = next(iter(Conexion.conexiones_registradas[o][d].values()))
        distancia += conexion.distancia
    return distancia


def graficar_itinerario(tramos_guardados: dict) -> None:
    """Genera los gráficos de distancia/tiempo y costo/distancia a partir de los tramos calculados."""
    distancias = []
    tiempos = []
    costos = []

    # extrae información de cada itinerario
    for tipos in tramos_guardados.values():
        for tramos in tipos.values():
            for tramo in tramos:
                distancias.append(_calcular_distancia(tramo["ruta"]))
                tiempos.append(tramo["tiempo_total"])
                costos.append(tramo["costo"])

    dist_acum = np.cumsum(distancias)
    time_acum = np.cumsum(tiempos)
    cost_acum = np.cumsum(costos)

    # Distancia acumulada vs. Tiempo acumulado
    plt.figure()
    plt.plot(time_acum, dist_acum, marker="o")
    plt.xlabel("Tiempo acumulado (min)")
    plt.ylabel("Distancia acumulada (km)")
    plt.title("Distancia vs. Tiempo")

    # Costo acumulado vs. Distancia acumulada
    plt.figure()
    plt.plot(dist_acum, cost_acum, marker="o", color="red")
    plt.xlabel("Distancia acumulada (km)")
    plt.ylabel("Costo acumulado ($)")
    plt.title("Costo vs. Distancia")

    plt.tight_layout()
    plt.show()


