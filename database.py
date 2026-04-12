from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# O caminho do banco de dados (SQLite local)
SQLALCHEMY_DATABASE_URL = "sqlite:///./banco_sistema.db"

# O motor que faz a comunicação entre o Python e o Banco de Dados
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# A sessão é a nossa "porta de entrada" para fazer consultas (SELECT) e alterações (INSERT, UPDATE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base que todos os nossos modelos vão herdar
Base = declarative_base()

# Função auxiliar para injetar o banco de dados nas nossas rotas da API futuramente
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()