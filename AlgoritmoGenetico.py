# Importamos a ramdom 
# Importamos a datetime
# Importamos a numpy 
# Llamamos al  Registro.py
# Llamamos a la Hormiga.py 

import random
from datetime import datetime
from typing import List
import numpy as np
from Registro import RegistroGeneracion
from Hormiga import HormigaGenetica

class AlgoritmoGenetico:
    """
    Clase que representa un algoritmo genético para la evolución de una hormiga genética.
    """

    def __init__(self):
        """
        Inicializa el algoritmo genético con los atributos necesarios.
        """
        self.hormiga_actual = None  # Hormiga en la generación actual
        self.mejor_hormiga = None    # Mejor hormiga encontrada hasta el momento
        self.generacion = 0          # Contador de generaciones
        self.tasa_mutacion = 0.1     # Tasa de mutación de los genes
        self.registros: List[RegistroGeneracion] = []  # Lista de registros de generaciones
        self.tiempo_inicio = datetime.now()  # Marca de tiempo de inicio
        self.archivo_stats = f'estadisticas_hormiga.txt'  # Archivo para almacenar estadísticas

    def inicializar(self):
        """
        Inicializa los parámetros del algoritmo genético y prepara el archivo de estadísticas.
        """
        self.hormiga_actual = HormigaGenetica(0, 0)  # Crea la hormiga inicial
        self.generacion = 0  # Reinicia el contador de generaciones
        self.tiempo_inicio = datetime.now()  # Reinicia el tiempo de inicio
        self.registros = []  # Reinicia la lista de registros
        
        # Abre el archivo de estadísticas para escritura y agrega un encabezado
        with open(self.archivo_stats, 'w', encoding='utf-8') as f:
            f.write(f"=== Estadísticas de Simulación - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n\n")

    def mutar(self, genes: np.ndarray) -> np.ndarray:
        """
        Aplica mutaciones a los genes de la hormiga actual según la tasa de mutación.
        Nuevos genes después de aplicar mutaciones.
        """
        nuevos_genes = genes.copy()  # Copia los genes actuales para mutar
        for i in range(len(nuevos_genes)):
            if random.random() < self.tasa_mutacion:  # Determina si se aplica mutación
                nuevos_genes[i] = random.randint(0, 3)  # Mutación aleatoria de los genes
        return nuevos_genes

    def evolucionar(self):
        """
        Realiza una evolución del algoritmo genético, creando una nueva hormiga basada
        en la mejor hormiga actual y aplicando mutaciones.
        """
        tiempo_total = (datetime.now() - self.tiempo_inicio).total_seconds()  # Tiempo total transcurrido
        registro = RegistroGeneracion(
            self.generacion,
            self.hormiga_actual.pasos,
            self.hormiga_actual.puntos,
            self.hormiga_actual.alcohol,
            self.hormiga_actual.llego_meta,
            tiempo_total
        )  # Crea un registro de la generación actual
        self.registros.append(registro)  # Agrega el registro a la lista

        # Actualiza la mejor hormiga si la actual tiene mejor aptitud
        if (not self.mejor_hormiga or 
            self.hormiga_actual.aptitud > self.mejor_hormiga.aptitud):
            self.mejor_hormiga = HormigaGenetica(0, 0)  # Crea una nueva mejor hormiga
            self.mejor_hormiga.genes = self.hormiga_actual.genes.copy()  # Copia los genes
            self.mejor_hormiga.aptitud = self.hormiga_actual.aptitud  # Actualiza la aptitud

        # Crea una nueva hormiga basada en la mejor hormiga y muta sus genes
        nueva_hormiga = HormigaGenetica(0, 0)
        nueva_hormiga.genes = self.mutar(self.mejor_hormiga.genes)
        
        self.hormiga_actual = nueva_hormiga  # Actualiza la hormiga actual
        self.generacion += 1  # Incrementa el contador de generaciones

        self.guardar_estadisticas(registro)  # Guarda las estadísticas de la generación

    def guardar_estadisticas(self, registro: RegistroGeneracion):
        """
        Guarda las estadísticas de la generación actual en un archivo.

        Args:
            registro (RegistroGeneracion): Registro que contiene la información de la generación.
        """
        with open(self.archivo_stats, 'a', encoding='utf-8') as f:
            f.write("\n" + "="*50 + "\n\n")  # Separador en el archivo
            f.write(registro.to_string())  # Escribe el registro en el archivo
