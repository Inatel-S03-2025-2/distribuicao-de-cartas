import pytest
from unittest.mock import Mock
from modules.distribuicao.service import GestorCartas
from modules.distribuicao.external import GestorAPI
from modules.distribuicao.models import Pokemon
from modules.distribuicao.repository import GerenciadorBD


@pytest.fixture
def mock_api():
    api = Mock(spec=GestorAPI)
    api.getMaxID.return_value = 151
    return api


@pytest.fixture
def mock_bd():
    bd = Mock(spec=GerenciadorBD)
    return bd


@pytest.fixture
def gestor_cartas(mock_api, mock_bd):
    GestorCartas._instance = None
    return GestorCartas(mock_api, mock_bd)


@pytest.fixture
def pokemon_mock():
    pokemon = Mock(spec=Pokemon)
    pokemon.get_nome.return_value = "Pikachu"
    pokemon.get_numero_pokedex.return_value = 25
    pokemon.is_shiny.return_value = False
    return pokemon


# Testes do método gerarPokemonsIniciais
def test_gerar_pokemons_iniciais_sucesso(gestor_cartas, mock_api, mock_bd, pokemon_mock):
    mock_api.getPokemon.return_value = pokemon_mock
    resultado = gestor_cartas.gerarPokemonsIniciais("jogador1")
    
    assert resultado["status"] == "sucesso"
    assert resultado["codigo"] == "200"
    assert len(resultado["pokemons"]) == 5


def test_gerar_pokemons_iniciais_cria_jogador(gestor_cartas, mock_api, mock_bd, pokemon_mock):
    mock_api.getPokemon.return_value = pokemon_mock
    gestor_cartas.gerarPokemonsIniciais("jogador1")
    
    mock_bd.createJogador.assert_called_once_with("jogador1")


def test_gerar_pokemons_iniciais_adiciona_ao_bd(gestor_cartas, mock_api, mock_bd, pokemon_mock):
    mock_api.getPokemon.return_value = pokemon_mock
    gestor_cartas.gerarPokemonsIniciais("jogador1")
    
    assert mock_bd.adicionarPokemon.call_count == 5


def test_gerar_pokemons_iniciais_vincula_jogador(gestor_cartas, mock_api, mock_bd, pokemon_mock):
    mock_api.getPokemon.return_value = pokemon_mock
    gestor_cartas.gerarPokemonsIniciais("jogador1")
    
    assert mock_bd.adicionarPokemonAoJogador.call_count == 5


def test_gerar_pokemons_iniciais_erro_api(gestor_cartas, mock_api):
    mock_api.getMaxID.side_effect = AttributeError("Erro na API")
    resultado = gestor_cartas.gerarPokemonsIniciais("jogador1")
    
    assert resultado["status"] == "erro"
    assert resultado["codigo"] == "500"


# Testes do método adicionarPokemon
def test_adicionar_pokemon_sucesso(gestor_cartas, mock_bd, pokemon_mock):
    resultado = gestor_cartas.adicionarPokemon(1, pokemon_mock)
    
    assert resultado["status"] == "sucesso"
    assert resultado["codigo"] == "200"
    assert "Pikachu foi adicionado" in resultado["mensagem"]


def test_adicionar_pokemon_chama_bd(gestor_cartas, mock_bd, pokemon_mock):
    gestor_cartas.adicionarPokemon(1, pokemon_mock)
    
    mock_bd.adicionarPokemon.assert_called_once_with(pokemon_mock)


def test_adicionar_pokemon_vincula_jogador(gestor_cartas, mock_bd, pokemon_mock):
    gestor_cartas.adicionarPokemon(1, pokemon_mock)
    
    mock_bd.adicionarPokemonAoJogador.assert_called_once_with(1, pokemon_mock)


def test_adicionar_pokemon_erro_inesperado(gestor_cartas, mock_bd, pokemon_mock):
    mock_bd.adicionarPokemon.side_effect = RuntimeError("Erro no banco")
    resultado = gestor_cartas.adicionarPokemon(1, pokemon_mock)
    
    assert resultado["status"] == "erro"
    assert resultado["codigo"] == "500"


# Testes do método removerPokemon
def test_remover_pokemon_sucesso(gestor_cartas, mock_bd, pokemon_mock):
    resultado = gestor_cartas.removerPokemon(1, pokemon_mock)
    
    assert resultado["status"] == "sucesso"
    assert resultado["codigo"] == "200"
    assert "Pikachu foi removido" in resultado["mensagem"]


def test_remover_pokemon_chama_bd(gestor_cartas, mock_bd, pokemon_mock):
    gestor_cartas.removerPokemon(1, pokemon_mock)
    
    mock_bd.removerPokemonDoJogador.assert_called_once_with(1, pokemon_mock)


def test_remover_pokemon_jogador_especifico(gestor_cartas, mock_bd, pokemon_mock):
    gestor_cartas.removerPokemon(123, pokemon_mock)
    
    assert mock_bd.removerPokemonDoJogador.call_args[0][0] == 123


# Testes do padrão Singleton
def test_singleton_mesma_instancia(mock_api, mock_bd):
    GestorCartas._instance = None
    gestor1 = GestorCartas(mock_api, mock_bd)
    gestor2 = GestorCartas(mock_api, mock_bd)
    
    assert gestor1 is gestor2


def test_singleton_nao_reinicializa(mock_api, mock_bd):
    GestorCartas._instance = None
    gestor1 = GestorCartas(mock_api, mock_bd)
    mock_api_novo = Mock(spec=GestorAPI)
    gestor2 = GestorCartas(mock_api_novo, mock_bd)
    
    assert gestor1 is gestor2
    assert gestor1._GestorCartas__api is mock_api