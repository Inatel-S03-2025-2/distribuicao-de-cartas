from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

DB_URL = 'mysql+pymysql://root:zSh3rl0cK$20@localhost:3306/distribuicao_de_cartas'
engine = create_engine(DB_URL)

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

try:
    engine.connect()
    print("Conexão com o banco concluída com sucesso.")
except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")