from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from ..core.config import settings

DB_URL = settings.DATABASE_URL
engine = create_engine(DB_URL)

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

try:
    engine.connect()
    print("✅ Conexão com o banco concluída com sucesso.")
except Exception as e:
    print(f"❌ Erro ao conectar ao banco de dados: {e}")