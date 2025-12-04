import sys
import pytest
from unittest.mock import MagicMock, patch

import requests
from modules.distribuicao.external import GestorAPI 

mock_pokemon_module = MagicMock()

class PokemonMock:
    def __init__(self, numero_pokedex, nome, shiny):
        self.numero_pokedex = numero_pokedex
        self.nome = nome
        self.shiny = shiny

mock_pokemon_module.Pokemon = PokemonMock
sys.modules['modules.distribuicao.models'] = mock_pokemon_module


@pytest.fixture(autouse=True)
def reset_singleton():
    # Esta fixture roda automaticamente antes de CADA teste.
    # Ela garante que a instância Singleton seja resetada 
    # senão o teste A poderia sujar o estado do teste B.
    GestorAPI._instance = None
    yield
    GestorAPI._instance = None

@pytest.fixture
def gestor():
    # Retorna uma instância limpa do gestor para ser usada nos testes
    return GestorAPI()


# =================== TESTES GESTOR API ==================
class TestConexao:
    @patch('requests.get')
    def test_conexao_sucesso(self, mock_get, gestor):
        mock_get.return_value.status_code = 200
        resultado = gestor.conexaoAPI()
        assert resultado is True

    @patch('requests.get')
    def test_conexao_falha_500(self, mock_get, gestor):
        mock_get.return_value.status_code = 500
        assert gestor.conexaoAPI() is False

    @patch('requests.get')
    def test_conexao_exception(self, mock_get, gestor):
        mock_get.side_effect = requests.exceptions.RequestException
        assert gestor.conexaoAPI() is False


class TestGetPokemon:
    @patch.object(GestorAPI, 'conexaoAPI', return_value=True)
    @patch('requests.get')
    def test_get_pokemon_sucesso(self, mock_get, mock_conn, gestor):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "forms": [{"name": "charizard"}]
        }

        pokemon = gestor.getPokemon(6, shiny=True)

        assert pokemon is not None
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