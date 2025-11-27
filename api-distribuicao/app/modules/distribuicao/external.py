import requests
from ...core.pokemon import Pokemon

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

    def getPokemon(self, numero_pokedex: int, shiny=False) -> Pokemon:
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
        
    def getMaxID(self) -> int:
        if not self.conexaoAPI():
            print("Erro de Conexão ao tentar buscar Max ID")
            return 1025 # Fallback para Gen 9
            
        url = f"{self.api_url}pokemon-species/?limit=1"
        
        try:
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                dados = response.json()
                # Retorna o total ou 1025 se a chave não existir
                return dados.get("count", 1025)
            else:
                print(f"Erro ao buscar Max ID. Status: {response.status_code}")
                return 1025 # Fallback para Gen 9
                
        except requests.exceptions.RequestException as e:
            print(f"Exceção ao buscar Max ID: {e}")
            return 1025 # Fallback para Gen 9