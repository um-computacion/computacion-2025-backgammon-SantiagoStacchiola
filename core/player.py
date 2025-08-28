class Player:
    def __init__(self, color: str):
        if color not in ["blanca", "negra"]:
            raise ValueError("Color inválido, debe ser 'blanca' o 'negra'")
        
        self.__color__ = color
        self.__fichas_en_juego__ = 15  # cantidad total
        self.__barra__ = []            # fichas capturadas
        self.__fuera__ = []            # fichas que ya salieron 

    def get_color(self):
        # Muestra el color
        return self.__color__
    