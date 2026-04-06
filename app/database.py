from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# String de conexão do PostgreSQL (Ajuste usuário, senha e banco)
# Formato: postgresql+psycopg2://usuario:senha@localhost:5432/nome_do_banco
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:suasenha@localhost:5432/efata_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependência para injetar a sessão do banco nas rotas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

