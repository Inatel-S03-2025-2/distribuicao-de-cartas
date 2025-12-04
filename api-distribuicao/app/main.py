from fastapi import FastAPI
from modules.distribuicao.repository import PokemonRepository
from modules.distribuicao.models import Pokemon
from shared.database import SessionLocal

# app = FastAPI()

# # Rota principal (GET)
# @app.get("/")
# def home():
#     return {"mensagem": "Olá! Minha API está viva."}

# from modules.distribuicao.router import router as distribuicao_router
# app.include_router(distribuicao_router, prefix="/api", tags=["Distribuição"])

# from modules.distribuicao.service import GestorCartas
# from modules.distribuicao.external import GestorAPI
# gestor_cartas = GestorCartas(GestorAPI(), None)

# resultado = gestor_cartas.gerarPokemonsIniciais()
# if resultado.get("status") == "sucesso":
#     pokemons = resultado.get("pokemons", [])
#     for p in pokemons:
#         print(f"Número da Pokédex: {p.get_numero_pokedex()}, Nome: {p.get_nome()}, Shiny: {p.is_shiny()}")
# else:
#     print(f"Erro: {resultado.get('mensagem')}")


pokemon1 = Pokemon(10, "bulba", True)
pokemon2 = Pokemon(20, "sharm", False)


PokemonRepository().adicionaPokemon(pokemon=pokemon1)