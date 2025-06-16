import string
import random
from nodo import Nodo
from conexion import Conexion
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
    '''Esta funcion busca la ruta a partir de los datos ingresados,esta funcion es llamda en la linea 66
        para encontrar las rutas
    '''
    if not isinstance(origen, Nodo) or not isinstance(destino, Nodo):
        raise TypeError("Origen y destino deben ser instancias de Nodo")
    if not isinstance(tipo, str):
        raise TypeError("El tipo debe ser una cadena de texto")
    rutas = []

    def camino_encontrado(actual, camino, distancia_acumulada):
        '''Esta funcion esta hecha para buscar cada uno de los caminos a partir de las conexiones'''
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
    '''Esta funcion calcula los tiempos que tarda en cada tramo de la ruta para despues sumarlos
    y poder encontrar el tiempo total
    '''
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
    '''Esta funcion es la funcion principal, la que se encarga de primero agarrar las solicitudes.
        Una vez tiene las solicitudes va a ir buscando las rutas para todos los distintos tipos ruta.
        Despues de eso decidimos guardar todas las rutas en un diccionario 'tramos_guardados' para que despues
        sea mas facil acceder a los datos para hacer los KPI.
        Este diccionario contiene todos los itinerarios posibles para una solicitud.
        En caso de necesitar todos los itinerarios es muy facil de llamar.
        Despues se van recorriendo cada una de lass conexiones/tramos en una ruta y va calculando los costos y
        tiempos para luego guardarlos en el diccionario creado.
    '''
    solicitudes = leer_solicitudes_csv()
    while solicitudes:
        solicitud = solicitudes.popleft()
        types = ['Ferroviaria', 'Automotor', 'Aerea', 'Fluvial', 'Maritima']
        letra_index = 0  # indice global para letras
        for type in types:
            id_carga, peso, origen_name, destino_name = solicitud
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
                carga_por_vehiculo = cantidad_de_vehiculos(ruta, type, peso)
                cantidad_vehiculos = len(carga_por_vehiculo)
                tiempo_total = calcular_tiempo(ruta, type)
                costo = calculadora_de_costos(type,cantidad_vehiculos, ruta,carga_por_vehiculo)
                tramos_guardados[id_carga][type].append({
                    "letra": letra,
                    "ruta": [nodo.nombre_ciudad for nodo in ruta],
                    "tiempo_total": tiempo_total,
                    "costo": costo,
                })

