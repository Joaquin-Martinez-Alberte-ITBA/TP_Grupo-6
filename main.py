from nodo import Nodo, cargar_nodos_desde_csv
from conexion import crear_conexiones_desde_csv
from conexion import Conexion
from tramo import procesar_tramos
def main():
    cargar_nodos_desde_csv("nodos.csv")
    print("--- Nodos registrados ---")
    for nombre, nodo in Nodo.nodos_registrados.items():
        print(nodo)
    archivo_csv = "conexiones.csv"
    conexiones = crear_conexiones_desde_csv(archivo_csv, Nodo.nodos_registrados)
    print("\nConexiones cargadas:")
    for origen, destinos in Conexion.conexiones_registradas.items():
        for destino, tipos in destinos.items():
            for tipo, conexion in tipos.items():
                print(conexion)
    procesar_tramos()
if __name__ == "__main__":
    main()