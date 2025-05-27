class Vehiculo:
    def __init__(self,modo:str,velocidad_kmh:float,capacidad_kg:float,costo_fijo:float,costo_por_km:float,costo_por_kg:float):
        if Vehiculo.verificar_velocidad and Vehiculo.verificar_capacidad and Vehiculo.verificar_costo_fijo and Vehiculo.verificar_costo_por_km and Vehiculo.verificar_costo_por_kg:
            self.modo=modo
            self.velocidad_kmh=velocidad_kmh
            self.capacidad_kg=capacidad_kg
            self.costo_fijo=costo_fijo
            self.costo_por_km=costo_por_km
            self.costo_por_kg=costo_por_kg
    def __str__(self):
        return f"Modo: {self.modo}, Velocidad: {self.velocidad_kmh} km/h, Capacidad: {self.capacidad_kg} kg, Costo Fijo: ${self.costo_fijo}, Costo por km: ${self.costo_por_km}, Costo por kg: ${self.costo_por_kg}"
    @staticmethod
    def verificar_modo(modo:str):
        if modo not in ["Automotor", "Ferrocarril", "Aereo", "Maritimo"]:
            raise ValueError("Modo de transporte no válido")
        return modo
    @staticmethod
    def verificar_velocidad(velocidad:float):
        if velocidad <= 0:
            raise ValueError("La velocidad debe ser mayor a 0")
        return velocidad
    @staticmethod
    def verificar_capacidad(capacidad:float):
        if capacidad <= 0:
            raise ValueError("La capacidad debe ser mayor a 0")
        return capacidad
    @staticmethod
    def verificar_costo_fijo(costo_fijo:float):
        if costo_fijo < 0:
            raise ValueError("El costo fijo no puede ser negativo")
        return costo_fijo
    @staticmethod
    def verificar_costo_por_km(costo_por_km:float):
        if costo_por_km < 0:
            raise ValueError("El costo por km no puede ser negativo")
        return costo_por_km
    @staticmethod
    def verificar_costo_por_kg(costo_por_kg:float):
        if costo_por_kg < 0:
            raise ValueError("El costo por kg no puede ser negativo")
        return costo_por_kg
    @staticmethod
class Camion(Vehiculo):
    def __init__(self,costo_por_kg:float):
        super().__init__("Automotor",80,30000,30,5,costo_por_kg)
    
class Tren(Vehiculo):
    def __init__(self,costo_por_km:float):
        super().__init__("Ferrocarril",100,150000,100,costo_por_km,3)

class Avion(Vehiculo):
    def __init__(self,velocidad_kmh:float):
       super().__init__("Aereo",velocidad_kmh,5000,750,40,10) 

class Barco(Vehiculo):
    def __init__(self,costo_fijo:float):
        super().__init__("Maritimo",40,100000,costo_fijo,15,2)
    