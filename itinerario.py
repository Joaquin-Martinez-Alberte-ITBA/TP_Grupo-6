class Itinerario:
    def __init__(self, id_carga, metodo_optimizacion):
        self.id_carga = id_carga
        self.tramos = []  # Lista de diccionarios: [{'origen': Nodo, 'destino': Nodo, 'vehiculo': Vehiculo, 'distancia': float}]
        self.costo_total = 0
        self.tiempo_total = 0
        self.metodo_optimizacion = metodo_optimizacion  # "costo" o "tiempo"

    def agregar_tramo(self, origen, destino, vehiculo):
        distancia = vehiculo.distancia  # Asumiendo que esto es la distancia entre origen y destino
        costo = vehiculo.costo_por_uso
        tiempo = vehiculo.tiempo

        self.tramos.append({
            "origen": origen,
            "destino": destino,
            "vehiculo": vehiculo,
            "distancia": distancia,
            "costo": costo,
            "tiempo": tiempo
        })

        self.costo_total += costo
        self.tiempo_total += tiempo

    def contiene_loops(self):
        visitados = set()
        for tramo in self.tramos:
            if tramo["origen"] in visitados:
                return True
            visitados.add(tramo["origen"])
        return False

    def resumen(self):
        print(f"Itinerario para ID Carga: {self.id_carga}")
        print(f"Optimización: {self.metodo_optimizacion}")
        for tramo in self.tramos:
            print(f"{tramo['origen'].nombre_ciudad} -> {tramo['destino'].nombre_ciudad} | "
                  f"Vehículo: {tramo['vehiculo'].__class__.__name__} | "
                  f"Distancia: {tramo['distancia']} km | "
                  f"Tiempo: {tramo['tiempo']} h | "
                  f"Costo: ${tramo['costo']}")
        print(f"Costo Total: ${self.costo_total} | Tiempo Total: {self.tiempo_total} hs")
        