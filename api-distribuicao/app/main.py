from fastapi import FastAPI

app = FastAPI()

# Rota principal (GET)
@app.get("/")
def home():
    return {"mensagem": "Olá! Minha API está viva."}