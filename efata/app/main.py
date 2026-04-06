from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime

# Importações locais (vamos criar os models no futuro)
from .database import engine, Base, get_db

# Cria as tabelas no banco de dados (idealmente usaremos Alembic depois)
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Plataforma Éfata",
    description="API para atendimento online humanizado, agenda e vídeo.",
    version="1.0.0"
)

# Configuração de CORS (Essencial para o Frontend conseguir falar com o Backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção, coloque a URL do seu site
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "Éfata API está online e operante!"}

@app.post("/agendas/")
def criar_agenda(profissional_id: int, paciente_id: int, data_hora: datetime, db: Session = Depends(get_db)):
    """
    Endpoint provisório para testar a lógica de agendamento.
    Aqui entrarão as travas de limite semanal e diário.
    """
    # Lógica de validação virá aqui
    
    return {
        "mensagem": "Iniciando agendamento seguro...",
        "profissional": profissional_id,
        "paciente": paciente_id,
        "data_hora": data_hora,
        "status": "Em processamento"
    }