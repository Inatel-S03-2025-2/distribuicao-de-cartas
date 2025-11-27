"""
Configurações da aplicação
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Configurações centralizadas da aplicação"""
    
    # API
    API_TITLE = "API Distribuição de Cartas Pokémon"
    API_VERSION = "1.0.0"
    API_DESCRIPTION = "Serviço SOA para distribuição de pokémons aleatórios aos jogadores"
    
    # Database
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "distribuicao_de_cartas")
    
    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # PokeAPI
    POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/"
    POKEAPI_TIMEOUT = 5
    
    # Game Rules
    MAX_POKEMONS_PER_PLAYER = 5
    SHINY_PROBABILITY = 8192  # 1 em 8192 chance


settings = Settings()
