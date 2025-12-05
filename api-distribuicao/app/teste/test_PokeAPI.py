import pytest
from unittest.mock import MagicMock, patch
import requests

from modules.distribuicao.external import GestorAPI 

class PokemonMock:
    def __init__(self, numero_pokedex, nome, shiny=False): 
        self.numero_pokedex = numero_pokedex
        self.nome = nome # O teste acessa .nome direto
        self.shiny = shiny
    
    def __eq__(self, other):
        # Permite comparar: if pokemon_retornado == PokemonMock(...)
        return (self.numero_pokedex == other.numero_pokedex and 
                self.nome == other.nome)


@pytest.fixture(autouse=True)
def reset_singleton():
    """Reseta o Singleton antes de cada teste"""
    GestorAPI._instance = None
    yield
    GestorAPI._instance = None

@pytest.fixture
def gestor():
    return GestorAPI()

# =================== TESTES ==================

class TestConexao:
    @patch('requests.get')
    def test_conexao_sucesso(self, mock_get, gestor):
        mock_get.return_value.status_code = 200
        assert gestor.conexaoAPI() is True

    @patch('requests.get')
    def test_conexao_falha_500(self, mock_get, gestor):
        mock_get.return_value.status_code = 500
        assert gestor.conexaoAPI() is False

    @patch('requests.get')
    def test_conexao_exception(self, mock_get, gestor):
        mock_get.side_effect = requests.exceptions.RequestException
        assert gestor.conexaoAPI() is False


# APLICAMOS O PATCH AQUI NA CLASSE INTEIRA
# Isso substitui 'modules.distribuicao.external.Pokemon' pelo nosso 'PokemonMock'
# Assim, quando o GestorAPI chamar Pokemon(...), ele chamará PokemonMock(...)
@patch('modules.distribuicao.external.Pokemon', new=PokemonMock)
class TestGetPokemon:
    
    @patch.object(GestorAPI, 'conexaoAPI', return_value=True)
    @patch('requests.get')
    def test_get_pokemon_sucesso(self, mock_get, mock_conn, gestor):
        # Configura o retorno da API
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "forms": [{"name": "charizard"}]
        }

        # Executa
        pokemon = gestor.getPokemon(6, shiny=True)

        # Asserts
        assert pokemon is not None
        # Agora funciona, pois 'pokemon' é uma instância de PokemonMock
        assert pokemon.nome == "charizard" 
        assert pokemon.numero_pokedex == 6
        assert pokemon.shiny is True

    @patch.object(GestorAPI, 'conexaoAPI', return_value=True)
    @patch('requests.get')
    def test_get_pokemon_404_nao_encontrado(self, mock_get, mock_conn, gestor):
        mock_get.return_value.status_code = 404
        pokemon = gestor.getPokemon(9999)
        assert pokemon is None

    @patch.object(GestorAPI, 'conexaoAPI', return_value=False)
    def test_get_pokemon_sem_conexao(self, mock_conn, gestor):
        pokemon = gestor.getPokemon(1)
        assert pokemon is None


class TestMaxID:
    @patch.object(GestorAPI, 'conexaoAPI', return_value=True)
    @patch('requests.get')
    def test_get_max_id_sucesso(self, mock_get, mock_conn, gestor):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"count": 1500}
        assert gestor.getMaxID() == 1500

    @patch.object(GestorAPI, 'conexaoAPI', return_value=False)
    def test_get_max_id_fallback_sem_conexao(self, mock_conn, gestor):
        assert gestor.getMaxID() == 1025

    @patch.object(GestorAPI, 'conexaoAPI', return_value=True)
    @patch('requests.get')
    def test_get_max_id_erro_json(self, mock_get, mock_conn, gestor):
        mock_get.side_effect = requests.exceptions.RequestException
        assert gestor.getMaxID() == 1025

def test_singleton_padrao():
    g1 = GestorAPI()
    g2 = GestorAPI()
    assert g1 is g2