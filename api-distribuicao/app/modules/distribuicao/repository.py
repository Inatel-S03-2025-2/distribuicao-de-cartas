from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .models import UsuarioORM, UsuarioPokemonORM, PokemonORM, Pokemon
from .adapters import pokemon_to_orm_adapter

class PokemonRepository:
    def __init__(self, db: Session):
        self.db = db

    def adicionaPokemon(self, pokemon: Pokemon):
        """Apenas adiciona. Erro se já existir."""
        pokemon_orm = self.db.query(PokemonORM).filter(
            PokemonORM.idPokemon == pokemon.get_numero_pokedex()
        ).first()

        if pokemon_orm:
            raise ValueError("Pokémon já existe")

        novo_pokemon_orm = pokemon_to_orm_adapter(pokemon)
        self.db.add(novo_pokemon_orm)
        self.db.commit()

    def buscar_por_id(self, numero_pokedex: int) -> PokemonORM:
        """Busca um Pokémon existente"""
        pokemon_orm = self.db.query(PokemonORM).filter(
            PokemonORM.idPokemon == numero_pokedex
        ).first()

        if pokemon_orm is None:
            raise ValueError(f"Pokémon com ID {numero_pokedex} não encontrado")

        return pokemon_orm

class UsuarioPokemonRepository:
    def __init__(self, db: Session, pokemon_repo: PokemonRepository):
        self.db = db
        self.pokemon_repo = pokemon_repo

    def adicionar_pokemon_ao_usuario(self, id_usuario: int, pokemon: Pokemon):
        # garantindo primeiro que o Pokémon existe na tabela Pokemon
        pokemon_persisted = self.pokemon_repo.buscar_por_id(
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