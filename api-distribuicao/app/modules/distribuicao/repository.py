from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound

from shared.database import SessionLocal
from modules.distribuicao.models import Jogador, UsuarioORM, UsuarioPokemonORM, PokemonORM, Pokemon
from modules.distribuicao.adapters import pokemonToOrmAdapter, OrmTopokemonAdapter, UsuarioToOrmAdapter, \
    OrmToUsuarioAdapter

class IRepository(ABC):
    """Interface base para repositórios"""

    @abstractmethod
    def create(self, entity):
        """Adiciona uma entidade"""
        pass

    @abstractmethod
    def read(self, id):
        """Busca uma entidade por ID"""
        pass

    @abstractmethod
    def delete(self, entity):
        """Remove uma entidade"""
        pass

    @abstractmethod
    def exists(self, id) -> bool:
        """Verifica se uma entidade existe"""
        pass


class GerenciadorBD:

    def __init__(self):
        self.conexaoBD()

    def conexaoBD(self):
        self.session = SessionLocal()
        self.session.rollback()

    def createJogador(self, jogador: Jogador):
        usuario_repo = UsuarioRepository(self.session)
        usuario_repo.create(jogador)
        return True

    def readJogador(self, id_jogador: str) -> Jogador:
        usuario_repo = UsuarioRepository(self.session)
        return usuario_repo.read(id_jogador)

    def deleteJogador(self, jogador: Jogador):
        usuario_repo = UsuarioRepository(self.session)
        usuario_repo.delete(jogador)
        return True
    
    def getPokemonsDoJogador(self, id_jogador: str) -> list[Pokemon]:
        usuario_repo = UsuarioRepository(self.session)
        pokemon_repo = PokemonRepository(self.session)
        usuario_pokemon_repo = UsuarioPokemonRepository(self.session, pokemon_repo, usuario_repo)
        return usuario_pokemon_repo.listarPokemonsDoUsuario(id_jogador)

    def removerPokemonDoJogador(self, id_jogador: str, id_pokemon: int) -> bool:
        usuario_repo = UsuarioRepository(self.session)
        pokemon_repo = PokemonRepository(self.session)
        usuario_pokemon_repo = UsuarioPokemonRepository(self.session, pokemon_repo, usuario_repo)
        return usuario_pokemon_repo.removerPokemonJogador(id_jogador, id_pokemon)
    
    def adicionarPokemonAoJogador(self, id_jogador: str, pokemon: Pokemon):
        usuario_repo = UsuarioRepository(self.session)
        pokemon_repo = PokemonRepository(self.session)
        usuario_pokemon_repo = UsuarioPokemonRepository(self.session, pokemon_repo, usuario_repo)
        usuario_pokemon_repo.adicionarPokemonJogador(id_jogador, pokemon)
        return True

class PokemonRepository(IRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, pokemon: Pokemon):
        """Adiciona um pokémon. Erro se já existir."""
        if self.exists(pokemon.get_numero_pokedex()):
            raise ValueError(
                f"Pokémon com ID {pokemon.get_numero_pokedex()} já existe"
            )

        novo_pokemon_orm = pokemonToOrmAdapter(pokemon)
        try:
            self.db.add(novo_pokemon_orm)
            self.db.commit()
            self.db.refresh(novo_pokemon_orm)
        except IntegrityError as e:
            self.db.rollback()
            raise ValueError(f"Erro ao adicionar pokémon: {e}")

    def delete(self, pokemon: Pokemon):
        """Remove um pokémon. Erro se não existir."""
        pokemon_orm = self.db.query(PokemonORM).filter(
            PokemonORM.idPokemon == pokemon.get_numero_pokedex()
        ).first()

        if pokemon_orm is None:
            raise ValueError(
                f"Pokémon com ID {pokemon.get_numero_pokedex()} não encontrado"
            )

        try:
            self.db.delete(pokemon_orm)
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise ValueError(f"Erro ao remover pokémon: {e}")

    def read(self, id_pokemon: int) -> Pokemon:
        """Busca um Pokémon pelo ID da tabela e retorna entidade de domínio"""
        pokemon_orm = self.db.query(PokemonORM).filter(
            PokemonORM.idPokemon == id_pokemon
        ).first()

        if pokemon_orm is None:
            raise ValueError(f"Pokémon com ID {id_pokemon} não encontrado")

        return OrmTopokemonAdapter(pokemon_orm)

    def listarTodos(self) -> list[Pokemon]:
        """Retorna todos os pokémons como entidades de domínio"""
        pokemons_orm = self.db.query(PokemonORM).all()
        return [OrmTopokemonAdapter(p) for p in pokemons_orm]

    def exists(self, numero_pokedex: int) -> bool:
        """Verifica se um pokémon existe"""
        return (
            self.db.query(PokemonORM)
            .filter(PokemonORM.idPokemon == numero_pokedex)
            .first()
            is not None
        )

