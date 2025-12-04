from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.modules.distribuicao.service import GestorCartas
from app.modules.distribuicao.models import Pokemon
from app.modules.distribuicao.external import GestorAPI

router = APIRouter()

# Schema para a resposta
class PokemonResponse(BaseModel):
    numero_pokedex: int
    nome: str
    shiny: bool

class DistribuicaoResponse(BaseModel):
    status: str
    mensagem: str
    codigo: str
    pokemons: list[PokemonResponse] = []

class TrocaPokemonSchema(BaseModel):
    removed_pokemon_id: int
    removed_pokemon_shiny: bool
    add_pokemon_id: int
    add_pokemon_shiny: bool

class TrocaPlayerSchema(BaseModel):
    sender_id: str
    sender_pokemon_id: int
    sender_pokemon_shiny: bool
    receiver_id: str
    receiver_pokemon_id: int
    receiver_pokemon_shiny: bool

class PokemonSchema(BaseModel):
    pokemon_id: int
    pokemon_shiny: bool

<<<<<<< HEAD
#TODO:
@router.get("/payers/{player_id}/team")
def time_jogador(player_id: str):
    return

@router.post("/players/{player_id}/distribution", response_model=DistribuicaoResponse)
def distribuicao_inicial(player_id: str):
    status = GestorCartas.gerarPokemonsIniciais()
    return status


@router.post("/players/{player_id}/team")
def adiciona_pokemon_jogador(player_id: str, dados_pokemon: PokemonSchema):
    pokemon_adicionado = GestorAPI.getPokemon(
        numero_pokedex=dados_pokemon.pokemon_id,
        shiny=dados_pokemon.pokemon_shiny
    )
    status = GestorCartas.adicionarPokemon(player_id, pokemon_adicionado)
    return status

@router.delete("/players/{player_id}/team")
def remove_pokemon_jogador(player_id: str, dados_pokemon: PokemonSchema):

    pokemon_removido = GestorAPI.getPokemon(dados_pokemon.pokemon_id)
    status = GestorCartas().removerPokemon(player_id, pokemon_removido)
=======

@router.get("/players/{player_id}/team")
def time_jogador(player_id: str):
    return {"message": "Endpoint não implementado"}

@router.post("/players/{player_id}/distribution", response_model=DistribuicaoResponse)
def distribuicao_inicial(player_id: str):
    resultado = GestorCartas(GestorAPI(), None).gerarPokemonsIniciais(player_id)
    return resultado

@router.delete("/players/{player_id}/team")
def remove_pokemon_jogador(player_id: str, dados_pokemon: PokemonSchema):
    id_pokemon = dados_pokemon.pokemon_id
    is_shiny = dados_pokemon.pokemon_shiny
    pokemon_removido = GestorAPI().getPokemon(numero_pokedex=id_pokemon, shiny=is_shiny)
    resultado = GestorCartas(GestorAPI(), None).removerPokemon(player_id, pokemon_removido)
    return resultado

@router.post("/players/{player_id}/team")
def adiciona_pokemon_jogador(player_id: str, dados_pokemon: PokemonSchema):
    id_pokemon = dados_pokemon.pokemon_id
    is_shiny = dados_pokemon.pokemon_shiny
    pokemon_adicionado = GestorAPI().getPokemon(numero_pokedex=id_pokemon, shiny=is_shiny)
    resultado = GestorCartas(GestorAPI(), None).adicionarPokemon(player_id, pokemon_adicionado)
    return resultado
>>>>>>> 8b830eef67a9bdf9b19a4f54dd0496362ea72d9f

    return status

#TODO:
@router.patch("/players/{player_id}/team")
def troca_pokemons_jogador(player_id: int, dados_troca: TrocaPokemonSchema):
    id_removido = dados_troca.removed_pokemon_id
    shiny_removido = dados_troca.removed_pokemon_shiny
    id_adicionado = dados_troca.add_pokemon_id
    shiny_adicionado = dados_troca.add_pokemon_shiny
    return {"message": "Endpoint não implementado"}

<<<<<<< HEAD
#TODO:
@route.post("/trades")
=======

@router.post("/trades")
>>>>>>> 8b830eef67a9bdf9b19a4f54dd0496362ea72d9f
def troca_entre_players(dados_troca: TrocaPlayerSchema):
    sender_id = dados_troca.sender_id
    sender_poke_id = dados_troca.sender_pokemon_id
    sender_is_shiny = dados_troca.sender_pokemon_shiny
    receiver_id = dados_troca.receiver_id
    receiver_poke_id = dados_troca.receiver_pokemon_id
    receiver_is_shiny = dados_troca.receiver_pokemon_shiny
    return {"message": "Endpoint não implementado"}