class RegistroGeneracion:
    """
    Clase para representar y almacenar los datos de una generación en la simulación.

    Atributos:
    ----------
    generacion : int
        Número identificador de la generación.
    pasos : int
        Número de pasos realizados en esta generación.
    puntos : int
        Puntuación obtenida en esta generación.
    alcohol : int
        Nivel de alcohol registrado en esta generación.
    llego_meta : bool
        Indicador de si se llegó a la meta en esta generación (True si se llegó, False si no).
    tiempo_total : float
        Tiempo total en segundos que tomó esta generación.

    Métodos:
    --------
    to_string() -> str:
        Devuelve una representación en texto del registro de la generación,
        formateada con todos los datos relevantes de la instancia.
    """

    def __init__(self, generacion: int, pasos: int, puntos: int, alcohol: int, 
                 llego_meta: bool, tiempo_total: float):
        """
        Inicializa una instancia de RegistroGeneracion con los datos específicos de una generación.

        Parámetros:
        -----------
        generacion : int
            El número de la generación.
        pasos : int
            Número de pasos realizados en esta generación.
        puntos : int
            Puntuación obtenida en esta generación.
        alcohol : int
            Nivel de alcohol registrado.
        llego_meta : bool
            Indicador de si se alcanzó la meta en esta generación.
        tiempo_total : float
            Tiempo total en segundos para completar la generación.
        """
        self.generacion = generacion
        self.pasos = pasos
        self.puntos = puntos
        self.alcohol = alcohol
        self.llego_meta = llego_meta
        self.tiempo_total = tiempo_total

    def to_string(self) -> str:
        """
        Devuelve una representación en texto de la instancia, formateada y detallada.

        Retorna:
        --------
        str:
            Cadena de texto con toda la información del registro de la generación,
            incluyendo los pasos, puntos, nivel de alcohol, si se llegó a la meta y el tiempo total.

        Ejemplo de retorno:
        -------------------
        "Generación: 1
        Pasos: 100
        Puntos: 50
        Alcohol: 10
        Llegó a la meta: Sí
        Tiempo total: 15.30 segundos"
        """
        return (f"Generación: {self.generacion}\n"
                f"Pasos: {self.pasos}\n"
                f"Puntos: {self.puntos}\n"
                f"Alcohol: {self.alcohol}\n"
                f"Llegó a la meta: {'Sí' if self.llego_meta else 'No'}\n"
                f"Tiempo total: {self.tiempo_total:.2f} segundos\n")
