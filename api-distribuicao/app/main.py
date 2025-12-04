from fastapi import FastAPI
from modules.distribuicao.router import router as distribuicao_router

app = FastAPI()

# Rota principal (GET)
@app.get("/")
def home():
    return {"mensagem": "Olá! Minha API está viva."}

app.include_router(distribuicao_router, prefix="/api", tags=["Distribuição"])