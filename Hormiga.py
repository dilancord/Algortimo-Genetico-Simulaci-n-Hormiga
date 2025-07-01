import numpy as np
from typing import Tuple, List

class HormigaGenetica:
    """
    Esta clase modela el comportamiento de una hormiga que navega en el laberinto
    

    Atributos:
    ----------
    x, y : int
        Posición actual de la hormiga en el laberinto.
    x_inicial, y_inicial : int
        Posición inicial de la hormiga en el laberinto.
    puntos : int
        Puntuación acumulada por la hormiga al recoger recursos.
    alcohol : int
        Nivel de alcohol acumulado, afecta la aptitud.
    aptitud : float
        Valor calculado que representa la capacidad de la hormiga en la simulación.
    viva : bool
        Estado de la hormiga, indica si está viva o ha "muerto".
    pasos : int
        Número de pasos realizados en esta generación.
    pasos_maximos : int
    
        Conjunto de genes que representan direcciones de movimiento.
    gen_actual : int
        Índice del gen que la hormiga está usando en su secuencia de movimientos.
    llego_meta : bool
        Indicador de si la hormiga ha alcanzado la meta.

    Métodos:
    --------
    reiniciar():
        Restaura todos los atributos a sus valores iniciales para una nueva simulación.
    calcular_aptitud(pos_meta: Tuple[int, int]) -> float:
        Calcula y retorna la aptitud de la hormiga basada en su desempeño.
    mover(laberinto: List[List[str]]) -> bool:
        Realiza un movimiento en el laberinto basado en el gen actual de la hormiga y 
        actualiza sus atributos según los recursos que encuentra o los obstáculos que enfrenta.
    """

    def __init__(self, x: int, y: int):
        """
        Inicializa una instancia de HormigaGenetica en una posición dada (x, y) en el laberinto.

        Parámetros:
        -----------
        x : int
            Coordenada horizontal inicial de la hormiga.
        y : int
            Coordenada vertical inicial de la hormiga.
        """
        self.x = x
        self.y = y
        self.x_inicial = x
        self.y_inicial = y
        self.puntos = 0
        self.alcohol = 0
        self.aptitud = 0
        self.viva = True
        self.pasos = 0
        self.pasos_maximos = 200
        self.genes = np.random.randint(0, 4, size=200)
        self.gen_actual = 0
        self.llego_meta = False

    def reiniciar(self):
        """
        Reinicia los atributos de la hormiga a sus valores iniciales,
        permitiendo que la hormiga participe en una nueva simulación.
        """
        self.x = self.x_inicial
        self.y = self.y_inicial
        self.puntos = 0
        self.alcohol = 0
        self.aptitud = 0
        self.viva = True
        self.pasos = 0
        self.gen_actual = 0
        self.llego_meta = False

    def calcular_aptitud(self, pos_meta: Tuple[int, int]) -> float:
        """
        Calcula la aptitud de la hormiga en función de su distancia a la meta,
        puntuación acumulada y nivel de alcohol.

        Parámetros:
        -----------
        pos_meta : Tuple[int, int]
            Posición de la meta en el laberinto (x, y).

        Retorna:
        --------
        float:
            Aptitud calculada de la hormiga, que refleja su desempeño.
        """
        # Calcular la distancia Manhattan a la meta
        distancia = abs(self.x - pos_meta[0]) + abs(self.y - pos_meta[1])
        # Penalización por el nivel de alcohol
        penalizacion_alcohol = self.alcohol * 5
        # Bonificación por los puntos acumulados
        bonificacion_puntos = self.puntos * 2
        # Aptitud inicial basada en distancia, puntos y alcohol
        self.aptitud = 1000 - distancia * 10 + bonificacion_puntos - penalizacion_alcohol

        # Bonificación adicional si llega a la meta
        if self.llego_meta:
            self.aptitud += 2000
            # Bonificación adicional si llega a la meta sin alcohol
            if self.alcohol == 0:
                self.aptitud += 1000
        elif not self.viva:
            # Penalización si la hormiga muere antes de llegar a la meta
            self.aptitud -= 500

        return self.aptitud

    def mover(self, laberinto: List[List[str]]) -> bool:
        """
        Realiza un movimiento basado en el gen actual de la hormiga y actualiza
        su posición y estado según el contenido de la nueva celda.

        Parámetros:
        -----------
        laberinto : List[List[str]]
            Matriz que representa el laberinto, donde cada celda puede ser:
            - 'A' para puntos, 
            - 'V' para alcohol,
            - 'X' para un obstáculo mortal,
            - 'M' para la meta,
            - 'R' para un obstáculo (pared),
            - '.' para una celda vacía.

        Retorna:
        --------
        bool:
            True si la hormiga se movió con éxito o sigue viva y en la simulación;
            False si la hormiga ha muerto o ha alcanzado el máximo de pasos.
        """
        # Verificar si la hormiga puede moverse
        if not self.viva or self.pasos >= self.pasos_maximos:
            return False

        # Definir movimientos posibles (derecha, abajo, izquierda, arriba)
        movimientos = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        # Determinar el movimiento según el gen actual
        movimiento_actual = self.genes[self.gen_actual]
        dx, dy = movimientos[movimiento_actual]

        # Calcular nueva posición
        nuevo_x = self.x + dx
        nuevo_y = self.y + dy

        # Comprobar si la nueva posición está dentro del laberinto y no es una pared
        if (0 <= nuevo_x < len(laberinto) and 
            0 <= nuevo_y < len(laberinto[0]) and 
            laberinto[nuevo_x][nuevo_y] != 'R'):
            
            # Actualizar la posición de la hormiga
            self.x, self.y = nuevo_x, nuevo_y
            # Obtener el tipo de celda en la nueva posición
            tipo = laberinto[nuevo_x][nuevo_y]
            
            # Actualizar los atributos en función de la celda visitada
            if tipo == 'A':
                self.puntos += 10
                laberinto[nuevo_x][nuevo_y] = '.'
            elif tipo == 'V':
                self.alcohol += 5
                laberinto[nuevo_x][nuevo_y] = '.'
            elif tipo == 'X':
                self.viva = False
                return False
            elif tipo == 'M':
                self.llego_meta = True
                self.puntos += 100
                return True

        # Incrementar el contador de pasos y avanzar al siguiente gen
        self.pasos += 1
        self.gen_actual = (self.gen_actual + 1) % len(self.genes)
        return True
