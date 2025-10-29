import requests

class GestorAPI():
    def __init__(self, api_url="https://pokeapi.co/api/v2/"):
        self.api_url = api_url

    def conexãoAPI(self):
        try:
            response = requests.get(self.base_url, timeout=5)
            
            if response.status_code == 200:
                print("Conexão realizada.")
                return True
            else:
                print(f"Falha ao conectar. Status: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"Ocorreu um erro de conexão: {e}")
            return False

    def getPokemon(self, numero_pokedex: int):
        if not GestorAPI.conexãoAPI():
            print("Erro de Conexão com a API")
            return None
             
        url_pokemon = f"{self.api_url}pokemon/{numero_pokedex}/"
        try:
            response = requests.get(url_pokemon)
            
            if response.status_code == 200:
                dados_json = response.json()
                
                nome = dados_json['name'].capitalize()
                pokedex_id = dados_json['id']
                
                # TODO: Mudar para objeto pokemon
                pokemon_dict ={ 
                    nome:nome,
                    pokedex_id:pokedex_id,
                }
                return pokemon_dict
            
            elif response.status_code == 404:
                print(f"Erro: Pokémon com o número {numero_pokedex} não encontrado.")
                return None
            
            else:
                print(f"Erro ao acessar a API. Código de status: {response.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Ocorreu um erro de conexão: {e}")
            return None