"""
Main - Ponto de entrada da aplicação FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .modules.distribuicao.router import router as distribuicao_router


# Inicializa a aplicação FastAPI
app = FastAPI(
    title="API de Distribuição de Pokémons",
    description="Sistema de distribuição e gerenciamento de pokémons para jogadores",
    version="1.0.0"
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota de health check
@app.get("/")
def home():
    """
    Health check endpoint.
    Verifica se a API está funcionando.
    """
    return {
        "status": "online",
        "mensagem": "API de Distribuição de Pokémons está funcionando",
        "versao": "1.0.0"
    }


# Incluir routers
app.include_router(distribuicao_router)