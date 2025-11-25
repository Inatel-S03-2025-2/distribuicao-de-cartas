class Pokemon:
    def __init__(self, numero_pokedex: int, nome: str, shiny: bool = False):
        self.__numero_pokedex = numero_pokedex
        self.__nome = nome
        self.__shiny = shiny

    def get_numero_pokedex(self):
        return self.__numero_pokedex

    def get_nome(self):
        return self.__nome

    def is_shiny(self):
        return self.__shiny