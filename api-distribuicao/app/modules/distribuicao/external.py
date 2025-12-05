import requests
from .models import Pokemon

class GestorAPI:
    _instance = None
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, api_url="https://pokeapi.co/api/v2/"):
        if not GestorAPI._initialized:
            self.api_url = api_url
            GestorAPI._initialized = True

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

    def getPokemon(self, numero_pokedex: int, shiny=False) -> Pokemon:
        url_pokemon = f"{self.api_url}pokemon/{numero_pokedex}/"
        try:
            response = requests.get(url_pokemon, timeout=5)
            
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
                return None
            
            else:
                return None

        except requests.exceptions.RequestException as e:
            return None
        
    def getMaxID(self) -> int:
        url = f"{self.api_url}pokemon-species/?limit=1"
        
        try:
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                dados = response.json()
                # Retorna o total ou 1025 se a chave não existir
                return dados.get("count", 1025)
            else:
                return 1025 # Fallback para Gen 9
                
        except requests.exceptions.RequestException as e:
            return 1025 # Fallback para Gen 9