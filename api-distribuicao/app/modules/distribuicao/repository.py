from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound

from modules.distribuicao.models import UsuarioORM, UsuarioPokemonORM, PokemonORM, Pokemon, Jogador
from .adapters import pokemonToOrmAdapter, OrmTopokemonAdapter, UsuarioToOrmAdapter, OrmToUsuarioAdapter


class PokemonRepository:
    def __init__(self, db: Session):
        self.db = db

    def adicionaPokemon(self, pokemon: Pokemon):
        """Adiciona um pokémon. Erro se já existir."""
        if self.existe(pokemon.get_numero_pokedex()):
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

    def removePokemon(self, pokemon: Pokemon):
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

    def buscaPokeId(self, id_pokemon: int) -> Pokemon:
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

    def existe(self, numero_pokedex: int) -> bool:
        """Verifica se um pokémon existe"""
        return (
            self.db.query(PokemonORM)
            .filter(PokemonORM.idPokemon == numero_pokedex)
            .first()
            is not None
        )

class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def adicionaUsuario(self, usuario: Jogador):
        """Adiciona um jogador. Erro se já existir."""
        if self.existe(usuario.get_id()):
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

    def removeUsuario(self, usuario: Jogador):
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

    def buscaPorId(self, id_usuario: str) -> Jogador:
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

    def existe(self, id_usuario: str) -> bool:
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
        if not self.usuario_repo.existe(id_usuario):
            raise ValueError(f"Usuário com ID {id_usuario} não encontrado")

        # Garante que o Pokémon existe
        pokemon_entidade = self.pokemon_repo.buscaPokeId(
            pokemon.get_numero_pokedex()
        )

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
        if not self.usuario_repo.existe(id_usuario):
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
