import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from AlgoritmoGenetico import AlgoritmoGenetico
from Hormiga import HormigaGenetica
from datetime import datetime
from estadisticas import mostrar_estadisticas

class SimulacionHormiga:
    """
    Clase que maneja la interfaz gráfica y la lógica de la simulación de la hormiga .
    """

    def __init__(self, master):
        """
        Inicializa la simulación configurando la ventana principal y variables iniciales.
        La ventana principal de la aplicación.
        """
        self.master = master
        self.master.title("Simulación de Hormiga Genética")
        
        self.tamaño = tk.IntVar(value=10)  # Tamaño inicial del laberinto
        self.herramienta_actual = 'A'  # Herramienta seleccionada (por defecto, Azúcar)
        self.tamaño_celda = 40  # Tamaño de cada celda en el laberinto
        self.laberinto = None  # Inicializa el laberinto
        self.algoritmo_genetico = AlgoritmoGenetico()  # Instancia del algoritmo genético
        self.pos_meta = None  # Posición de la meta en el laberinto
        self.tiempo_limite = 300  # Tiempo límite para la simulación (en segundos)
        
        self.crear_interfaz()  # Crea la interfaz gráfica

    def crear_interfaz(self):
        """
        Crea los componentes visuales de la interfaz de usuario.
        """
        self.frame_principal = ttk.Frame(self.master)
        self.frame_principal.pack(padx=10, pady=10)
        
        self.frame_config = ttk.LabelFrame(self.frame_principal, text="Configuración")
        self.frame_config.pack(side=tk.LEFT, padx=5, pady=5)
        
        ttk.Label(self.frame_config, text="Tamaño del laberinto:").pack()
        self.label_tamaño = ttk.Label(self.frame_config, text=f"Tamaño actual: {self.tamaño.get()}x{self.tamaño.get()}")
        self.label_tamaño.pack()
        
        # Control deslizante para ajustar el tamaño del laberinto
        self.tamaño_scale = ttk.Scale(self.frame_config, from_=3, to=10, 
                                       variable=self.tamaño, orient=tk.HORIZONTAL,
                                       command=self.actualizar_tamaño)
        self.tamaño_scale.pack(padx=5, pady=5)
        
        # Herramientas para colocar elementos en el laberinto
        self.frame_herramientas = ttk.LabelFrame(self.frame_config, text="Herramientas")
        self.frame_herramientas.pack(padx=5, pady=5)
        
        herramientas = [
            ('A', 'Azúcar', 'azucar.png'),
            ('V', 'Vino', 'vino.png'),
            ('X', 'Veneno', 'veneno.png'),
            ('R', 'Roca', 'piedra.png'),
            ('M', 'Meta', 'diamante.png'),
            ('.', 'Borrar', None)
        ]
        
        self.imagenes = {}  # Diccionario para almacenar las imágenes de los elementos
        for tipo, nombre, ruta_imagen in herramientas:
            if ruta_imagen:
                img = Image.open(ruta_imagen).resize((self.tamaño_celda, self.tamaño_celda), Image.LANCZOS)
                self.imagenes[tipo] = ImageTk.PhotoImage(img)  # Carga la imagen
            btn = ttk.Button(self.frame_herramientas, text=nombre,
                             command=lambda t=tipo: self.seleccionar_herramienta(t))
            btn.pack(pady=2)  # Botón para seleccionar la herramienta

        # Carga la imagen de la hormiga
        self.imagen_hormiga = ImageTk.PhotoImage(
            Image.open("hormiga.png").resize((self.tamaño_celda-10, self.tamaño_celda-10), Image.LANCZOS)
        )
        
        # Botones para crear el laberinto y comenzar la evolución
        ttk.Button(self.frame_config, text="Crear Laberinto",
                   command=self.crear_laberinto).pack(pady=5)
        ttk.Button(self.frame_config, text="Comenzar Evolución",
                   command=self.comenzar_evolucion).pack(pady=5)
        
        self.frame_laberinto = ttk.Frame(self.frame_principal)
        self.frame_laberinto.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.canvas = None  # Canvas donde se dibuja el laberinto
        
        self.etiqueta_generacion = ttk.Label(self.master, text="")
        self.etiqueta_generacion.pack(pady=5)
        self.etiqueta_estado = ttk.Label(self.master, text="")
        self.etiqueta_estado.pack(pady=5)
        
        # Instrucciones para el usuario
        self.frame_instrucciones = ttk.LabelFrame(self.frame_config, text="Instrucciones")
        self.frame_instrucciones.pack(padx=5, pady=5, fill='x')
        
        instrucciones_text = """
1. Selecciona el tamaño del laberinto
2. Haz clic en "Crear Laberinto"
3. Coloca los elementos:
   - Al menos una Meta (M)
   - Azúcar, Vino, Veneno y Rocas
4. Haz clic en "Comenzar Simulación"
"""
        ttk.Label(self.frame_instrucciones, text=instrucciones_text, justify='left').pack(padx=5, pady=5)
        
        self.label_estado = ttk.Label(self.master, text="¡Primero crea un laberinto!")
        self.label_estado.pack(pady=5)

    def actualizar_tamaño(self, valor):
        """
        Actualiza el tamaño del laberinto y redibuja.
        valor: Nuevo valor del tamaño del laberinto.
        """
        nuevo_tamaño = int(float(valor))
        self.label_tamaño.config(text=f"Tamaño actual: {nuevo_tamaño}x{nuevo_tamaño}")
        self.tamaño.set(nuevo_tamaño)
        self.laberinto = None  # Reinicia el laberinto
        self.pos_meta = None  # Reinicia la posición de la meta
        self.crear_laberinto()  # Crea un nuevo laberinto

    def seleccionar_herramienta(self, tipo):
        """
        Selecciona la herramienta actual para colocar en el laberinto.
        Tipo de herramienta seleccionada.
        """
        self.herramienta_actual = tipo

    def crear_laberinto(self):
        """
        Crea un nuevo laberinto basado en el tamaño seleccionado.
        """
        if self.canvas:
            self.canvas.destroy()  # Elimina el canvas anterior si existe
            
        tamaño = self.tamaño.get()
        tamaño_canvas = self.tamaño_celda * tamaño
        
        self.canvas = tk.Canvas(self.frame_laberinto, 
                                width=tamaño_canvas, height=tamaño_canvas)
        self.canvas.pack()
        
        # Inicializa el laberinto como una matriz de caracteres
        self.laberinto = [['.'] * tamaño for _ in range(tamaño)]
        self.pos_meta = None  # Reinicia la posición de la meta
        self.dibujar_laberinto()  # Dibuja el laberinto inicial
        
        self.canvas.bind('<Button-1>', self.colocar_item)  # Evento para colocar elementos
        
        # Actualizar el estado
        self.label_estado.config(text="Coloca una meta y otros elementos en el laberinto")

    def colocar_item(self, event):
        """
        Coloca un elemento en el laberinto en la posición donde se hace clic.
        Evento que contiene la posición del clic.
        """
        if not self.laberinto:
            return
            
        x = event.x // self.tamaño_celda  # Calcula la posición en la cuadrícula
        y = event.y // self.tamaño_celda
        
        # Si es una meta, actualizar pos_meta
        if self.herramienta_actual == 'M':
            if self.pos_meta:  # Elimina la meta anterior si existe
                self.laberinto[self.pos_meta[0]][self.pos_meta[1]] = '.'
            self.pos_meta = (y, x)  # Actualiza la posición de la meta
            self.label_estado.config(text="Meta colocada - Añade otros elementos al laberinto")
        
        self.laberinto[y][x] = self.herramienta_actual  # Coloca el elemento en el laberinto
        self.dibujar_laberinto()  # Redibuja el laberinto

    def dibujar_laberinto(self):
        """
        Dibuja el laberinto en el canvas.
        """
        if not self.canvas:
            return
            
        self.canvas.delete("all")  # Limpia el canvas antes de redibujar
        for i in range(len(self.laberinto)):
            for j in range(len(self.laberinto)):
                x = j * self.tamaño_celda
                y = i * self.tamaño_celda
                tipo = self.laberinto[i][j]
                
                # Dibuja el fondo del laberinto
                self.canvas.create_rectangle(x, y, x+self.tamaño_celda, y+self.tamaño_celda,
                                              fill='beige', outline='black')
                
                # Dibuja los elementos del laberinto
                if tipo in self.imagenes:
                    self.canvas.create_image(x, y, anchor='nw', image=self.imagenes[tipo])
        
        # Dibuja la hormiga si está viva
        if (hasattr(self, 'algoritmo_genetico') and 
            self.algoritmo_genetico.hormiga_actual and 
            self.algoritmo_genetico.hormiga_actual.viva):
            hormiga = self.algoritmo_genetico.hormiga_actual
            x = hormiga.y * self.tamaño_celda
            y = hormiga.x * self.tamaño_celda
            self.canvas.create_image(x+5, y+5, anchor='nw', image=self.imagen_hormiga)

    def comenzar_evolucion(self):
        """
        Inicia el proceso de evolución de la hormiga.
        """
        # Validar que existe el laberinto
        if not self.laberinto:
            messagebox.showwarning("Error", "Primero crea el laberinto")
            return
        
        # Validar que existe una meta
        tiene_meta = False
        for fila in self.laberinto:
            if 'M' in fila:
                tiene_meta = True
                break
        
        if not tiene_meta:
            messagebox.showwarning("Error", "Debes colocar una meta (M) en el laberinto")
            return
        
        self.algoritmo_genetico.inicializar()  # Inicializa el algoritmo genético
        self.evolucionar()  # Comienza el proceso de evolución

    def evolucionar(self):
        """
        Realiza una iteración de evolución para la hormiga.
        """
        hormiga = self.algoritmo_genetico.hormiga_actual
        tiempo_actual = (datetime.now() - self.algoritmo_genetico.tiempo_inicio).total_seconds()
        
        if tiempo_actual > self.tiempo_limite:
            messagebox.showinfo("Fin", "Tiempo límite alcanzado")
            mostrar_estadisticas(self.algoritmo_genetico.archivo_stats)  # Muestra estadísticas al finalizar
            return
        
        if hormiga.viva and hormiga.pasos < hormiga.pasos_maximos:
            if hormiga.mover(self.laberinto):  # Mueve la hormiga en el laberinto
                if hormiga.llego_meta:
                    hormiga.calcular_aptitud(self.pos_meta)  # Calcula la aptitud si llegó a la meta
                    self.algoritmo_genetico.evolucionar()  # Evoluciona a la siguiente hormiga
                    messagebox.showinfo("¡Éxito!", 
                                    f"¡Hormiga llegó a la meta!\nGeneración: {self.algoritmo_genetico.generacion}\n"
                                    f"Puntos: {hormiga.puntos}\nAlcohol: {hormiga.alcohol}")
                    mostrar_estadisticas(self.algoritmo_genetico.archivo_stats)  # Muestra estadísticas al llegar a la meta
                    return
                hormiga.calcular_aptitud(self.pos_meta)  # Calcula la aptitud aunque no haya llegado a la meta
            else:
                self.algoritmo_genetico.evolucionar()  # Evoluciona si no pudo moverse
                
        self.dibujar_laberinto()  # Redibuja el laberinto
        
        # Actualiza las etiquetas con información actual de la generación y estado
        self.etiqueta_generacion.config(
            text=f"Generación: {self.algoritmo_genetico.generacion}")
        self.etiqueta_estado.config(
            text=f"Puntos: {hormiga.puntos} | Alcohol: {hormiga.alcohol} | "
                f"Aptitud: {hormiga.aptitud:.2f}")
        
        self.master.after(50, self.evolucionar)  # Repite el proceso cada 50 ms


if __name__ == "__main__":
    root = tk.Tk()  # Crea la ventana principal
    app = SimulacionHormiga(root)  # Inicia la simulación de la hormiga
    root.mainloop()  # Mantiene la aplicación corriendo
