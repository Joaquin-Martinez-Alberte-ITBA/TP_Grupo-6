from vehiculos import Camion, Tren, Avion, Barco
from conexion import Conexion

def calculadora_de_costos(tipo, cantidad_vehiculos, ruta, carga_por_vehiculo):
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
        "Fluvial": Barco().costo_fluvial,
        "Maritima": Barco().costo_maritimo
    }

    # --- Cálculo del CostoTramo total ---
    costo_total_tramos = 0
    for origen, destino in zip(ruta, ruta[1:]):
        conexion = Conexion.conexiones_registradas[origen][destino][tipo]
        distancia_km = conexion.distancia

        # 1. Definir costo por km
        if tipo == "Ferroviaria":
            if distancia_km >= 200:
                costo_km = Tren().costo_km_largo
            else:
                costo_km = Tren().costo_km_corto
        else:
            costo_km = costos_por_km[tipo]

        # 2. Definir costo fijo según tipo y tasa_de_uso
        if tipo in ["Fluvial", "Maritima"]:
            tasa = getattr(conexion, "tasa_de_uso", "").lower()
            if tasa == "maritimo":
                costo_fijo = Barco().costo_maritimo
            elif tasa == "fluvial":
                costo_fijo = Barco().costo_fluvial
            else:
                costo_fijo = 0
        else:
            costo_fijo = costos_fijos[tipo] or 0

        costo_tramo = (costo_fijo + costo_km * distancia_km) * cantidad_vehiculos
        costo_total_tramos += costo_tramo

    # --- Cálculo del CostoVehiculo total ---
    costo_total_vehiculos = 0
    for carga in carga_por_vehiculo:
        if tipo == "Automotor":
            if carga >= 15000:
                costo_por_kg = Camion().costo_kg_pesado
            else:
                costo_por_kg = Camion().costo_kg_liviano
        else:
            costo_por_kg = costos_por_kg[tipo] or 0

        costo_total_vehiculos += carga * costo_por_kg

    # --- Costo total del itinerario ---
    costo_itinerario = costo_total_tramos + costo_total_vehiculos
    return costo_itinerario


