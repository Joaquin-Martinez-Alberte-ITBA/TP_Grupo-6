from vehiculos import Camion, Tren, Avion, Barco
def calculadora_de_costos(tipo,distancia,peso,cantidad_vehiculos,ruta):
    costos_por_km = {
        "Ferroviaria": None,
        "Automotor": Camion().costo_por_km,
        "Aerea": Avion().costo_por_km,
        "Fluvial": Barco().costo_por_km,
        "Maritima": Barco().costo_por_km
    }
    costos_por_kg = {
        "Ferroviaria": Tren().costo_por_kg, 
        "Automotor": None,
        "Aerea": Avion().costo_por_kg,
        "Fluvial": Barco().costo_por_kg,
        "Maritima": Barco().costo_por_kg
    }
    costos_fijos = {
        "Ferroviaria": Tren().costo_fijo,
        "Automotor": Camion().costo_fijo,
        "Aerea": Avion().costo_fijo,
        "Fluvial": None,
        "Maritima": None
    }
    if tipo == "Fluvial":
        costo_fijo = Barco().costo_fluvial
    elif tipo == "Maritima":
        costo_fijo = Barco().costo_maritimo
    else:
        costo_fijo = int(costos_fijos.get(tipo, 0))

    if tipo == "Ferroviaria":
        if distancia >200:
            costo_km = Tren().costo_km_largo
        else:
            costo_km = Tren().costo_km_corto
    else:
        costo_km = int(costos_por_km.get(tipo, 0))
    
    if tipo == "Automotor":
        if peso < 15000:
            costo_kg = Camion.costo_kg_liviano
        else:
            costo_kg = Camion.costo_kg_pesado
    else:
        costo_kg = int(costos_por_kg.get(tipo, 0))
    tramos = len(ruta) - 1
    costo_total = (costo_km * int(distancia))*int(cantidad_vehiculos) + (costo_kg * peso) + costo_fijo*int(cantidad_vehiculos)*tramos
    return costo_total
    

    