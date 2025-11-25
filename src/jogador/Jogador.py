class Jogador:
    def __init__(self, id: str, pokemons: list, log: str):
        self.__id = id
        self.__pokemons = pokemons  # lista de objetos Pokemon
        self.__log = log

    def get_id(self):
        return self.__id
    def get_pokemons(self):
        return self.__pokemons
    def get_log(self):
        return self.__log
