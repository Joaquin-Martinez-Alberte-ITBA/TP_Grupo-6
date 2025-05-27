from tramo import Tramo

class Itinerario:
    def __init__(self, optimizacion):
        if optimizacion not in {"costo", "tiempo"}:
            raise ValueError("El método de optimización debe ser 'costo' o 'tiempo'.")
        self.tramos = []
        self.optimizacion = optimizacion

    def agregar_tramo(self, tramo):
        nodos_visitados = set()
        for t in self.tramos:
            nodos_visitados.add(t.origen)
            nodos_visitados.add(t.destino)
        if tramo.origen in nodos_visitados or tramo.destino in nodos_visitados:
            raise ValueError("El itinerario no puede contener loops (ciclos).")
        self.tramos.append(tramo)

    def costo_total(self):
        return sum(tramo.costo for tramo in self.tramos)

    def tiempo_total(self):
        return sum(tramo.distancia / tramo.velocidad_utilizada for tramo in self.tramos)
    
    def mostrar_itinerario(self):
        print("Itinerario:")
        for i, tramo in enumerate(self.tramos, start=1):
            tiempo = tramo.distancia / tramo.velocidad_utilizada
            print(f"Tramo {i}: {tramo.origen.nombre} → {tramo.destino.nombre}")
            print(f"Vehículo: {tramo.vehiculo.__class__.__name__} ({tramo.modo})")
            print(f"Distancia: {tramo.distancia} km | Velocidad: {tramo.velocidad_utilizada} km/h")
            print(f"Tiempo estimado: {tiempo} h | Costo tramo: ${tramo.costo}")
            print()
        print(f"Método de optimización: {self.optimizacion}")
        print(f"Costo total: ${self.costo_total()}")
        print(f"Tiempo total: {self.tiempo_total()} h")
