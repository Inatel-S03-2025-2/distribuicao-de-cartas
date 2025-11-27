from .models import Pokemon, PokemonORM

def pokemon_to_orm_adapter(pokemon: Pokemon) -> PokemonORM:
    """Converte um objeto de Pokemon padrão para um objeto ORM."""
    return PokemonORM(
        idPokemon=pokemon.get_numero_pokedex(),
        nomePokemon=pokemon.get_nome(),
        isShiny=pokemon.is_shiny()
    )

def pokemon_orm_adapter(pokemon_orm: PokemonORM) -> Pokemon:
    """Converte um objeto ORM para um objeto de Pokemon padrão"""
    return Pokemon(
        numero_pokedex=pokemon_orm.idPokemon, # Usando o ID do BD
        nome=pokemon_orm.nomePokemon,
        shiny=pokemon_orm.isShiny
    )