import tkinter as tk
from tkinter import messagebox
from nodo import Nodo, cargar_nodos_desde_csv
from conexion import crear_conexiones_desde_csv, Conexion
from tramo import procesar_tramos, tramos_guardados
from kpi import obtener_ruta_optima_por_solicitud
from graficos import graficar_itinerario_por_carga

indice_actual = 0
ids_carga = []

def cargar_datos():
    '''Carga los nodos y conexiones desde archivos CSV.'''
    try:
        cargar_nodos_desde_csv("nodos.csv")
        crear_conexiones_desde_csv("conexiones.csv", Nodo.nodos_registrados)
        messagebox.showinfo("Datos cargados", "Los datos fueron cargados exitosamente.")
    except Exception as e:
        messagebox.showerror("Error al cargar datos", str(e))

def procesar_datos():
    '''Procesa los tramos y prepara las solicitudes para su visualización.'''
    global ids_carga, indice_actual
    if not Nodo.nodos_registrados or not Conexion.conexiones_registradas:
        if not messagebox.askyesno("Datos no cargados", "¿Deseás cargar los datos ahora?"):
            return
        cargar_datos()
    procesar_tramos()
    ids_carga = list(tramos_guardados.keys())
    indice_actual = 0
    mostrar_siguiente()

def mostrar_siguiente():
    '''Muestra la siguiente solicitud de carga y su ruta óptima.'''
    global indice_actual
    if indice_actual >= len(ids_carga):
        messagebox.showinfo("Fin", "Ya se mostraron todas las solicitudes.")
        return

    id_actual = ids_carga[indice_actual]
    resultado = obtener_ruta_optima_por_solicitud(tramos_guardados, id_actual)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, resultado)
    graficar_itinerario_por_carga(tramos_guardados[id_actual], id_actual)
    indice_actual += 1

# Interfaz
app = tk.Tk()
app.title("Gestión de Envíos")

frame = tk.Frame(app, padx=20, pady=20)
frame.pack()

tk.Label(frame, text="Sistema de Envíos de Cargas", font=("Arial", 16)).pack(pady=10)
tk.Button(frame, text="Cargar datos", command=cargar_datos, width=30).pack(pady=5)
tk.Button(frame, text="Procesar solicitudes", command=procesar_datos, width=30).pack(pady=5)
tk.Button(frame, text="Siguiente solicitud", command=mostrar_siguiente, width=30).pack(pady=5)

output_text = tk.Text(app, height=20, width=80)
output_text.pack(padx=20, pady=10)

app.mainloop()