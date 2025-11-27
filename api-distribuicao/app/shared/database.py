import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.environ.get("DB_USER", "fallback_user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "fallback_password")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "3306")
DB_NAME = os.environ.get("DB_NAME", "distribuicao_de_cartas")

DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_URL)

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

try:
    engine.connect()
    print("Conexão com o banco concluída com sucesso.")
except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")