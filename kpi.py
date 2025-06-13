import time

def convertir_a_hhmmss(minutos):
    segundos = int(minutos * 60)
    return time.strftime("%Hh:%Mm:%Ss", time.gmtime(segundos))

def obtener_ruta_optima(tramos_guardados):
    resultado = ""
    for id_carga, tipos in tramos_guardados.items():
        mejor_costo = None
        menor_tiempo = None

        for tipo, tramos in tipos.items():
            for tramo in tramos:
                if mejor_costo is None or tramo["costo"] < mejor_costo["costo"]:
                    mejor_costo = tramo
                    mejor_costo["modo"] = tipo
                if menor_tiempo is None or tramo["tiempo_total"] < menor_tiempo["tiempo_total"]:
                    menor_tiempo = tramo
                    menor_tiempo["modo"] = tipo

        resultado += f"Resultado para {id_carga}:\n"
        resultado += f"La solución {mejor_costo['letra']} es la más económica.\n"
        resultado += f"● Modo: {mejor_costo['modo']}\n"
        resultado += f"● Itinerario: {' - '.join(mejor_costo['ruta'])}\n"
        resultado += f"● Costo total: ${round(mejor_costo['costo'])}\n"
        resultado += f"● Tiempo total: {convertir_a_hhmmss(mejor_costo['tiempo_total'])}\n\n"

        resultado += f"La solución {menor_tiempo['letra']} es la más rápida.\n"
        resultado += f"● Modo: {menor_tiempo['modo']}\n"
        resultado += f"● Itinerario: {' - '.join(menor_tiempo['ruta'])}\n"
        resultado += f"● Costo total: ${round(menor_tiempo['costo'])}\n"
        resultado += f"● Tiempo total: {convertir_a_hhmmss(menor_tiempo['tiempo_total'])}\n\n"

    return resultado

