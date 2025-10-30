import json
import random

import src.pokeapi.GestorAPI as gapi
import src.pokemon.Pokemon as pkmn
import src.status.StatusDistribuicao as sd

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

    # FIXME: por enquanto retorna um booleano, mas deve ser alterado futuramente para statusDistribuicao
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

    # FIXME: por enquanto retorna um booleano, mas deve ser alterado futuramente para statusDistribuicao
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
    
    def gerarPokemonsIniciais(self):
        pokemons = []
        gestor = gapi.GestorAPI()
        status = sd.StatusDistribuicao()
        while len(pokemons) < 5:
            pokemon_id = random.randint(1, 1025)
            if pokemon_id not in pokemons:
                dados_pokemon = gestor.getPokemon(pokemon_id)
                if dados_pokemon:
                    nome = dados_pokemon['name']
                    numero_pokedex = dados_pokemon['id']
                    novo_pokemon = pkmn.Pokemon(nome, numero_pokedex)
                    self.__pokemons.append(novo_pokemon)
                    pokemons.append(pokemon_id)
                    status.sucesso(f"{nome} adicionado com sucesso.")
                else:
                    status.erro(f"Falha ao obter dados para o Pokémon com ID {pokemon_id}.")
        return status.sucesso("Geração de pokémons concluída com sucesso.")
    #TODO: Mandar a lista de pokémons para o Banco de Dados
    
    def removerPokemon(self, pokemon):
        try:
            self.__pokemons.remove(pokemon)
            return sd.StatusDistribuicao().sucesso(f"{pokemon.get_nome()} removido com sucesso.")
        except ValueError:
            return sd.StatusDistribuicao().erro(f"{pokemon.get_nome()} não encontrado na lista.")
        except Exception as e:
            return sd.StatusDistribuicao().erro(f"Erro ao remover pokémon: {e}")
        #TODO: Remover o pokémon do Banco de Dados