class UsuarioRepository(IRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, usuario: Jogador):
        """Adiciona um jogador. Erro se já existir."""
        if self.exists(usuario.get_id()):
            raise ValueError(
                f"Usuário com ID {usuario.get_id()} já existe"
            )

        novo_usuario_orm = UsuarioToOrmAdapter(usuario)

        try:
            self.db.add(novo_usuario_orm)
            self.db.commit()
            self.db.refresh(novo_usuario_orm)
        except IntegrityError as e:
            self.db.rollback()
            raise ValueError(f"Erro ao adicionar usuário: {e}")

    def delete(self, usuario: Jogador):
        """Remove um jogador."""
        usuario_orm = (
            self.db.query(UsuarioORM)
            .filter(UsuarioORM.idUsuario == usuario.get_id())
            .first()
        )

        if usuario_orm is None:
            raise ValueError(
                f"Usuário com ID {usuario.get_id()} não encontrado"
            )

        try:
            self.db.delete(usuario_orm)
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise ValueError(f"Erro ao remover usuário: {e}")

    def read(self, id_usuario: str) -> Jogador:
        """Busca um usuário por ID."""
        usuario_orm = (
            self.db.query(UsuarioORM)
            .filter(UsuarioORM.idUsuario == id_usuario)
            .first()
        )

        if usuario_orm is None:
            raise ValueError(
                f"Usuário com ID {id_usuario} não encontrado"
            )

        return OrmToUsuarioAdapter(usuario_orm)

    def exists(self, id_usuario: str) -> bool:
        """Verifica se o usuário existe."""
        return (
            self.db.query(UsuarioORM)
            .filter(UsuarioORM.idUsuario == id_usuario)
            .first()
            is not None
        )

class UsuarioPokemonRepository:
    def __init__(self, db: Session, pokemon_repo: PokemonRepository, usuario_repo: UsuarioRepository):
        self.db = db
        self.pokemon_repo = pokemon_repo
        self.usuario_repo = usuario_repo

    def adicionarPokemonJogador(self, id_usuario: str, pokemon: Pokemon):
        """Adiciona um pokémon ao jogador."""
        if not self.usuario_repo.exists(id_usuario):
            raise ValueError(f"Usuário com ID {id_usuario} não encontrado")

        # Garante que o Pokémon existe
        self.pokemon_repo.read(pokemon.get_numero_pokedex())

        nova_carta = UsuarioPokemonORM(
            idUsuario=id_usuario,
            idPokemon=pokemon.get_numero_pokedex(),
        )

        try:
            self.db.add(nova_carta)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise ValueError(
                f"Usuário {id_usuario} já possui o Pokémon {pokemon.get_numero_pokedex()}"
            )

    def removerPokemonJogador(self, id_usuario: str, id_pokemon: int) -> bool:
        """Remove um pokémon da coleção do jogador."""
        try:
            relacao = (
                self.db.query(UsuarioPokemonORM).filter(
                    UsuarioPokemonORM.idUsuario == id_usuario,
                    UsuarioPokemonORM.idPokemon == id_pokemon,
                ).one()
            )

            self.db.delete(relacao)
            self.db.commit()
            return True

        except NoResultFound:
            return False

    def listarPokemonsDoUsuario(self, id_usuario: str) -> list[Pokemon]:
        """Lista todos os pokémons de um usuário."""
        if not self.usuario_repo.exists(id_usuario):
            raise ValueError(f"Usuário com ID {id_usuario} não encontrado")

        # join para buscar os poke
        resultados = (
            self.db.query(PokemonORM)
            .join(UsuarioPokemonORM, PokemonORM.idPokemon == UsuarioPokemonORM.idPokemon)
            .filter(UsuarioPokemonORM.idUsuario == id_usuario)
            .all()
        )

        return [OrmTopokemonAdapter(pokemon_orm) for pokemon_orm in resultados]

    def usuarioPossuiPokemon(self, id_usuario: str, id_pokemon: int) -> bool:
        """Verifica se o usuário possui um Pokémon."""
        return (
            self.db.query(UsuarioPokemonORM)
            .filter(
                UsuarioPokemonORM.idUsuario == id_usuario,
                UsuarioPokemonORM.idPokemon == id_pokemon,
            ).first() is not None
        )