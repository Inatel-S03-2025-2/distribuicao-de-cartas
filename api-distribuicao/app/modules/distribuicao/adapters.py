from .models import Pokemon, PokemonORM

def pokemon_domain_to_orm(pokemon: Pokemon) -> PokemonORM:
    """Converte um objeto de Pokemon padrão para um objeto ORM."""
    return PokemonORM(
        nomePokemon=pokemon.get_numero_pokedex(),
        isShiny=pokemon.is_shiny()
    )

def pokemon_orm_to_domain(pokemon_orm: PokemonORM) -> Pokemon:
    """Converte um objeto ORM para um objeto de Pokemon padrão"""
    return Pokemon(
        numero_pokedex=pokemon_orm.idPokemon, # Usando o ID do BD
        nome=pokemon_orm.nomePokemon,
        shiny=pokemon_orm.isShiny
    )