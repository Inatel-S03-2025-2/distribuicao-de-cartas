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

    def trocarPokemonADM(self, pokemon_origem, pokemon_destino):
        """
        Método para administrador trocar pokémons no sistema.
        
        Args:
            pokemon_origem: Pokémon que será removido
            pokemon_destino: Pokémon que será adicionado
            
        Returns:
            bool: True se a troca foi realizada com sucesso, False caso contrário
        """
        try:
            if pokemon_origem in self.__pokemons:
                # Remove o pokémon de origem
                self.__pokemons.remove(pokemon_origem)
                # Adiciona o pokémon de destino
                self.__pokemons.append(pokemon_destino)
                return True
            else:
                return False
        except Exception as e:
            print(f"Erro na troca de pokémon (ADM): {e}")
            return False

    def trocarPokemonPlayer(self, indice_origem, pokemon_destino):
        """
        Método para jogador trocar pokémon por índice.
        
        Args:
            indice_origem (int): Índice do pokémon a ser trocado na lista
            pokemon_destino: Pokémon que substituirá o pokémon no índice especificado
            
        Returns:
            bool: True se a troca foi realizada com sucesso, False caso contrário
        """
        try:
            if 0 <= indice_origem < len(self.__pokemons):
                # Substitui o pokémon no índice especificado
                self.__pokemons[indice_origem] = pokemon_destino
                return True
            else:
                print(f"Índice inválido: {indice_origem}")
                return False
        except Exception as e:
            print(f"Erro na troca de pokémon (Player): {e}")
            return False