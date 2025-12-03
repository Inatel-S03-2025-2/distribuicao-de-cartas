import json
import random

from .external import GestorAPI
from .models import Pokemon, UsuarioPokemonORM
from .schemas import StatusDistribuicao, Status

class GestorCartas:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init_once(*args, **kwargs)
        return cls._instance

    def __init_once(self, api:GestorAPI, bd):
        self.__pokemons = []
        self.__api = api
        self.__bd = bd



    def gerarPokemonsIniciais(self):
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
            sd.set_status(Status.SUCESSO)
            sd.set_mensagem("Os 5 pokémons iniciais foram gerados com sucesso.")
            sd.set_codigo("200")
            resultado = sd.get_resumo()
            resultado["pokemons"] = pokemons
            return resultado
        except AttributeError as e:
            sd.set_status(Status.ERRO)
            sd.set_mensagem(f"Erro ao gerar pokémons iniciais: {e}")
            sd.set_codigo("500")
            return sd.get_resumo()
    
    def adicionarPokemon(self, id_player: int, pokemon: Pokemon) -> dict:
        sd = StatusDistribuicao()
        
        try:
            # Verifica se o usuário existe
            usuario = self.__bd.usuario_repo.buscaUsuarioId(id_player)
            
            # Adiciona o Pokémon ao jogador
            self.__bd.usuario_pokemon_repo.adicionarPokemonUsuario(id_player, pokemon)
            
            sd.set_status(Status.SUCESSO)
            sd.set_mensagem(f"{pokemon.get_nome()} foi adicionado à coleção do jogador {id_player}.")
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


    def removerPokemon(self, id_player: int, pokemon: Pokemon) -> dict:
        """Remove um Pokémon da coleção de um jogador específico"""
        sd = StatusDistribuicao()
        
        try:
            # Verifica se o usuário existe
            usuario = self.__bd.usuario_repo.buscaUsuarioId(id_player)
            
            # Busca a relação UsuarioPokemon
            relacao = self.__bd.db.query(UsuarioPokemonORM).filter(
                UsuarioPokemonORM.idUsuario == id_player,
                UsuarioPokemonORM.idPokemon == pokemon.get_numero_pokedex()
            ).first()
            
            if not relacao:
                sd.set_status(Status.ERRO)
                sd.set_mensagem(f"O jogador {id_player} não possui {pokemon.get_nome()} em sua coleção.")
                sd.set_codigo("404")
                return sd.get_resumo()
            
            # Remove a relação
            self.__bd.db.delete(relacao)
            self.__bd.db.commit()
            
            sd.set_status(Status.SUCESSO)
            sd.set_mensagem(f"{pokemon.get_nome()} foi removido da coleção do jogador {id_player}.")
            sd.set_codigo("200")
            return sd.get_resumo()
            
        except ValueError as e:
            # Erros esperados (usuário não existe, etc)
            sd.set_status(Status.ERRO)
            sd.set_mensagem(str(e))
            sd.set_codigo("400")
            return sd.get_resumo()
            
        except Exception as e:
            # Erros inesperados
            self.__bd.db.rollback()
            sd.set_status(Status.ERRO)
            sd.set_mensagem(f"Erro inesperado ao remover Pokémon: {e}")
            sd.set_codigo("500")
            return sd.get_resumo()