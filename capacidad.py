from nodo import Nodo
from conexion import Conexion
from vehiculos import Vehiculo, Camion, Tren, Avion, Barco
import math

def cantidad_de_vehiculos(ruta: list[Nodo], tipo: str, peso: float):
    """
    Calcula cuantos vehiculos se necesitan para transportar una carga determinada
    a lo largo de una ruta, segun el tipo de transporte elegido.

    Para cada tramo de la ruta, evalua las capacidades de los vehiculos y 
    las restricciones impuestas por la conexion (por ejemplo, carga maxima en
    conexiones automotor). Luego determina la cantidad de vehiculos necesarios
    y cuanta carga llevara cada uno.

    Parametros:
    ----------
    ruta : list[Nodo]
        Lista de nodos que representa la ruta (incluyendo origen y destino).
    tipo : str
        Tipo de transporte utilizado. Debe ser uno de: 'Aerea', 'Maritimo',
        'Fluvial', 'Ferroviaria', 'Automotor'.
    peso : float
        Peso total de la carga a transportar, en kilogramos.

    Retorna:
    -------
    carga_por_vehiculo : list[float]
        Lista con las cargas asignadas a cada vehiculo. Cada elemento representa
        cuantos kilogramos transporta un vehiculo. La longitud de la lista es
        igual a la cantidad de vehiculos necesarios.

    Excepciones:
    -----------
    ValueError:
        Si se ingresa un tipo de transporte no reconocido.
        """
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
    else:
        raise ValueError(f"Tipo de vehiculo desconocido: {tipo}")
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
