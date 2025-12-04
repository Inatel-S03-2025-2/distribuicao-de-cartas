from fastapi import FastAPI
from app.modules.distribuicao.router import router as distribuicao_router
from shared.database import SessionLocal

app = FastAPI()

# Rota principal (GET)
@app.get("/")
def home():
    return {"mensagem": "Olá! Minha API está viva."}

app.include_router(distribuicao_router, prefix="/api", tags=["Distribuição"])

session = SessionLocal()
session.rollback()
session.close()