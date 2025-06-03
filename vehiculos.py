class Vehiculo:
    def __init__(self,modo:str,velocidad_kmh:float,capacidad_kg:float,costo_fijo:float,costo_por_km:float,costo_por_kg:float):
            self.modo=modo
            self.velocidad_kmh=velocidad_kmh
            self.capacidad_kg=capacidad_kg
            self.costo_fijo=costo_fijo
            self.costo_por_km=costo_por_km
            self.costo_por_kg=costo_por_kg
    def __str__(self):
        return f"Modo: {self.modo}, Velocidad: {self.velocidad_kmh} km/h, Capacidad: {self.capacidad_kg} kg, Costo Fijo: ${self.costo_fijo}, Costo por km: ${self.costo_por_km}, Costo por kg: ${self.costo_por_kg}"

class Camion(Vehiculo):
    costo_kg_liviano=1
    costo_kg_pesado=2
    def __init__(self):
        super().__init__("Automotor",80,30000,30,5,None)
    
class Tren(Vehiculo):
    costo_km_largo=15
    costo_km_corto=20
    def __init__(self):
        super().__init__("Ferrocarril",100,150000,100,None,3)
class Avion(Vehiculo):
    velocidad_reducida=400
    velocidad_normal=600
    def __init__(self):
       super().__init__("Aereo",None,5000,750,40,10) 
class Barco(Vehiculo):
    costo_fluvial=500
    costo_maritimo=1500
    def __init__(self,):
        super().__init__("Maritimo",40,100000,None,15,2)