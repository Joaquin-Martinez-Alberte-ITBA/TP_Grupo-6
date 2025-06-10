from nodo import Nodo
from conexion import Conexion
from vehiculos import Vehiculo, Camion, Tren, Avion, Barco

def cantidad_de_vehiculos(ruta: list[Nodo], tipo: str, peso:float):
    cantidad=0
    if tipo not in ['Aerea', 'Maritimo', 'Fluvial', 'Ferroviaria', 'Camion']:
        raise ValueError("Tipo de vehículo no válido. Debe ser 'Aerea', 'Maritimo', 'Fluvial', 'Ferroviaria' o 'Camion'.")
    if tipo=='Aerea':
        capacidad=Avion().capacidad_kg
    elif tipo=='Maritimo' or tipo=='Fluvial':
        capacidad=Barco().capacidad_kg
    elif tipo=='Ferroviaria':
        capacidad=Tren().capacidad_kg
    elif tipo=='Automotor':
        capacidad=Camion().capacidad_kg
        capacidad_ruta=0
        for i in range(len(ruta) - 1):
            origen = ruta[i]
            destino = ruta[i + 1]
            conexion =Conexion.conexiones_registradas[origen][destino][tipo]
            carga_maxima = getattr(Conexion.conexiones_registradas[origen][destino][tipo], 'carga_maxima', None)
            if carga_maxima<capacidad_ruta or capacidad_ruta==0:
                capacidad_ruta=carga_maxima
        capacidad_final=min(capacidad, capacidad_ruta)
        cantidad=(peso // capacidad_final) + 1 #Le sumamos 1 a la division para asi poder redondear hacia arriba#
    if tipo!='Automotor':
        cantidad=(peso // capacidad) + 1
