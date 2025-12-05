import json
import random

from modules.distribuicao.external import GestorAPI
from modules.distribuicao.models import Pokemon, Jogador
from modules.distribuicao.schemas import StatusDistribuicao, Status
from modules.distribuicao.repository import GerenciadorBD

class GestorCartas:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init_once(*args, **kwargs)
        return cls._instance

    def __init_once(self, api:GestorAPI, bd:GerenciadorBD):
        self.__pokemons = []
        self.__api = api
        self.__bd = bd

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
            
            jogador = Jogador(id=idJogador, pokemons=pokemons)
            
            #------------------------------------------------------------------------
            try:
                self.__bd.createJogador(jogador)
            except ValueError as e:
                print(f"Erro: {e}")
            #------------------------------------------------------------------------
            try:
                for p in pokemons:
                    self.__bd.adicionarPokemon(p)
            except ValueError as e:
                print(f"Erro: {e}")
            #------------------------------------------------------------------------
            try:
                for p in pokemons:
                    self.__bd.adicionarPokemonAoJogador(jogador.get_id(), p)
            except ValueError as e:
                print(f"Erro: {e}")
            #------------------------------------------------------------------------


            sd.set_status(Status.SUCESSO)
            sd.set_mensagem("Os 5 pokémons iniciais foram gerados com sucesso.")
            sd.set_codigo("200")
            status = sd.get_resumo()
            status["pokemons"] = pokemons
            return status
        except AttributeError as e:
            sd.set_status(Status.ERRO)
            sd.set_mensagem(f"Erro ao gerar pokémons iniciais: {e}")
            sd.set_codigo("500")
            return sd.get_resumo()
    
    def adicionarPokemon(self, idJogador: int, pokemon: Pokemon) -> dict:
        sd = StatusDistribuicao()
        
        try:
            #------------------------------------------------------------------------
            try:
                self.__bd.adicionarPokemon(pokemon)
            except ValueError as e:
                print(f"Erro: {e}")
            #------------------------------------------------------------------------
            try:
                self.__bd.adicionarPokemonAoJogador(idJogador, pokemon)
            except ValueError as e:
                print(f"Erro: {e}")
            #------------------------------------------------------------------------
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


    def removerPokemon(self, idJogador: int, pokemon: Pokemon) :
        sd = StatusDistribuicao()
        try:
            self.__bd.removerPokemonDoJogador(idJogador, pokemon.get_numero_pokedex())
        except ValueError as e:
            print(f"Erro: {e}")
        sd.set_status(Status.SUCESSO)
        sd.set_mensagem(f"{pokemon.get_nome()} foi removido da coleção do jogador {idJogador}.")
        sd.set_codigo("200")
        return sd.get_resumo()
    
    def listarTime(self, idJogador: str):
        try:
            # 1. Busca a lista de objetos Pokemon (Do domínio) usando o método existente no BD
            # Isso retorna uma lista de objetos da classe Pokemon
            lista_pokemons_dominio = self.__bd.getPokemonsDoJogador(idJogador)

            # 2. Transforma os objetos de domínio em dicionários simples para o JSON
            lista_formatada = []
            for pokemon in lista_pokemons_dominio:
                lista_formatada.append({
                    "pokemon_name": pokemon.get_nome(),
                    "is_shiny": pokemon.is_shiny()
                })

            # 3. Monta a resposta no formato exato solicitado
            return {
                "status": 200,
                "message": "Time adquirido com sucesso",
                "data": {
                    "player": idJogador,  # Usando o ID conforme solicitado (fallback do nome)
                    "operation": "LIST_TEAM",
                    "team": lista_formatada
                }
            }

        except ValueError as e:
            # Caso o usuário não exista (o repo lança ValueError)
            return {
                "status": 404,
                "message": str(e),
                "data": {}
            }
        except Exception as e:
            return {
                "status": 500,
                "message": f"Erro interno ao listar time: {str(e)}",
                "data": {}
            }