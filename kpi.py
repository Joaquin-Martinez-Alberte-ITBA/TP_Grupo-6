from tramo import tramos_guardados
from datetime import timedelta

def formato_tiempo(minutos_totales):
    segundos_totales = int(minutos_totales * 60)
    return str(timedelta(seconds=segundos_totales))

def imprimir_ruta_optima():
    for id_carga, modos in tramos_guardados.items():
        mejor_costo = None
        mejor_tiempo = None

        for tipo, rutas in modos.items():
            for ruta in rutas:
                if mejor_costo is None or ruta["costo"] < mejor_costo["costo"]:
                    mejor_costo = ruta
                    mejor_costo["tipo"] = tipo
                if mejor_tiempo is None or ruta["tiempo_total"] < mejor_tiempo["tiempo_total"]:
                    mejor_tiempo = ruta
                    mejor_tiempo["tipo"] = tipo

        print(f"La solución {mejor_costo['letra']} es la más económica.")
        print(f"● Modo: {modo_con_icono(mejor_costo['tipo'])}")
        print(f"● Itinerario: {' - '.join(mejor_costo['ruta'])}")
        print(f"● Costo total: ${round(mejor_costo['costo'])}")
        print(f"● Tiempo total: {formato_tiempo(mejor_costo['tiempo_total'])}\n")

        print(f"La solución {mejor_tiempo['letra']} es la más rápida.")
        print(f"● Modo: {modo_con_icono(mejor_tiempo['tipo'])}")
        print(f"● Itinerario: {' - '.join(mejor_tiempo['ruta'])}")
        print(f"● Costo total: ${round(mejor_tiempo['costo'])}")
        print(f"● Tiempo total: {formato_tiempo(mejor_tiempo['tiempo_total'])}\n")

def modo_con_icono(tipo):
    iconos = {
        "Ferroviaria": "Ferroviario 🚂",
        "Automotor": "Automotor 🚚",
        "Aerea": "Aéreo ✈️",
        "Fluvial": "Fluvial ⛴️",
        "Maritima": "Marítimo 🚢"
    }
    return iconos.get(tipo, tipo)
