"""
Router - Endpoints da API de distribuição de pokémons

Fornece 2 endpoints principais:
1. POST /players/{id}/distribution - Distribuir pokémons quando jogador se cadastra
2. GET /players/{id}/pokemons - Interface de consulta para outras aplicações
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List

from .service import DistribuicaoService
from ...shared.database import SessionLocal
from .schemas import Status


# Dependency para obter a sessão do banco
def get_db():
    """Fornece sessão do banco de dados para os endpoints"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Schemas para as respostas
class PokemonResponse(BaseModel):
    """Schema de resposta para pokémon"""
    numero_pokedex: int
    nome: str
    is_shiny: bool


class DistribuicaoResponse(BaseModel):
    """Schema de resposta para distribuição"""
    status: str
    mensagem: str
    codigo: str
    pokemons: List[PokemonResponse] = []


class AdicionarPokemonRequest(BaseModel):
    """Schema para adicionar pokémon"""
    pokemon_id: int
    is_shiny: bool = False


class TrocarPokemonRequest(BaseModel):
    """Schema para trocar pokémon de um jogador"""
    removed_pokemon_id: int
    add_poke_id: int


class TrocarEntreJogadoresRequest(BaseModel):
    """Schema para troca entre jogadores"""
    sender_id: int
    sender_poke_id: int
    receiver_id: int
    receiver_poke_id: int


# Inicializa o router
router = APIRouter(
    prefix="/api/v1",
    tags=["distribuicao"]
)


