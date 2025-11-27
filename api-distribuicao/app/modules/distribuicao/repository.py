from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .models import UsuarioORM, UsuarioPokemonORM, PokemonORM, Pokemon
from .adapters import pokemon_domain_to_orm

class PokemonRepository:
    def __init__(self, db: Session):
        self.db = db

    def criar_ou_obter_pokemon(self, pokemon_domain: Pokemon) -> PokemonORM:
        """Salva o Pokémon na tabela Pokemon se ainda não existirou retorna o existente"""
        # Tenta encontrar o Pokémon na base
        # Se você tiver um ID único da PokeAPI, use ele para a busca.
        pokemon_orm = self.db.query(PokemonORM).filter(
            PokemonORM.nomePokemon == pokemon_domain.get_nome()
        ).first()

        if pokemon_orm:
            return pokemon_orm  # Ja existe no BD

        # Se não existe, adapta e salva o novo Pokémon
        novo_pokemon_orm = pokemon_domain_to_orm(pokemon_domain)
        self.db.add(novo_pokemon_orm)
        self.db.flush()  # Força a geração do ID
        return novo_pokemon_orm

class UsuarioPokemonRepository:
    def __init__(self, db: Session, pokemon_repo: PokemonRepository):
        self.db = db
        self.pokemon_repo = pokemon_repo

    def adicionar_pokemon_ao_usuario(self, id_usuario: int, pokemon_domain: Pokemon) -> UsuarioPokemonORM:
        # garantindo primeiro que o Pokémon existe na tabela Pokemon
        pokemon_persisted = self.pokemon_repo.criar_ou_obter_pokemon(pokemon_domain)

        # Cria a nova carta de relacionamento (UsuarioPokemon)
        nova_carta = UsuarioPokemonORM(
            idUsuario=id_usuario,
            idPokemon=pokemon_persisted.idPokemon,
        )

        try:
            self.db.add(nova_carta)
            self.db.flush()
            return nova_carta
        except IntegrityError:
            self.db.rollback()
            raise ValueError(
                "O usuário já tem esse Pokémon (combinação de ID de Usuário e ID de Pokémon já existente).")