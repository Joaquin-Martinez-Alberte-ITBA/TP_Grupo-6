import tkinter as tk
from tkinter import messagebox
from nodo import Nodo, cargar_nodos_desde_csv
from conexion import crear_conexiones_desde_csv, Conexion
from tramo import procesar_tramos, tramos_guardados
from kpi import obtener_ruta_optima
from graficos import graficar_itinerario   

def cargar_datos():
    try:
        cargar_nodos_desde_csv("nodos.csv")
        crear_conexiones_desde_csv("conexiones.csv", Nodo.nodos_registrados)
        messagebox.showinfo("Datos cargados", "Los datos fueron cargados exitosamente.")
    except Exception as e:
        messagebox.showerror("Error al cargar datos", str(e))

def procesar_y_mostrar():
    if not Nodo.nodos_registrados or not Conexion.conexiones_registradas:
        if not messagebox.askyesno("Datos no cargados", "¿Deseás cargar los datos ahora?"):
            return
        cargar_datos()
    
    procesar_tramos()
    output = obtener_ruta_optima(tramos_guardados)
    mostrar_output(output)
    graficar_itinerario(tramos_guardados)    

def mostrar_output(texto):
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, texto)

app = tk.Tk()
app.title("Gestión de Envíos")

frame = tk.Frame(app, padx=20, pady=20)
frame.pack()

tk.Label(frame, text="Sistema de Envíos de Cargas", font=("Arial", 16)).pack(pady=10)

tk.Button(frame, text="Cargar datos", command=cargar_datos, width=30).pack(pady=5)
tk.Button(frame, text="Procesar solicitudes y mostrar KPIs", command=procesar_y_mostrar, width=30).pack(pady=5)

output_text = tk.Text(app, height=20, width=80)
output_text.pack(padx=20, pady=10)

app.mainloop()