@router.post("/players/{id}/distribution", response_model=DistribuicaoResponse)
def distribuir_pokemons_iniciais(id: int, db: Session = Depends(get_db)):
    """
    🎯 ENDPOINT PRINCIPAL: Distribui 5 pokémons aleatórios quando um jogador se cadastra.
    
    Chamado pela aplicação de cadastro quando um novo jogador é criado.
    Sorteia 5 pokémons diferentes da PokéAPI e registra no banco.
    
    Args:
        id: ID do jogador que acabou de se cadastrar
        db: Sessão do banco de dados (injetada)
        
    Returns:
        DistribuicaoResponse com os 5 pokémons sorteados e distribuídos
    """
    try:
        service = DistribuicaoService(db)
        status, pokemons = service.distribuir_pokemons_iniciais(id)
        
        # Converter para o formato da resposta
        pokemons_resposta = [
            PokemonResponse(
                numero_pokedex=p["numero_pokedex"],
                nome=p["nome"],
                is_shiny=p["is_shiny"]
            )
            for p in pokemons
        ]
        
        return DistribuicaoResponse(
            status=status.get_status(),
            mensagem=status.get_mensagem(),
            codigo=status.get_codigo(),
            pokemons=pokemons_resposta
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao sortear pokémons: {str(e)}")


@router.get("/players/{id}/pokemons", response_model=DistribuicaoResponse)
def listar_pokemons_jogador(id: int, db: Session = Depends(get_db)):
    """
    📋 INTERFACE DE CONSULTA: Permite que outras aplicações consultem os pokémons distribuídos.
    
    Endpoint usado por outras aplicações do sistema para verificar quais pokémons
    foram distribuídos para um determinado jogador.
    
    Args:
        id: ID do jogador
        db: Sessão do banco de dados (injetada)
        
    Returns:
        DistribuicaoResponse com a lista de pokémons do jogador
    """
    try:
        service = DistribuicaoService(db)
        status, pokemons = service.listar_pokemons_jogador(id)
        
        # Verificar se houve erro
        if status.get_status() != Status.SUCESSO.value:
            raise HTTPException(
                status_code=int(status.get_codigo()),
                detail=status.get_mensagem()
            )
        
        # Converter para o formato da resposta
        pokemons_resposta = [
            PokemonResponse(
                numero_pokedex=p["numero_pokedex"],
                nome=p["nome"],
                is_shiny=p["is_shiny"]
            )
            for p in pokemons
        ]
        
        return DistribuicaoResponse(
            status=status.get_status(),
            mensagem=status.get_mensagem(),
            codigo=status.get_codigo(),
            pokemons=pokemons_resposta
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar pokémons: {str(e)}")


@router.post("/players/{id}/team/{pokemonId}")
def adicionar_pokemon(id: int, pokemonId: int, request: AdicionarPokemonRequest, db: Session = Depends(get_db)):
    """
    POST /players/{id}/team/{pokemonId}
    Adiciona 1 pokémon no inventário do jogador.
    Se o jogador já possuir o pokémon ou não tiver espaço, retorna erro.
    """
    try:
        service = DistribuicaoService(db)
        status = service.adicionar_pokemon_jogador(id, pokemonId, request.is_shiny)
        
        if status.get_status() != Status.SUCESSO.value:
            raise HTTPException(
                status_code=int(status.get_codigo()),
                detail=status.get_mensagem()
            )
        
        return {
            "status": int(status.get_codigo()),
            "message": status.get_mensagem(),
            "data": {
                "player_id": id,
                "operation": "ADDED",
                "pokemon_id": pokemonId
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar pokémon: {str(e)}")


@router.delete("/players/{id}/team/{pokemonId}")
def remover_pokemon(id: int, pokemonId: int, db: Session = Depends(get_db)):
    """
    DELETE /players/{id}/team/{pokemonId}
    Remove 1 pokémon do jogador.
    Se o jogador não possuir o pokémon, retorna erro.
    """
    try:
        service = DistribuicaoService(db)
        status = service.remover_pokemon_jogador(id, pokemonId)
        
        if status.get_status() != Status.SUCESSO.value:
            raise HTTPException(
                status_code=int(status.get_codigo()),
                detail=status.get_mensagem()
            )
        
        return {
            "status": int(status.get_codigo()),
            "message": status.get_mensagem(),
            "data": {
                "player_id": id,
                "operation": "REMOVED",
                "pokemon_id": pokemonId
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao remover pokémon: {str(e)}")


@router.patch("/players/{id}/team")
def trocar_pokemon(id: int, request: TrocarPokemonRequest, db: Session = Depends(get_db)):
    """
    PATCH /players/{id}/team
    Realiza a troca no inventário do jogador, removendo pokémon 1 e adicionando pokémon 2.
    Body: {removed_pokemon_id, add_poke_id}
    """
    try:
        service = DistribuicaoService(db)
        status = service.trocar_pokemon_jogador(id, request.removed_pokemon_id, request.add_poke_id)
        
        if status.get_status() != Status.SUCESSO.value:
            raise HTTPException(
                status_code=int(status.get_codigo()),
                detail=status.get_mensagem()
            )
        
        return {
            "status": int(status.get_codigo()),
            "message": status.get_mensagem(),
            "data": {
                "player_id": id,
                "operation": "SWAPPED",
                "removed_pokemon_id": request.removed_pokemon_id,
                "added_pokemon_id": request.add_poke_id
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao trocar pokémon: {str(e)}")


@router.post("/trades")
def trocar_entre_jogadores(request: TrocarEntreJogadoresRequest, db: Session = Depends(get_db)):
    """
    POST /trades
    Realiza a troca entre jogador 1 e jogador 2.
    Remove pokémon 1 do sender e adiciona ao receiver, e vice-versa.
    Body: {sender_id, sender_poke_id, receiver_id, receiver_poke_id}
    """
    try:
        service = DistribuicaoService(db)
        status = service.trocar_entre_jogadores(
            request.sender_id, 
            request.sender_poke_id,
            request.receiver_id,
            request.receiver_poke_id
        )
        
        if status.get_status() != Status.SUCESSO.value:
            raise HTTPException(
                status_code=int(status.get_codigo()),
                detail=status.get_mensagem()
            )
        
        return {
            "status": int(status.get_codigo()),
            "message": status.get_mensagem(),
            "data": {
                "operation": "TRADE",
                "sender_id": request.sender_id,
                "sender_pokemon_id": request.sender_poke_id,
                "receiver_id": request.receiver_id,
                "receiver_pokemon_id": request.receiver_poke_id
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao realizar troca: {str(e)}")


@router.delete("/players/{id}")
def remover_jogador(id: int, db: Session = Depends(get_db)):
    """
    DELETE /players/{id}
    Remove completamente um jogador do banco de dados.
    """
    try:
        service = DistribuicaoService(db)
        status = service.remover_jogador(id)
        
        if status.get_status() != Status.SUCESSO.value:
            raise HTTPException(
                status_code=int(status.get_codigo()),
                detail=status.get_mensagem()
            )
        
        return {
            "status": int(status.get_codigo()),
            "message": status.get_mensagem(),
            "data": {
                "player_id": id,
                "operation": "PLAYER_REMOVED"
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao remover jogador: {str(e)}")