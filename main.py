import tkinter as tk
from tkinter import messagebox
from nodo import Nodo, cargar_nodos_desde_csv
from conexion import crear_conexiones_desde_csv, Conexion
from tramo import procesar_tramos
from kpi import imprimir_ruta_optima

# Estado interno para saber si los datos fueron cargados
datos_cargados = {"estado": False}

def cargar_datos():
    try:
        cargar_nodos_desde_csv("nodos.csv")
        crear_conexiones_desde_csv("conexiones.csv", Nodo.nodos_registrados)
        datos_cargados["estado"] = True
        messagebox.showinfo("Éxito", "Datos cargados correctamente.")
    except Exception as e:
        messagebox.showerror("Error al cargar datos", str(e))

def mostrar_nodos():
    if not Nodo.nodos_registrados:
        messagebox.showwarning("Aviso", "Primero cargá los datos.")
        return
    nodos = "\n".join([str(nodo) for nodo in Nodo.nodos_registrados.values()])
    messagebox.showinfo("Nodos registrados", nodos)

def mostrar_conexiones():
    if not Conexion.conexiones_registradas:
        messagebox.showwarning("Aviso", "Primero cargá los datos.")
        return
    conexiones = ""
    for origen, destinos in Conexion.conexiones_registradas.items():
        for destino, tipos in destinos.items():
            for tipo, conexion in tipos.items():
                conexiones += f"{conexion}\n"
    messagebox.showinfo("Conexiones registradas", conexiones)

def procesar_solicitudes():
    if not datos_cargados["estado"]:
        respuesta = messagebox.askyesno(
            "Datos no cargados",
            "¿Deseás cargar los datos antes de procesar solicitudes?"
        )
        if respuesta:
            cargar_datos()
        else:
            messagebox.showwarning("Proceso detenido", "No se puede continuar sin datos.")
            return
    try:
        procesar_tramos()
        imprimir_ruta_optima()
        messagebox.showinfo("Listo", "Procesamiento completado con éxito.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def interfaz_principal():
    ventana = tk.Tk()
    ventana.title("Sistema de Transporte de Cargas")
    ventana.geometry("400x300")

    tk.Label(ventana, text="Menú Principal", font=("Arial", 16)).pack(pady=10)

    tk.Button(ventana, text="Cargar datos", command=cargar_datos, width=30).pack(pady=5)
    tk.Button(ventana, text="Ver nodos", command=mostrar_nodos, width=30).pack(pady=5)
    tk.Button(ventana, text="Ver conexiones", command=mostrar_conexiones, width=30).pack(pady=5)
    tk.Button(ventana, text="Procesar solicitudes", command=procesar_solicitudes, width=30).pack(pady=5)
    tk.Button(ventana, text="Salir", command=ventana.quit, width=30).pack(pady=20)

    ventana.mainloop()

if __name__ == "__main__":
    interfaz_principal()

