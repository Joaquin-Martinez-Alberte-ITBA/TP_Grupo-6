from nodo import Nodo
from conexion import Conexion
from vehiculos import Vehiculo, Camion, Tren, Avion, Barco
import math

def cantidad_de_vehiculos(ruta: list[Nodo], tipo: str, peso:float):
    cantidad=0
    if tipo=='Aerea':
        capacidad=Avion().capacidad_kg
    elif tipo=='Maritimo' or tipo=='Fluvial':
        capacidad=Barco().capacidad_kg
    elif tipo=='Ferroviaria':
        capacidad=Tren().capacidad_kg
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
        cantidad=math.ceil(peso / capacidad_final)
        return cantidad
    cantidad=math.ceil(peso / capacidad) 
    return cantidad
