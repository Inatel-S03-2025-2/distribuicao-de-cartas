"""
Classe de domínio Jogador
Representa um jogador do sistema com seus pokémons e histórico
"""


class Jogador:
    def __init__(self, id: str, pokemons: list = None, log: str = ""):
        self.__id = id
        self.__pokemons = pokemons if pokemons is not None else []
        self.__log = log

    def get_id(self):
        return self.__id
    
    def get_pokemons(self):
        return self.__pokemons
    
    def get_log(self):
        return self.__log
