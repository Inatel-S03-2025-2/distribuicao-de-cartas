from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.jogador.Jogador import Jogador
from .models import UsuarioORM, UsuarioPokemonORM, PokemonORM, Pokemon
from .adapters import pokemonToOrmAdapter, UsuarioToOrmAdapter

'''
Definir a classe repository (gerenciaBD)
class repository[T]
'''

class PokemonRepository:
    def __init__(self, db: Session):
        self.db = db

    def adicionaPokemon(self, pokemon: Pokemon):
        """Apenas adiciona o pokemon. Erro se já existir."""
        pokemon_orm = self.db.query(PokemonORM).filter(
            PokemonORM.idPokemon == pokemon.get_numero_pokedex()
        ).first()

        if pokemon_orm:
            raise ValueError("Pokémon já existe")

        novo_pokemon_orm = pokemonToOrmAdapter(pokemon)
        try:
            self.db.add(novo_pokemon_orm)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise ValueError(f"Erro ao adicionar pokemon: {pokemon}")


    def buscaPokeId(self, numero_pokedex: int) -> PokemonORM:
        """Busca um Pokémon existente por id"""
        pokemon_orm = self.db.query(PokemonORM).filter(
            PokemonORM.idPokemon == numero_pokedex
        ).first()

        if pokemon_orm is None:
            raise ValueError(f"Pokémon com ID {numero_pokedex} não encontrado")

        return pokemon_orm

class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def adicionaUsuario(self, usuario: Jogador):
        """Apenas adiciona um jogador. Erro se ele já existir."""
        usuario_orm = self.db.query(UsuarioORM).filter(
            UsuarioORM.idUsuario == usuario.get_id()
        ).first()

        if usuario_orm is None:
            raise ValueError(f"")

        novo_usuario_orm = UsuarioToOrmAdapter(usuario)

        try:
            self.db.add(novo_usuario_orm)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise ValueError(f"Erro ao adicionar usuario: {usuario}")


class UsuarioPokemonRepository:
    def __init__(self, db: Session, pokemon_repo: PokemonRepository):
        self.db = db
        self.pokemon_repo = pokemon_repo

    def adicionarPokemonUsuario(self, id_usuario: int, pokemon: Pokemon):
        """Adiciona um pokemon ao jogador. Erro se ele já possuiir o pokemon com o mesmo id."""
        # garantindo primeiro que o Pokémon existe na tabela Pokemon
        pokemon_persisted = self.pokemon_repo.buscaPokeId(
            pokemon.get_numero_pokedex()
        )

        nova_carta = UsuarioPokemonORM(
            idUsuario=id_usuario,
            idPokemon=pokemon_persisted.idPokemon,
        )

        try:
            self.db.add(nova_carta)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise ValueError(
                "O usuário já tem esse Pokémon (combinação de ID de Usuário e ID de Pokémon já existente).")