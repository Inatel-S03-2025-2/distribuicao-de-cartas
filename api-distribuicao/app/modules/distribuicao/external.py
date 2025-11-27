# %%
import requests
from .models import Pokemon

class GestorAPI:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init_once(*args, **kwargs)
        return cls._instance

    def __init_once(self, api_url="https://pokeapi.co/api/v2/"):
        self.api_url = api_url

    def conexaoAPI(self):
        try:
            response = requests.get(self.api_url, timeout=5)
            
            if response.status_code == 200:
                print("Conexão realizada.")
                return True
            else:
                print(f"Falha ao conectar. Status: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"Ocorreu um erro de conexão: {e}")
            return False

    def getPokemon(self, numero_pokedex: int, shiny=False)->Pokemon:
        if not self.conexaoAPI():
            print("Erro de Conexão com a API")
            return None
             
        url_pokemon = f"{self.api_url}pokemon/{numero_pokedex}/"
        try:
            response = requests.get(url_pokemon)
            
            if response.status_code == 200:
                dados_json = response.json()
                lista_forms = dados_json.get("forms", [])

                if lista_forms:
                    nome_pokemon = lista_forms[0]["name"]
                else:
                    nome_pokemon = "Nome Desconhecido"

                pokemon = Pokemon(
                    numero_pokedex=numero_pokedex,
                    nome=nome_pokemon,
                    shiny=shiny
                )
                return pokemon
            
            elif response.status_code == 404:
                print(f"Erro: Pokémon com o número {numero_pokedex} não encontrado.")
                return None
            
            else:
                print(f"Erro ao acessar a API. Código de status: {response.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Ocorreu um erro de conexão: {e}")
            return None

# %%
