import matplotlib.pyplot as plt
import numpy as np
from tramo import procesar_tramos, tramos_guardados

procesar_tramos()  # carga los datos en tramos_guardados

distancias = []
tiempos = []
costos = []

for carga in tramos_guardados.values():
    for rutas in carga.values():
        for tramo in rutas:
            distancias.append(tramo["distancia_total"])
            tiempos.append(tramo["tiempo_total"])
            costos.append(tramo["costo"])

# Calcular acumulados si se desea visualizar la evolución
dist_acum = np.cumsum(distancias)
time_acum = np.cumsum(tiempos)
cost_acum = np.cumsum(costos)

# Distancia acumulada vs. tiempo acumulado
plt.figure()
plt.plot(dist_acum, time_acum, marker='o')
plt.xlabel("Distancia acumulada (km)")
plt.ylabel("Tiempo acumulado (min)")
plt.title("Distancia vs Tiempo")

# Costo acumulado vs. tiempo acumulado
plt.figure()
plt.plot(time_acum, cost_acum, marker='o', color='red')
plt.xlabel("Tiempo acumulado (min)")
plt.ylabel("Costo acumulado ($)")
plt.title("Costo vs Tiempo")

plt.show()
