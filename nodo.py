class Nodo():
    nodos_registrados = {}
    def __init__(self, nombre_ciudad, soporte_conexiones = []):
        if nombre_ciudad in Nodo.nodos_registrados:
            raise ValueError(f"El nodo {nombre_ciudad} ya está registrado.")
        elif not isinstance(nombre_ciudad, str):
            raise TypeError("El nombre de la ciudad debe ser una cadena de texto.")
        self.nombre_ciudad = nombre_ciudad
        self.modo_transporte = []
        self.soporte_conexiones = soporte_conexiones
        Nodo.nodos_registrados[nombre_ciudad] = self
    
    def __str__(self):
        return f"Ciudad: {self.nombre_ciudad}, Rol: {self.rol_nodo}, Modo de Transporte: {self.modo_transporte}, Soporte Conexiones: {self.soporte_conexiones}"
    
    def agregar_modo_transporte(self, modo):
        if modo not in self.modo_transporte:
            self.modo_transporte.append(modo)
        else:
            raise ValueError(f"El modo de transporte {modo} ya está registrado en {self.nombre_ciudad}.")
    
    def eliminar_modo_transporte(self, modo):
        if modo in self.modo_transporte:
            self.modo_transporte.pop(modo)
        else:
            raise ValueError(f"El modo de transporte {modo} no está registrado en {self.nombre_ciudad}.")
    