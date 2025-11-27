"""
Service Layer - Lógica de negócio da distribuição de pokémons

Responsável por:
1. Sortear 5 pokémons aleatórios da PokéAPI quando um jogador se cadastra
2. Garantir que um jogador não tenha pokémons repetidos
3. Fornecer interface para consulta dos pokémons distribuídos
"""
import random
from sqlalchemy.orm import Session
from typing import Tuple, List, Dict, Any

from ...core.pokemon import Pokemon
from ...core.config import settings
from .repository import PokemonRepository, UsuarioRepository, UsuarioPokemonRepository
from .external import GestorAPI
from .schemas import StatusDistribuicao, Status
from .models import UsuarioPokemonORM, PokemonORM, UsuarioORM


class DistribuicaoService:
    """
    Serviço de distribuição de pokémons.
    
    Principais responsabilidades:
    - Distribuir 5 pokémons aleatórios quando um jogador se cadastra
    - Consultar pokémons de um jogador
    """
    
    def __init__(self, db: Session):
        """
        Inicializa o serviço com suas dependências.
        
        Args:
            db: Sessão do SQLAlchemy
        """
        self.db = db
        self.pokemon_repo = PokemonRepository(db)
        self.usuario_repo = UsuarioRepository(db)
        self.usuario_pokemon_repo = UsuarioPokemonRepository(db, self.pokemon_repo)
        self.gestor_api = GestorAPI()
    
    def distribuir_pokemons_iniciais(self, usuario_id: int) -> Tuple[StatusDistribuicao, List[Dict[str, Any]]]:
        """
        PRINCIPAL FUNCIONALIDADE: Distribui 5 pokémons aleatórios quando um jogador se cadastra.
        
        Regras:
        - Sorteia 5 pokémons aleatórios da PokéAPI
        - Garante que não haja repetição para o mesmo jogador
        - Um mesmo pokémon pode ser distribuído para jogadores diferentes
        
        Args:
            usuario_id: ID do jogador que acabou de se cadastrar
            
        Returns:
            Tupla com (StatusDistribuicao, lista de pokémons distribuídos)
        """
        status = StatusDistribuicao()
        
        try:
            # Verificar se usuário já tem pokémons
            count = self.db.query(UsuarioPokemonORM).filter(
                UsuarioPokemonORM.idUsuario == usuario_id
            ).count()
            
            if count >= settings.MAX_POKEMONS_PER_PLAYER:
                status.set_status(Status.ERRO)
                status.set_mensagem(f"Jogador já possui {count} pokémons")
                status.set_codigo("400")
                return status, []
            
            # Gerar pokémons únicos
            max_id = self.gestor_api.getMaxID()
            ids_gerados = set()
            pokemons_distribuidos = []
            
            slots_disponiveis = settings.MAX_POKEMONS_PER_PLAYER - count
            
            while len(ids_gerados) < slots_disponiveis:
                poke_id = random.randint(1, max_id)
                
                if poke_id in ids_gerados:
                    continue
                
                # Chance de shiny configurável
                is_shiny = random.randint(1, settings.SHINY_PROBABILITY) == 1
                
                # Buscar pokémon na API
                pokemon = self.gestor_api.getPokemon(poke_id, is_shiny)
                
                if pokemon is None:
                    continue
                
                # Adicionar pokémon na tabela Pokemon (se não existir)
                try:
                    self.pokemon_repo.adicionaPokemon(pokemon)
                except ValueError:
                    pass  # Pokémon já existe
                
                # Vincular pokémon ao usuário
                try:
                    self.usuario_pokemon_repo.adicionarPokemonJogador(usuario_id, pokemon)
                    ids_gerados.add(poke_id)
                    pokemons_distribuidos.append({
                        "nome": pokemon.get_nome(),
                        "numero_pokedex": pokemon.get_numero_pokedex(),
                        "is_shiny": pokemon.is_shiny()
                    })
                except ValueError:
                    continue
            
            status.set_status(Status.SUCESSO)
            status.set_mensagem(f"{len(pokemons_distribuidos)} pokémons distribuídos com sucesso")
            status.set_codigo("201")
            
            return status, pokemons_distribuidos
            
        except Exception as e:
            status.set_status(Status.ERRO)
            status.set_mensagem(f"Erro ao distribuir pokémons: {str(e)}")
            status.set_codigo("500")
            return status, []
    
    def listar_pokemons_jogador(self, usuario_id: int) -> Tuple[StatusDistribuicao, List[Dict[str, Any]]]:
        """
        INTERFACE DE CONSULTA: Permite que outras aplicações consultem os pokémons de um jogador.
        
        Args:
            usuario_id: ID do jogador
            
        Returns:
            Tupla com (StatusDistribuicao, lista de pokémons distribuídos)
        """
        status = StatusDistribuicao()
        
        try:
            # Verificar se usuário existe
            usuario = self.db.query(UsuarioORM).filter(
                UsuarioORM.idUsuario == usuario_id
            ).first()
            
            if not usuario:
                status.set_status(Status.ERRO)
                status.set_mensagem(f"Jogador {usuario_id} não encontrado")
                status.set_codigo("404")
                return status, []
            
            # Buscar pokémons do usuário
            pokemons = self.db.query(PokemonORM).join(
                UsuarioPokemonORM, PokemonORM.idPokemon == UsuarioPokemonORM.idPokemon
            ).filter(
                UsuarioPokemonORM.idUsuario == usuario_id
            ).all()
            
            pokemons_data = [
                {
                    "nome": p.nomePokemon,
                    "numero_pokedex": p.idPokemon,
                    "is_shiny": p.isShiny
                }
                for p in pokemons
            ]
            
            status.set_status(Status.SUCESSO)
            status.set_mensagem(f"Time do jogador {usuario_id} listado com sucesso")
            status.set_codigo("200")
            
            return status, pokemons_data
            
        except Exception as e:
            status.set_status(Status.ERRO)
            status.set_mensagem(f"Erro ao listar pokémons: {str(e)}")
            status.set_codigo("500")
            return status, []
    
    def adicionar_pokemon_jogador(self, usuario_id: int, pokemon_id: int, is_shiny: bool = False) -> StatusDistribuicao:
        """
        Adiciona 1 pokémon no inventário do jogador.
        Se o jogador já possuir o pokémon, ou não tiver espaço livre,
        nenhuma operação é realizada.
        """
        status = StatusDistribuicao()
        
        try:
            # Verificar se jogador já tem 5 pokémons
            count = self.db.query(UsuarioPokemonORM).filter(
                UsuarioPokemonORM.idUsuario == usuario_id
            ).count()
            
            if count >= settings.MAX_POKEMONS_PER_PLAYER:
                status.set_status(Status.ERRO)
                status.set_mensagem(f"Jogador já possui {settings.MAX_POKEMONS_PER_PLAYER} pokémons. Nenhum espaço livre.")
                status.set_codigo("400")
                return status
            
            # Buscar pokémon na API
            pokemon = self.gestor_api.getPokemon(pokemon_id, is_shiny)
            
            if pokemon is None:
                status.set_status(Status.ERRO)
                status.set_mensagem(f"Pokémon {pokemon_id} não encontrado na PokéAPI")
                status.set_codigo("404")
                return status
            
            # Adicionar ao banco
            try:
                self.pokemon_repo.adicionaPokemon(pokemon)
            except ValueError:
                pass  # Pokémon já existe
            
            # Vincular ao jogador
            self.usuario_pokemon_repo.adicionarPokemonJogador(usuario_id, pokemon)
            
            status.set_status(Status.SUCESSO)
            status.set_mensagem(f"Pokémon {pokemon.get_nome()} adicionado com sucesso")
            status.set_codigo("201")
            
            return status
            
        except ValueError as e:
            status.set_status(Status.ERRO)
            status.set_mensagem(str(e))
            status.set_codigo("400")
            return status
        except Exception as e:
            self.db.rollback()
            status.set_status(Status.ERRO)
            status.set_mensagem(f"Erro ao adicionar pokémon: {str(e)}")
            status.set_codigo("500")
            return status
    
    def remover_pokemon_jogador(self, usuario_id: int, pokemon_id: int) -> StatusDistribuicao:
        """
        Remove 1 pokémon do jogador.
        Se o jogador não possuir o pokémon, nenhuma operação é realizada.
        """
        status = StatusDistribuicao()
        
        try:
            # Buscar relação
            relacao = self.db.query(UsuarioPokemonORM).filter(
                UsuarioPokemonORM.idUsuario == usuario_id,
                UsuarioPokemonORM.idPokemon == pokemon_id
            ).first()
            
            if not relacao:
                status.set_status(Status.ERRO)
                status.set_mensagem(f"Jogador não possui o pokémon {pokemon_id}. Nenhuma operação realizada.")
                status.set_codigo("404")
                return status
            
            self.db.delete(relacao)
            self.db.commit()
            
            status.set_status(Status.SUCESSO)
            status.set_mensagem(f"Pokémon {pokemon_id} removido com sucesso")
            status.set_codigo("200")
            
            return status
            
        except Exception as e:
            self.db.rollback()
            status.set_status(Status.ERRO)
            status.set_mensagem(f"Erro ao remover pokémon: {str(e)}")
            status.set_codigo("500")
            return status
    
    def trocar_pokemon_jogador(self, usuario_id: int, pokemon_removido_id: int, pokemon_adicionado_id: int) -> StatusDistribuicao:
        """
        Realiza a troca no inventário do jogador, removendo o pokémon 1 e adicionando o pokémon 2.
        Se houver algum tipo de conflito, retorna status diferente.
        """
        status = StatusDistribuicao()
        
        try:
            # Verificar se possui o pokémon a ser removido
            relacao = self.db.query(UsuarioPokemonORM).filter(
                UsuarioPokemonORM.idUsuario == usuario_id,
                UsuarioPokemonORM.idPokemon == pokemon_removido_id
            ).first()
            
            if not relacao:
                status.set_status(Status.ERRO)
                status.set_mensagem(f"Jogador não possui o pokémon {pokemon_removido_id} para remover")
                status.set_codigo("404")
                return status
            
            # Verificar se já possui o pokémon a ser adicionado
            ja_possui = self.db.query(UsuarioPokemonORM).filter(
                UsuarioPokemonORM.idUsuario == usuario_id,
                UsuarioPokemonORM.idPokemon == pokemon_adicionado_id
            ).first()
            
            if ja_possui:
                status.set_status(Status.ERRO)
                status.set_mensagem(f"Jogador já possui o pokémon {pokemon_adicionado_id}")
                status.set_codigo("400")
                return status
            
            # Remover pokémon antigo
            self.db.delete(relacao)
            
            # Buscar pokémon novo na API
            pokemon_novo = self.gestor_api.getPokemon(pokemon_adicionado_id)
            
            if pokemon_novo is None:
                self.db.rollback()
                status.set_status(Status.ERRO)
                status.set_mensagem(f"Pokémon {pokemon_adicionado_id} não encontrado na PokéAPI")
                status.set_codigo("404")
                return status
            
            # Adicionar pokémon ao banco
            try:
                self.pokemon_repo.adicionaPokemon(pokemon_novo)
            except ValueError:
                pass
            
            # Vincular ao jogador
            nova_relacao = UsuarioPokemonORM(
                idUsuario=usuario_id,
                idPokemon=pokemon_adicionado_id
            )
            self.db.add(nova_relacao)
            self.db.commit()
            
            status.set_status(Status.SUCESSO)
            status.set_mensagem(f"Pokémon {pokemon_removido_id} trocado por {pokemon_adicionado_id} com sucesso")
            status.set_codigo("200")
            
            return status
            
        except Exception as e:
            self.db.rollback()
            status.set_status(Status.ERRO)
            status.set_mensagem(f"Erro ao trocar pokémon: {str(e)}")
            status.set_codigo("500")
            return status
    
    def trocar_entre_jogadores(self, sender_id: int, sender_poke_id: int, 
                               receiver_id: int, receiver_poke_id: int) -> StatusDistribuicao:
        """
        Realiza a troca entre jogador 1 e jogador 2.
        Remove pokémon 1 do sender e adiciona ao receiver, e vice-versa.
        """
        status = StatusDistribuicao()
        
        try:
            # Verificar se sender possui o pokémon
            sender_relacao = self.db.query(UsuarioPokemonORM).filter(
                UsuarioPokemonORM.idUsuario == sender_id,
                UsuarioPokemonORM.idPokemon == sender_poke_id
            ).first()
            
            if not sender_relacao:
                status.set_status(Status.ERRO)
                status.set_mensagem(f"Jogador {sender_id} não possui o pokémon {sender_poke_id}")
                status.set_codigo("404")
                return status
            
            # Verificar se receiver possui o pokémon
            receiver_relacao = self.db.query(UsuarioPokemonORM).filter(
                UsuarioPokemonORM.idUsuario == receiver_id,
                UsuarioPokemonORM.idPokemon == receiver_poke_id
            ).first()
            
            if not receiver_relacao:
                status.set_status(Status.ERRO)
                status.set_mensagem(f"Jogador {receiver_id} não possui o pokémon {receiver_poke_id}")
                status.set_codigo("404")
                return status
            
            # Verificar duplicatas
            sender_ja_tem = self.db.query(UsuarioPokemonORM).filter(
                UsuarioPokemonORM.idUsuario == sender_id,
                UsuarioPokemonORM.idPokemon == receiver_poke_id
            ).first()
            
            receiver_ja_tem = self.db.query(UsuarioPokemonORM).filter(
                UsuarioPokemonORM.idUsuario == receiver_id,
                UsuarioPokemonORM.idPokemon == sender_poke_id
            ).first()
            
            if sender_ja_tem or receiver_ja_tem:
                status.set_status(Status.ERRO)
                status.set_mensagem("Conflito: Um dos jogadores já possui o pokémon da troca")
                status.set_codigo("400")
                return status
            
            # Realizar a troca
            sender_relacao.idPokemon = receiver_poke_id
            receiver_relacao.idPokemon = sender_poke_id
            
            self.db.commit()
            
            status.set_status(Status.SUCESSO)
            status.set_mensagem(f"Troca realizada: Jogador {sender_id} ↔ Jogador {receiver_id}")
            status.set_codigo("200")
            
            return status
            
        except Exception as e:
            self.db.rollback()
            status.set_status(Status.ERRO)
            status.set_mensagem(f"Erro ao realizar troca: {str(e)}")
            status.set_codigo("500")
            return status
    
    def remover_jogador(self, usuario_id: int) -> StatusDistribuicao:
        """
        Remove completamente um jogador do banco de dados.
        """
        status = StatusDistribuicao()
        
        try:
            from .models import UsuarioORM
            
            # Verificar se usuário existe
            usuario = self.db.query(UsuarioORM).filter(
                UsuarioORM.idUsuario == usuario_id
            ).first()
            
            if not usuario:
                status.set_status(Status.ERRO)
                status.set_mensagem(f"Jogador {usuario_id} não encontrado")
                status.set_codigo("404")
                return status
            
            # Remover todas as relações de pokémons
            self.db.query(UsuarioPokemonORM).filter(
                UsuarioPokemonORM.idUsuario == usuario_id
            ).delete()
            
            # Remover usuário
            self.db.delete(usuario)
            self.db.commit()
            
            status.set_status(Status.SUCESSO)
            status.set_mensagem(f"Jogador {usuario_id} e seu time foram removidos do registro")
            status.set_codigo("200")
            
            return status
            
        except Exception as e:
            self.db.rollback()
            status.set_status(Status.ERRO)
            status.set_mensagem(f"Erro ao remover jogador: {str(e)}")
            status.set_codigo("500")
            return status
