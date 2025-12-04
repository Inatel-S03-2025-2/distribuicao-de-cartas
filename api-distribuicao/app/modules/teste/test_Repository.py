import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.distribuicao.models import Base, Pokemon, Jogador
from modules.distribuicao.repository import PokemonRepository, UsuarioRepository, UsuarioPokemonRepository

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def pokemon_repo(db_session):
    return PokemonRepository(db_session)


@pytest.fixture
def usuario_repo(db_session):
    return UsuarioRepository(db_session)


@pytest.fixture
def usuario_pokemon_repo(db_session, pokemon_repo, usuario_repo):
    return UsuarioPokemonRepository(db_session, pokemon_repo, usuario_repo)

# Testes envonveldno o pokemon repository

def test_create_pokemon(pokemon_repo):
    pokemon = Pokemon(1, "Bulbasaur")
    pokemon_repo.create(pokemon)
    assert pokemon_repo.exists(1)

def test_read_pokemon(pokemon_repo):
    pokemon = Pokemon(1, "Bulbasaur")
    pokemon_repo.create(pokemon)
    resultado = pokemon_repo.read(1)
    assert resultado.get_nome() == "Bulbasaur"

def test_delete_pokemon(pokemon_repo):
    pokemon = Pokemon(1, "Bulbasaur")
    pokemon_repo.create(pokemon)
    pokemon_repo.delete(pokemon)
    assert not pokemon_repo.exists(1)

def test_exists_pokemon(pokemon_repo):
    pokemon = Pokemon(1, "Bulbasaur")
    assert not pokemon_repo.exists(1)
    pokemon_repo.create(pokemon)
    assert pokemon_repo.exists(1)

def test_listar_todos_pokemons(pokemon_repo):
    pokemon1 = Pokemon(1, "Bulbasaur")
    pokemon2 = Pokemon(2, "Charmander")
    pokemon_repo.create(pokemon1)
    pokemon_repo.create(pokemon2)
    resultado = pokemon_repo.listarTodos()
    assert len(resultado) == 2

# Testes envolvendo o usuario(jogador) repository
def test_create_usuario(usuario_repo):
    jogador = Jogador("1", [])
    usuario_repo.create(jogador)
    assert usuario_repo.exists("1")

def test_read_usuario(usuario_repo):
    jogador = Jogador("1", [])
    usuario_repo.create(jogador)
    resultado = usuario_repo.read("1")
    assert resultado.get_id() == "1"

def test_delete_usuario(usuario_repo):
    jogador = Jogador("1", [])
    usuario_repo.create(jogador)
    usuario_repo.delete(jogador)
    assert not usuario_repo.exists("1")

def test_exists_usuario(usuario_repo):
    jogador = Jogador("1", [])
    assert not usuario_repo.exists("1")
    usuario_repo.create(jogador)
    assert usuario_repo.exists("1")

# Testes envolvendo o usuario(jogador) has pokemon repositoru
def test_adicionar_pokemon_jogador(usuario_pokemon_repo, pokemon_repo, usuario_repo):
    jogador = Jogador("1", [])
    pokemon = Pokemon(1, "Bulbasaur")
    usuario_repo.create(jogador)
    pokemon_repo.create(pokemon)
    usuario_pokemon_repo.adicionarPokemonJogador("1", pokemon)
    assert usuario_pokemon_repo.usuarioPossuiPokemon("1", 1)

def test_remover_pokemon_jogador(usuario_pokemon_repo, pokemon_repo, usuario_repo):
    jogador = Jogador("1", [])
    pokemon = Pokemon(1, "Bulbasaur")
    usuario_repo.create(jogador)
    pokemon_repo.create(pokemon)
    usuario_pokemon_repo.adicionarPokemonJogador("1", pokemon)
    resultado = usuario_pokemon_repo.removerPokemonJogador("1", 1)
    assert resultado is True
    assert not usuario_pokemon_repo.usuarioPossuiPokemon("1", 1)

def test_listar_pokemons_do_usuario(usuario_pokemon_repo, pokemon_repo, usuario_repo):
    jogador = Jogador("1", [])
    pokemon1 = Pokemon(1, "Bulbasaur")
    pokemon2 = Pokemon(2, "Charmander")
    usuario_repo.create(jogador)
    pokemon_repo.create(pokemon1)
    pokemon_repo.create(pokemon2)
    usuario_pokemon_repo.adicionarPokemonJogador("1", pokemon1)
    usuario_pokemon_repo.adicionarPokemonJogador("1", pokemon2)
    resultado = usuario_pokemon_repo.listarPokemonsDoUsuario("1")
    assert len(resultado) == 2