import tkinter as tk
from tkinter import messagebox, filedialog
from nodo import Nodo, cargar_nodos_desde_csv
from conexion import crear_conexiones_desde_csv, Conexion
from tramo import procesar_todas_las_solicitudes, Planificador
from graficos import graficar_itinerario_por_carga, plt

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gestión de Envíos")
        self.indice_actual = 0
        self.planificadores = []
        self.figura_actual = None 

        self.configurar_interfaz()
        self.bloquear_botones(inicial=True)

    def configurar_interfaz(self):
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack()

        tk.Label(frame, text="Sistema de Envíos de Cargas", font=("Arial", 16)).pack(pady=10)

        self.btn_cargar = tk.Button(frame, text="Cargar datos", command=self.cargar_datos, width=30)
        self.btn_cargar.pack(pady=5)

        self.btn_procesar = tk.Button(frame, text="Procesar solicitudes", command=self.procesar_datos, width=30)
        self.btn_procesar.pack(pady=5)

        self.btn_siguiente = tk.Button(frame, text="Siguiente solicitud", command=self.mostrar_siguiente, width=30)
        self.btn_siguiente.pack(pady=5)

        self.btn_guardar = tk.Button(frame, text="Guardar gráfico actual", command=self.guardar_grafico, width=30)
        self.btn_guardar.pack(pady=5)

        self.output_text = tk.Text(self.root, height=20, width=80)
        self.output_text.pack(padx=20, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_app)

    def bloquear_botones(self, inicial=False):
        self.btn_procesar.config(state="disabled" if inicial else "normal")
        self.btn_siguiente.config(state="disabled")
        self.btn_guardar.config(state="disabled")

    def cargar_datos(self):
        try:
            cargar_nodos_desde_csv("nodos.csv")
            crear_conexiones_desde_csv("conexiones.csv", Nodo.nodos_registrados)
            messagebox.showinfo("Datos cargados", "Los datos fueron cargados exitosamente.")
            self.btn_procesar.config(state="normal")
        except Exception as e:
            messagebox.showerror("Error al cargar datos", str(e))

    def procesar_datos(self):
        if not Nodo.nodos_registrados or not Conexion.conexiones_registradas:
            if not messagebox.askyesno("Datos no cargados", "¿Deseas cargar los datos ahora?"):
                return
            self.cargar_datos()

        self.planificadores = procesar_todas_las_solicitudes()
        self.indice_actual = 0

        if not self.planificadores:
            messagebox.showinfo("Sin solicitudes", "No hay solicitudes válidas para procesar.")
            self.bloquear_botones(inicial=True)
            return

        self.btn_siguiente.config(state="normal")
        self.mostrar_siguiente()

    def mostrar_siguiente(self):
        if self.indice_actual >= len(self.planificadores):
            messagebox.showinfo("Fin", "Ya se mostraron todas las solicitudes.")
            self.btn_siguiente.config(state="disabled")
            return
        if self.figura_actual:
            plt.close(self.figura_actual)
            self.figura_actual = None

        planificador = self.planificadores[self.indice_actual]
        tramos_texto = planificador.obtener_todos_los_tramos_formateados()
        resultado_kpi = planificador.obtener_kpi()

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, tramos_texto + resultado_kpi)

        if planificador.tramos_por_tipo:
            self.figura_actual = graficar_itinerario_por_carga(planificador.tramos_por_tipo, planificador.id_carga)
            self.btn_guardar.config(state="normal")

        self.indice_actual += 1

    def guardar_grafico(self):
        if self.figura_actual:
            archivo = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if archivo:
                self.figura_actual.savefig(archivo)
                messagebox.showinfo("Guardado", f"Gráfico guardado en:\n{archivo}")

    def cerrar_app(self):
        if self.figura_actual:
            plt.close(self.figura_actual)
        self.root.destroy()

    def ejecutar(self):
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = App()
        app.ejecutar()
    except Exception as e:
        print(f"Error en la ejecución del programa: {e}")
