from nodo import Nodo
from conexion import Conexion
from vehiculos import Vehiculo, Camion, Tren, Avion, Barco
import math

def cantidad_de_vehiculos(ruta: list[Nodo], tipo: str, peso:float):
    cantidad=0
    if tipo=='Aerea':
        capacidad_final=Avion().capacidad_kg
    elif tipo=='Maritimo' or tipo=='Fluvial':
        capacidad_final=Barco().capacidad_kg
    elif tipo=='Ferroviaria':
        capacidad_final=Tren().capacidad_kg
    elif tipo=='Automotor':
        capacidad=Camion().capacidad_kg
        for i in range(len(ruta) - 1):
            origen = ruta[i]
            destino = ruta[i + 1]
            carga_maxima = getattr(Conexion.conexiones_registradas[origen][destino][tipo], 'carga_maxima', None)
            if carga_maxima == 0:
                capacidad_final = capacidad
            else:
                capacidad_final=min(capacidad, carga_maxima)
    numero_vehiculos = (peso / capacidad_final)
    carga_por_vehiculo =[]
    while numero_vehiculos > 0:
        if numero_vehiculos >=1:
            carga_por_vehiculo.append(capacidad_final)
            numero_vehiculos -= 1
        else:
            carga_por_vehiculo.append(capacidad_final * numero_vehiculos)
            numero_vehiculos -= 1
    return carga_por_vehiculo
