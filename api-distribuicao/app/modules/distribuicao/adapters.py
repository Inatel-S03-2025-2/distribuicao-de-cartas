from src.jogador.Jogador import Jogador
from .models import Pokemon, PokemonORM, UsuarioORM

def pokemonToOrmAdapter(pokemon: Pokemon) -> PokemonORM:
    """Converte um objeto de Pokemon padrão para um objeto ORM."""
    return PokemonORM(
        idPokemon=pokemon.get_numero_pokedex(),
        nomePokemon=pokemon.get_nome(),
        isShiny=pokemon.is_shiny()
    )

def OrmTopokemonAdapter(pokemon_orm: PokemonORM) -> Pokemon:
    """Converte um objeto ORM para um objeto de Pokemon padrão"""
    return Pokemon(
        numero_pokedex=pokemon_orm.idPokemon, # Usando o ID do BD
        nome=pokemon_orm.nomePokemon,
        shiny=pokemon_orm.isShiny
    )

def UsuarioToOrmAdapter(usuario: Jogador) -> UsuarioORM:
    """Converte um objeto Jogador padrão em um Jogador ORM"""
    return UsuarioORM(
        idUsuario=usuario.get_id()
    )


def OrmToUsuarioAdapter(usuario_orm: UsuarioORM) -> Jogador:
    """"""
    return Jogador(
        id=usuario_orm.idUsuario,
        pokemons=usuario_orm.pokemons_colecao
    )