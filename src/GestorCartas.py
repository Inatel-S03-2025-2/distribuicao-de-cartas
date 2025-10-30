import json

class GestorCartas:
    def __init__(self):
        self.__pokemons = []

    def listarPokemons(self, formato: str) -> str:
        dicionario = []
        for p in self.__pokemons:
            dicionario.append({
                "numero_pokedex": p.get_numero_pokedex(),
                "nome": p.get_nome()
            })

        if formato.lower() == "json":
            return json.dumps(dicionario, indent=4)
        else:
            return "Formato inválido! Use 'json'."