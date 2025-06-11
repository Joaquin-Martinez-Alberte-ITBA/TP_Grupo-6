import string
import math
import random
from nodo import Nodo, cargar_nodos_desde_csv
from conexion import crear_conexiones_desde_csv, Conexion
from Solicitudes import leer_solicitudes_csv
from vehiculos import Camion, Tren, Avion, Barco
from capacidad import cantidad_de_vehiculos
from Costos import calculadora_de_costos

VELOCIDAD_POR_TIPO = {
    "Ferroviaria": Tren().velocidad_kmh,
    "Automotor": Camion().velocidad_kmh,
    "Aerea": Avion().velocidad_normal,
    "Fluvial": Barco().velocidad_kmh,
}

tramos_guardados = {}

def buscar_rutas(origen: Nodo, destino: Nodo, tipo: str):
    rutas = []

    def camino_encontrado(actual, camino, distancia_acumulada):
        if actual == destino:
            rutas.append((camino[:], distancia_acumulada))
            return
        conexiones = Conexion.conexiones_registradas.get(actual, {})
        for siguiente, modos in conexiones.items():
            if tipo in modos and siguiente not in camino:
                distancia = modos[tipo].distancia
                camino_encontrado(siguiente, camino + [siguiente], distancia_acumulada + distancia)

    camino_encontrado(origen, [origen], 0)
    return rutas

def calcular_tiempo(ruta: list[Nodo], tipo: str):
    tiempo_horas = 0
    for origen, destino in zip(ruta, ruta[1:]):
        conexion = Conexion.conexiones_registradas[origen][destino][tipo]
        velocidad = VELOCIDAD_POR_TIPO[tipo]
        if tipo == "Ferroviaria":
            vmax = getattr(conexion, "velocidad_maxima", 0)
            if vmax:
                velocidad = min(velocidad, vmax)
        elif tipo == "Aerea":
            prob = getattr(conexion, "probabilidad", 0)
            if prob and random.random() < prob:
                velocidad = Avion.velocidad_reducida
        tiempo_horas += conexion.distancia / velocidad
    return tiempo_horas * 60

def procesar_tramos():
    solicitudes = leer_solicitudes_csv()
    types = ['Ferroviaria', 'Automotor', 'Aerea', 'Fluvial', 'Maritima']
    letra_index = 0  # índice global para letras

    for type in types:
        for id_carga, peso, origen_name, destino_name in solicitudes:
            origen = Nodo.nodos_registrados[origen_name]
            destino = Nodo.nodos_registrados[destino_name]
            rutas = buscar_rutas(origen, destino, type)

            if id_carga not in tramos_guardados:
                tramos_guardados[id_carga] = {}
            tramos_guardados[id_carga][type] = []

            for ruta, distancia in rutas:
                if letra_index < 26:
                    letra = string.ascii_uppercase[letra_index]
                else:
                    letra = f"({letra_index})"
                letra_index += 1

                cantidad_vehiculos = cantidad_de_vehiculos(ruta, type, peso)
                tiempo_total = calcular_tiempo(ruta, type)
                costo = calculadora_de_costos(type, distancia, peso, cantidad_vehiculos, ruta)

                tramos_guardados[id_carga][type].append({
                    "letra": letra,
                    "ruta": [nodo.nombre_ciudad for nodo in ruta],
                    "distancia_total": distancia,
                    "tiempo_total": tiempo_total,
                    "peso": peso,
                    "cantidad_vehiculos": cantidad_vehiculos,
                    "costo": costo,
                })

                print(
                    f"{letra} - {type}: "
                    + " -> ".join(nodo.nombre_ciudad for nodo in ruta)
                    + f" | {math.ceil(distancia)} km"
                    + f" | {math.ceil(tiempo_total)} min"
                    + f" | {cantidad_vehiculos} vehículos necesarios"
                    + f" | Costo: {math.ceil(costo)} $"
                )
