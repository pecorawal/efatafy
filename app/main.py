from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

# Importações internas do seu projeto
from app.database import engine, get_db, Base
from app import models  # Certifique-se de ter o arquivo app/models.py

# Inicializa as tabelas no banco de dados assim que o app sobe
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Plataforma Éfatafy",
    description="Atendimento humanizado com tecnologia de ponta.",
    version="1.0.0"
)

# Configuração de CORS (Permite que Web, Tablet e Mobile acessem a API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {
        "status": "Online",
        "ambiente": "Python 3.12",
        "projeto": "Éfatafy"
    }

@app.post("/agendar", tags=["Agendamento"])
def realizar_agendamento(
    profissional_id: int, 
    paciente_id: int, 
    data_hora: datetime, 
    db: Session = Depends(get_db)
):
    """
    Realiza o agendamento verificando:
    1. Limite de 10h diárias para o profissional.
    2. Limite de 3 sessões semanais para o paciente.
    """
    
    # --- REGRA 1: Limite do Profissional (10h/dia) ---
    inicio_dia = data_hora.replace(hour=0, minute=0, second=0, microsecond=0)
    fim_dia = inicio_dia + timedelta(days=1)
    
    contagem_profissional = db.query(models.Agendamento).filter(
        models.Agendamento.profissional_id == profissional_id,
        models.Agendamento.data_hora >= inicio_dia,
        models.Agendamento.data_hora < fim_dia
    ).count()

    if contagem_profissional >= 10:
        raise HTTPException(
            status_code=400, 
            detail="Este profissional já atingiu o limite de 10 horas de atendimento para este dia."
        )

    # --- REGRA 2: Limite do Paciente (3 sessões/semana) ---
    # Pegamos o início da semana (segunda-feira)
    inicio_semana = data_hora - timedelta(days=data_hora.weekday())
    inicio_semana = inicio_semana.replace(hour=0, minute=0, second=0, microsecond=0)
    
    contagem_paciente = db.query(models.Agendamento).filter(
        models.Agendamento.paciente_id == paciente_id,
        models.Agendamento.data_hora >= inicio_semana,
        models.Agendamento.data_hora < inicio_semana + timedelta(days=7)
    ).count()

    if contagem_paciente >= 3:
        raise HTTPException(
            status_code=400, 
            detail="Limite de 3 agendamentos semanais atingido para este paciente."
        )

    # --- SUCESSO: Salva no Banco ---
    novo_agendamento = models.Agendamento(
        profissional_id=profissional_id,
        paciente_id=paciente_id,
        data_hora=data_hora
    )
    
    db.add(novo_agendamento)
    db.commit()
    db.refresh(novo_agendamento)
    
    return {
        "status": "sucesso",
        "mensagem": "Consulta agendada! Notificações enviadas para WhatsApp e E-mail.",
        "dados": novo_agendamento
    }