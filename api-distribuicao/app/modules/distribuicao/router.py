from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from modules.distribuicao.service import GestorCartas
from modules.distribuicao.external import GestorAPI

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

@router.post("/players/{id}/distribution", response_model=DistribuicaoResponse)
def distribuir_pokemons_iniciais(id: int):
    """
    Sorteia os 5 pokémons iniciais para o jogador em questão
    """
    try:
        # Instancia o gestor sem banco de dados
        gestor_cartas = GestorCartas(GestorAPI(), None)
        
        # Gera os 5 pokémons iniciais
        resultado = gestor_cartas.gerarPokemonsIniciais()
        
        if resultado.get("status") != "sucesso":
            raise HTTPException(
                status_code=500, 
                detail=resultado.get("mensagem", "Erro ao gerar pokémons")
            )
        
        pokemons = resultado.get("pokemons", [])
        
        # Converte os objetos Pokemon para o formato de resposta
        pokemons_resposta = [
            {
                "numero_pokedex": pokemon.get_numero_pokedex(),
                "nome": pokemon.get_nome(),
                "shiny": pokemon.is_shiny()
            }
            for pokemon in pokemons
        ]
        
        return {
            "status": "sucesso",
            "mensagem": f"5 pokémons iniciais sorteados com sucesso para o jogador {id}",
            "codigo": "200",
            "pokemons": pokemons_resposta
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao sortear pokémons: {str(e)}")