# Importación de librerías necesarias
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
"""matplotlib.pyplot y FigureCanvasTkAgg: 
Estos módulos de Matplotlib nos permiten crear gráficos y visualizarlos en la interfaz gráfica de Tkinter."""
import tkinter as tk
from tkinter import ttk
import numpy as np
"""numpy: Numpy es una biblioteca para cálculos matemáticos en Python. 
Aquí la usamos para obtener estadísticas como la media de los datos."""
from typing import List
from datetime import datetime
"""typing.List y datetime: List permite especificar tipos de datos en listas. 
datetime ayuda a manejar fechas y horas para guardar archivos con marcas de tiempo"""

# Clase que representa la ventana de estadísticas
class VentanaEstadisticas:
    def __init__(self, archivo: str):
        """
        Inicializa la ventana de estadísticas, se configura la interfaz gráfica,
        y procesa el archivo de estadísticas para mostrar los datos.
        
        esto en base al archivo estadisticas_hormiga.txt
        """
        
        # Crear una ventana secundaria para mostrar las estadísticas
        self.ventana = tk.Toplevel()
        self.ventana.title("Estadísticas de la Simulación")
        self.ventana.geometry("1200x800")
        
        # Crear el frame principal donde se colocarán otros elementos
        self.frame_principal = ttk.Frame(self.ventana)
        self.frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame para los gráficos, se expandirá para ocupar el espacio disponible
        self.frame_graficos = ttk.Frame(self.frame_principal)
        self.frame_graficos.pack(fill=tk.BOTH, expand=True)
        
        # Frame para el resumen de estadísticas
        self.frame_resumen = ttk.LabelFrame(self.frame_principal, text="Resumen de Estadísticas")
        self.frame_resumen.pack(fill=tk.X, pady=(10, 0))
        
        # Llamada al método que procesa el archivo y genera los gráficos y resumen
        self.procesar_estadisticas(archivo)
        
    def procesar_estadisticas(self, archivo: str):
        """
        Procesa el archivo de estadísticas y muestra los gráficos y el resumen de datos.
        
        :param archivo: Ruta del archivo que contiene los datos de la simulación
        """
        try:
            # Inicialización de listas para almacenar los datos de cada métrica
            generaciones, puntos, tiempos = [], [], []
            alcoholes, pasos, llegadas_meta = [], [], []
            
            # Leer el archivo línea por línea
            with open(archivo, 'r', encoding='utf-8') as f:
                lineas = f.readlines()
                
            gen_actual = None  # Variable auxiliar para almacenar la generación actual
            
            # Procesar cada línea del archivo
            for linea in lineas:
                linea = linea.strip()  # Quitar espacios en blanco y saltos de línea
                if linea.startswith('Generación:'):
                    gen_actual = int(linea.split(':')[1])
                    generaciones.append(gen_actual)
                elif linea.startswith('Puntos:'):
                    puntos.append(int(linea.split(':')[1]))
                elif linea.startswith('Tiempo total:'):
                    tiempos.append(float(linea.split(':')[1].split()[0]))
                elif linea.startswith('Alcohol:'):
                    alcoholes.append(int(linea.split(':')[1]))
                elif linea.startswith('Pasos:'):
                    pasos.append(int(linea.split(':')[1]))
                elif linea.startswith('Llegó a la meta:'):
                    llegadas_meta.append(1 if 'Sí' in linea else 0)
                    
                    """Según el prefijo de cada línea (Generación, Puntos, etc.), 
                    se extrae la información correspondiente y se almacena en la lista adecuada.
                    Por ejemplo, si una línea comienza con Generación:, 
                    se extrae el número de generación y se agrega a la lista generaciones."""
            
            # Crear una figura de matplotlib con 4 gráficos (subplots)
            fig = plt.Figure(figsize=(12, 8))
            
            # Definir cada subplot de la figura
            ax1 = fig.add_subplot(221)
            ax2 = fig.add_subplot(222)
            ax3 = fig.add_subplot(223)
            ax4 = fig.add_subplot(224)
            
            # 1. Gráfico de puntos por generación
            ax1.plot(generaciones, puntos, 'b.-')
            ax1.set_title('Puntos por generación')
            ax1.set_xlabel('Generación')
            ax1.set_ylabel('Puntos')
            ax1.grid(True)
            
            # 2. Gráfico de tiempo por generación
            ax2.plot(generaciones, tiempos, 'r.-')
            ax2.set_title('Tiempo por generación')
            ax2.set_xlabel('Generación')
            ax2.set_ylabel('Tiempo (segundos)')
            ax2.grid(True)
            
            # 3. Gráfico de nivel de alcohol por generación
            ax3.plot(generaciones, alcoholes, 'g.-')
            ax3.set_title('Alcohol por generación')
            ax3.set_xlabel('Generación')
            ax3.set_ylabel('Nivel de alcohol')
            ax3.grid(True)
            
            # 4. Gráfico de pasos por generación
            ax4.plot(generaciones, pasos, 'm.-')
            ax4.set_title('Pasos por generación')
            ax4.set_xlabel('Generación')
            ax4.set_ylabel('Número de pasos')
            ax4.grid(True)
            
            #  el layout para que los gráficos no se superpongan
            fig.tight_layout()
            
            # Integrar la figura de matplotlib en el widget de Tkinter
            canvas = FigureCanvasTkAgg(fig, self.frame_graficos)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Crear un resumen estadístico en formato de texto
            resumen_texto = f"""
                Total de generaciones: {len(generaciones)}
                Puntuación máxima: {max(puntos)}
                Puntuación promedio: {np.mean(puntos):.2f}
                Tiempo total de simulación: {max(tiempos):.2f} segundos
                Promedio de pasos por generación: {np.mean(pasos):.2f}
                Veces que llegó a la meta: {sum(llegadas_meta)}
                Tasa de éxito: {(sum(llegadas_meta)/len(llegadas_meta)*100):.2f}%
                """
            # Mostrar el resumen en el frame de resumen
            ttk.Label(self.frame_resumen, text=resumen_texto, justify='left').pack(padx=10, pady=5)
            
            # Función para guardar los gráficos como imagen
            def guardar_graficas():
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                fig.savefig(f'estadisticas_hormiga_{timestamp}.png')
                
            # Botón para guardar los gráficos, usando la función anterior
            ttk.Button(self.frame_resumen, text="Guardar Gráficas", 
                       command=guardar_graficas).pack(pady=5)
            
        except Exception as e:
            # Mostrar mensaje de error si ocurre una excepción al procesar los datos
            ttk.Label(self.frame_resumen, 
                      text=f"Error al procesar las estadísticas: {str(e)}",
                      foreground='red').pack(padx=10, pady=5)

# Función para iniciar la ventana de estadísticas
def mostrar_estadisticas(archivo: str):
    """
    Función principal para mostrar la ventana de estadísticas.
    
    :param archivo: Ruta del archivo con los datos de la simulación.
    :return: Instancia de VentanaEstadisticas.
    """
    return VentanaEstadisticas(archivo)

# Bloque de ejecución principal para pruebas independientes
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal de Tkinter
    app = mostrar_estadisticas("estadisticas_hormiga.txt")
    root.mainloop()
