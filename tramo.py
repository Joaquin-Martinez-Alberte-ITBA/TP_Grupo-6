from nodo import Nodo, cargar_nodos_desde_csv
from conexion import crear_conexiones_desde_csv, Conexion
from Solicitudes import leer_solicitudes_csv

# Diccionario donde se guardarán los tramos por ID de carga
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

def procesar_tramos():
    solicitudes = leer_solicitudes_csv()
    types = ['Ferroviaria', 'Automotor', 'Aerea', 'Fluvial']
    for type in types:
        for id_carga, peso, origen_name, destino_name in solicitudes:
            origen = Nodo.nodos_registrados[origen_name]
            destino = Nodo.nodos_registrados[destino_name]
            rutas = buscar_rutas(origen, destino, type)
            if id_carga not in tramos_guardados:
                tramos_guardados[id_carga] = {}
            tramos_guardados[id_carga][type] = []
            for ruta, distancia in rutas:
                tramos_guardados[id_carga][type].append({
                    "ruta": [nodo.nombre_ciudad for nodo in ruta],
                    "distancia_total": distancia
                })
            print(f"Rutas {type} posibles para {id_carga} ({origen_name} → {destino_name})")
            for ruta, distancia in rutas:
                print(" -> ".join(nodo.nombre_ciudad for nodo in ruta) + f" | {distancia} km")

