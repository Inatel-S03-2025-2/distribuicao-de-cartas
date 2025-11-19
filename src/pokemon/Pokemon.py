class Pokemon:
    def __init__(self, nome: str, numero_pokedex: int, isShiny: bool = False):
        self.__numero_pokedex = numero_pokedex
        self.__nome = nome
        self.__isShiny = isShiny

    def get_numero_pokedex(self):
        return self.__numero_pokedex

    def get_nome(self):
        return self.__nome
    
    def get_isShiny(self):
        return self.__isShiny