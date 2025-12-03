import json
import random
import mysql.connector

import src.pokeapi.GestorAPI as gapi
import src.pokemon.Pokemon as pkmn
import src.status.StatusDistribuicao as sd

class GestorCartas:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init_once(*args, **kwargs)
        return cls._instance

    def __init_once(self):
        self.__pokemons = []

    def listarPokemons(self, idPlayer: int) -> str:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="distribuicao_de_cartas"
        )
        cursor = con.cursor(dictionary=True)

        query = """
                SELECT p.idPokemon   AS numero_pokedex,
                       p.nomePokemon AS nome,
                       p.isShiny     AS isShiny
                FROM UsuarioPokemon up
                         JOIN Pokemon p ON p.idPokemon = up.idPokemon
                WHERE up.idUsuario = %s
                """

        cursor.execute(query, (idPlayer,))
        resultado = cursor.fetchall()

        for p in resultado:
            p["isShiny"] = bool(p["isShiny"])

        cursor.close()
        con.close()

        return json.dumps(resultado, indent=4)

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
                    # 1/8192 de chance de ser shiny (~0.012%)
                    isShiny = random.randint(1, 8192) == 1
                    novo_pokemon = pkmn.Pokemon(nome, numero_pokedex, isShiny)
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
    
    #TODO: Adicionar o pokémon ao Banco de Dados
    def adicionarPokemon(self, pokemon):
        try:
            self.__pokemons.append(pokemon)
            return sd.StatusDistribuicao().sucesso(f"{pokemon.get_nome()} adicionado com sucesso.")
        except Exception as e:
            return sd.StatusDistribuicao().erro(f"Erro ao adicionar pokémon: {e}")