import random
from nodo import Nodo
from conexion import Conexion
from Solicitudes import leer_solicitudes_csv
from vehiculos import Camion, Tren, Avion, Barco, Vehiculo
from capacidad import cantidad_de_vehiculos

class Tramo:
    def __init__(self, id_tramo, ruta, tiempo_total, costo, modo):
        self.id = id_tramo
        self.ruta = ruta
        self.tiempo_total = tiempo_total
        self.costo = costo
        self.modo = modo

    def __repr__(self):
        return (
            f"Tramo(id={self.id}, modo={self.modo}, costo=${self.costo:.2f}, "
            f"tiempo={self.tiempo_total:.1f} min, ruta={' -> '.join(self.ruta)})"
        )

class Planificador:
    conteo_de_conexiones = {}  # Variable de clase

    VELOCIDAD_POR_TIPO = {
        "Ferroviaria": Tren().velocidad_kmh,
        "Automotor": Camion().velocidad_kmh,
        "Aerea": Avion().velocidad_normal,
        "Fluvial": Barco().velocidad_kmh,
    }

    def __init__(self, id_carga, peso, origen_name, destino_name):
        self.id_carga = id_carga
        self.peso = peso
        self.origen = Nodo.nodos_registrados[origen_name]
        self.destino = Nodo.nodos_registrados[destino_name]
        self.tramos_por_tipo = {}  
        self._procesar()

    def buscar_rutas(self, tipo):
        rutas = []

        def camino(actual, camino_actual):
            if actual == self.destino:
                rutas.append(camino_actual[:])
                return
            conexiones = Conexion.conexiones_registradas.get(actual, {})
            for siguiente, modos in conexiones.items():
                if tipo in modos and siguiente not in camino_actual:
                    camino(siguiente, camino_actual + [siguiente])

        camino(self.origen, [self.origen])
        return rutas

    def calcular_tiempo(self, ruta, tipo):
        tiempo_horas = 0
        for origen, destino in zip(ruta, ruta[1:]):
            conexion = Conexion.conexiones_registradas[origen][destino][tipo]
            velocidad = self.VELOCIDAD_POR_TIPO.get(tipo, 1)
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

    def _procesar(self):
        tipos = ['Ferroviaria', 'Automotor', 'Aerea', 'Fluvial', 'Maritima']
        id_counter = 1

        for tipo in tipos:
            rutas = self.buscar_rutas(tipo)
            self.tramos_por_tipo[tipo] = []

            for ruta in rutas:
                carga_por_vehiculo = cantidad_de_vehiculos(ruta, tipo, self.peso)
                cantidad_vehiculos = len(carga_por_vehiculo)
                tiempo_total = self.calcular_tiempo(ruta, tipo)
                costo = Vehiculo.calculadora_de_costos(tipo, cantidad_vehiculos, ruta, carga_por_vehiculo)
                tramo = Tramo(
                    id_tramo=id_counter,
                    ruta=[nodo.nombre_ciudad for nodo in ruta],
                    tiempo_total=tiempo_total,
                    costo=costo,
                    modo=tipo
                )
                self.tramos_por_tipo[tipo].append(tramo)
                id_counter += 1

                for a, b in zip(ruta, ruta[1:]):
                    clave = (a.nombre_ciudad, b.nombre_ciudad, tipo)
                    Planificador.conteo_de_conexiones[clave] = Planificador.conteo_de_conexiones.get(clave, 0) + 1

    def obtener_kpi(self):
        mejor_costo = None
        menor_tiempo = None

        for tramos in self.tramos_por_tipo.values():
            for tramo in tramos:
                if mejor_costo is None or tramo.costo < mejor_costo.costo:
                    mejor_costo = tramo
                if menor_tiempo is None or tramo.tiempo_total < menor_tiempo.tiempo_total:
                    menor_tiempo = tramo

        mejor_trafico = self.obtener_kpi_trafico()

        texto = ""
        if mejor_costo:
            texto += (
                f"Resultado para {self.id_carga}:La solución {mejor_costo.id} es la más económica.\n"
                f"● Modo: {mejor_costo.modo}\n"
                f"● Itinerario: {' - '.join(mejor_costo.ruta)}\n"
                f"● Costo total: ${round(mejor_costo.costo)}\n"
                f"● Tiempo total: {int(mejor_costo.tiempo_total)} minutos\n\n"
            )

        if menor_tiempo:
            texto += (
                f"La solución {menor_tiempo.id} es la más rápida.\n"
                f"● Modo: {menor_tiempo.modo}\n"
                f"● Itinerario: {' - '.join(menor_tiempo.ruta)}\n"
                f"● Costo total: ${round(menor_tiempo.costo)}\n"
                f"● Tiempo total: {int(menor_tiempo.tiempo_total)} minutos\n\n"
            )

        if mejor_trafico:
            texto += (
                f"La solución {mejor_trafico.id} tiene el menor tráfico.\n"
                f"● Modo: {mejor_trafico.modo}\n"
                f"● Itinerario: {' - '.join(mejor_trafico.ruta)}\n"
                f"● Costo total: ${round(mejor_trafico.costo)}\n"
                f"● Tiempo total: {int(mejor_trafico.tiempo_total)} minutos\n\n"
            )

        return texto or f"No se encontraron rutas para {self.id_carga}"

    def obtener_kpi_trafico(self):
        menor_trafico = None
        menor_peso = float('inf')

        for lista_tramos in self.tramos_por_tipo.values():
            for tramo in lista_tramos:
                peso = 0
                for a, b in zip(tramo.ruta, tramo.ruta[1:]):
                    clave = (a, b, tramo.modo)
                    peso += Planificador.conteo_de_conexiones.get(clave, 0)
                if peso < menor_peso:
                    menor_peso = peso
                    menor_trafico = tramo

        return menor_trafico

    def obtener_todos_los_tramos_formateados(self):
        texto = f"Tramos disponibles para {self.id_carga}:\n"
        for tipo, tramos in self.tramos_por_tipo.items():
            if tramos:
                texto += f"\nModo: {tipo}\n"
                for tramo in tramos:
                    texto += (
                        f"  Tramo ID {tramo.id}:\n"
                        f"    ● Ruta: {' -> '.join(tramo.ruta)}\n"
                        f"    ● Costo: ${round(tramo.costo)}\n"
                        f"    ● Tiempo estimado: {int(tramo.tiempo_total)} minutos\n"
                    )
        return texto + "\n"

def procesar_todas_las_solicitudes():
    solicitudes = leer_solicitudes_csv()
    planificadores = []
    while solicitudes:
        id_carga, peso, origen, destino = solicitudes.popleft()
        planificadores.append(Planificador(id_carga, peso, origen, destino))
    return planificadores
