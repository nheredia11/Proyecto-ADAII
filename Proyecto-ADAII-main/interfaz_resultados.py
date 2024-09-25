import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from proyectoADAII import read_input, modexV, modexPD, modexFB

class AlgoritmosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interfaz de Algoritmos")
        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=10)

        # Frame para archivo de entrada y resultados
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, padx=10)

        # Frame para gráficos
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, padx=10)

        # Botón para cargar el archivo de entrada
        self.load_button = tk.Button(left_frame, text="Cargar archivo de entrada", command=self.load_input_file)
        self.load_button.pack(pady=10)

        # Área de texto para mostrar el contenido del archivo de entrada
        self.file_content_text = tk.Text(left_frame, wrap=tk.WORD, height=10, width=50)
        self.file_content_text.pack(pady=10)
        self.file_content_text.insert(tk.END, "Contenido del archivo cargado aparecerá aquí...\n")

        # Área de texto para mostrar los resultados
        self.result_text = tk.Text(left_frame, wrap=tk.WORD, height=10, width=50)
        self.result_text.pack(pady=10)
        self.result_text.insert(tk.END, "Resultados de los algoritmos aparecerán aquí...\n")

        # Botones para ejecutar los algoritmos
        self.run_voraz_button = tk.Button(left_frame, text="Ejecutar Algoritmo Voraz", command=self.run_voraz)
        self.run_voraz_button.pack(pady=5)

        self.run_pd_button = tk.Button(left_frame, text="Ejecutar Algoritmo PD", command=self.run_pd)
        self.run_pd_button.pack(pady=5)

        self.run_fb_button = tk.Button(left_frame, text="Ejecutar Algoritmo Fuerza Bruta", command=self.run_fb)
        self.run_fb_button.pack(pady=5)

        # Área para gráficos
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.plot_area = FigureCanvasTkAgg(self.figure, right_frame)
        self.plot_area.get_tk_widget().pack(pady=10)

    def load_input_file(self):
        self.file_path = filedialog.askopenfilename(title="Selecciona archivo de entrada", filetypes=[("Text files", "*.txt")])
        if not self.file_path:
            messagebox.showerror("Error", "No se ha seleccionado ningún archivo")
            return
        
        # Mostrar el contenido del archivo en el área de texto
        self.file_content_text.delete(1.0, tk.END)
        try:
            with open(self.file_path, 'r') as file:
                file_content = file.read()
                self.file_content_text.insert(tk.END, file_content)
        except Exception as e:
            self.file_content_text.insert(tk.END, f"Error al leer el archivo: {str(e)}")
        
        # Limpiar resultados previos
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Archivo cargado: {self.file_path}\n")

    def run_voraz(self):
        if not hasattr(self, 'file_path'):
            messagebox.showerror("Error", "Primero debes cargar un archivo de entrada")
            return
        agents, Rmax = read_input(self.file_path)
        best_strategy, total_effort, final_extremism = modexV(agents, Rmax)
        self.show_results("Algoritmo Voraz", best_strategy, total_effort, final_extremism)
    
    def run_pd(self):
        if not hasattr(self, 'file_path'):
            messagebox.showerror("Error", "Primero debes cargar un archivo de entrada")
            return
        agents, Rmax = read_input(self.file_path)
        best_strategy, total_effort, final_extremism = modexPD(agents, Rmax)
        self.show_results("Algoritmo PD", best_strategy, total_effort, final_extremism)

    def run_fb(self):
        if not hasattr(self, 'file_path'):
            messagebox.showerror("Error", "Primero debes cargar un archivo de entrada")
            return
        agents, Rmax = read_input(self.file_path)
        best_strategy, total_effort, final_extremism = modexFB(agents, Rmax)
        self.show_results("Algoritmo Fuerza Bruta", best_strategy, total_effort, final_extremism)

    def show_results(self, algorithm_name, strategy, total_effort, final_extremism):
        # Mostrar los resultados en el área de texto
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"=== {algorithm_name} ===\n")
        self.result_text.insert(tk.END, f"Estrategia seleccionada: {strategy}\n")
        self.result_text.insert(tk.END, f"Esfuerzo total: {total_effort}\n")
        self.result_text.insert(tk.END, f"Extremismo final: {final_extremism}\n")

        # Crear el gráfico
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.bar(range(len(strategy)), strategy)
        ax.set_title(f"Estrategia {algorithm_name}")
        ax.set_xlabel("Agente")
        ax.set_ylabel("Seleccionado (1) o No (0)")
        self.plot_area.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = AlgoritmosApp(root)
    root.mainloop()

"""
El gráfico generado por el siguiente código:
es un gráfico de barras que representa visualmente la estrategia seleccionada para un conjunto de agentes. 

### Interpretación del gráfico para la salida:


Estrategia seleccionada: [1, 0, 1, 1, 0]
Esfuerzo total: 86
Extremismo final: 21.557365330670628


#### Ejes:
- Eje X (Agente): Representa a los diferentes agentes en el problema. Cada valor en el eje X corresponde a un agente numerado secuencialmente (agente 0, agente 1, agente 2, etc.). En este caso, como la estrategia tiene una longitud de 5, habrá 5 barras correspondientes a los 5 agentes.
  
- Eje Y (Seleccionado (1) o No (0)): Muestra si cada agente fue seleccionado (valor 1) o no (valor 0) en la estrategia propuesta. Si la barra está en 1, el agente fue seleccionado para alguna acción (como ser moderado, influenciado, etc.). Si la barra está en 0, significa que el agente no fue seleccionado.

#### Barras:
- Cada barra corresponde a un agente, y su altura es 1 si el agente fue seleccionado (según la estrategia) o 0 si no lo fue.
- Para la estrategia [1, 0, 1, 1, 0], el gráfico mostrará lo siguiente:
  - Agente 0: Seleccionado (barra de altura 1)
  - Agente 1: No seleccionado (barra de altura 0)
  - Agente 2: Seleccionado (barra de altura 1)
  - Agente 3: Seleccionado (barra de altura 1)
  - Agente 4: No seleccionado (barra de altura 0)

### Interpretación Completa:
- El gráfico muestra claramente qué agentes fueron seleccionados o no en función de la estrategia. En este caso:
  - Agentes 0, 2 y 3 fueron seleccionados.
  - Agentes 1 y 4 no fueron seleccionados.
  
Este gráfico es útil para visualizar de manera rápida qué agentes están involucrados en la solución, ayudando a evaluar la estrategia.

En cuanto a los demás datos:
- Esfuerzo total: 86 unidades de esfuerzo fueron necesarias para implementar esta estrategia.
- Extremismo final: El nivel de extremismo final de los agentes, después de aplicar la estrategia, es 21.56. Esto indica qué tan "extremos" permanecen los agentes después de que algunos de ellos fueron moderados.

El gráfico en sí no muestra el esfuerzo total ni el extremismo final, pero es una representación visual de la estrategia aplicada a los agentes.
"""