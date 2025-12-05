import json
import random

from .external import GestorAPI
from .models import Pokemon, Jogador
from .schemas import StatusDistribuicao, Status
from .repository import PokemonRepository, UsuarioRepository, UsuarioPokemonRepository
from .repository import GerenciadorBD

class GestorCartas:
    _instance = None
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, api: GestorAPI, bd: GerenciadorBD):
        if not GestorCartas._initialized:
            self.__pokemons = []
            self.__api = api
            self.__bd = bd
            GestorCartas._initialized = True

    def gerarPokemonsIniciais(self, idJogador:str):
        sd = StatusDistribuicao()
        pokemon = Pokemon()
        pokemons_id = []
        pokemons = []
        try:
            while len(pokemons_id) < 5:
                pokemon_id = random.randint(1, self.__api.getMaxID())
                if pokemon_id not in pokemons_id:
                    isShiny = random.randint(1, 256) == 1
                    pokemon = self.__api.getPokemon(pokemon_id, shiny=isShiny)
                    if pokemon != None:
                        pokemons.append(pokemon)
                        pokemons_id.append(pokemon_id)
                    else:
                        pass
            
            # Cria jogador
            self.__bd.createJogador(idJogador)
            
            # Adiciona pokémons
            for p in pokemons:
                self.__bd.adicionarPokemon(p)
            
            # Associa pokémons ao jogador
            for p in pokemons:
                self.__bd.adicionarPokemonAoJogador(idJogador, p)
            
            sd.set_status(Status.SUCESSO)
            sd.set_mensagem("Os 5 pokémons iniciais foram gerados com sucesso.")
            sd.set_codigo("200")
            status = sd.get_resumo()
            status["pokemons"] = pokemons
            return status
            
        except ValueError as e:
            sd.set_status(Status.ERRO)
            sd.set_mensagem(f"Erro de validação: {e}")
            sd.set_codigo("400")
            return sd.get_resumo()
            
        except Exception as e:
            sd.set_status(Status.ERRO)
            sd.set_mensagem(f"Erro ao gerar pokémons iniciais: {e}")
            sd.set_codigo("500")
            return sd.get_resumo()
    
    def adicionarPokemon(self, idJogador: str, pokemon: Pokemon) -> dict:
        sd = StatusDistribuicao()
        
        try:
            # Adiciona pokémon ao banco
            self.__bd.adicionarPokemon(pokemon)
            
            # Associa ao jogador
            self.__bd.adicionarPokemonAoJogador(idJogador, pokemon)
            
            sd.set_status(Status.SUCESSO)
            sd.set_mensagem(f"{pokemon.get_nome()} foi adicionado à coleção do jogador {idJogador}.")
            sd.set_codigo("200")
            return sd.get_resumo()
            
        except ValueError as e:
            # Erros esperados (usuário não existe, pokémon duplicado, etc)
            sd.set_status(Status.ERRO)
            sd.set_mensagem(str(e))
            sd.set_codigo("400")
            return sd.get_resumo()
            
        except Exception as e:
            # Erros inesperados
            sd.set_status(Status.ERRO)
            sd.set_mensagem(f"Erro inesperado ao adicionar Pokémon: {e}")
            sd.set_codigo("500")
            return sd.get_resumo()


    def removerPokemon(self, idJogador: str, pokemon: Pokemon):
        sd = StatusDistribuicao()
        try:
            self.__bd.removerPokemonDoJogador(idJogador, pokemon.get_numero_pokedex())
            sd.set_status(Status.SUCESSO)
            sd.set_mensagem(f"{pokemon.get_nome()} foi removido da coleção do jogador {idJogador}.")
            sd.set_codigo("200")
            return sd.get_resumo()
            
        except ValueError as e:
            sd.set_status(Status.ERRO)
            sd.set_mensagem(str(e))
            sd.set_codigo("400")
            return sd.get_resumo()
            
        except Exception as e:
            sd.set_status(Status.ERRO)
            sd.set_mensagem(f"Erro inesperado ao remover Pokémon: {e}")
            sd.set_codigo("500")
            return sd.get_resumo()