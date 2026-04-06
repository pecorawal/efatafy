from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import declarative_base, relationship
from pgvector.sqlalchemy import Vector # Para o banco de dados vetorial
from datetime import datetime

Base = declarative_base()

class Profissional(Base):
    __tablename__ = 'profissionais'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    foto_perfil_url = Column(String(255))
    registro_conselho = Column(String(50), nullable=False) # CRP ou CREFITO
    especialidades = Column(String(255)) # Ex: "Ansiedade, Depressão, Luto" (Máx 5)
    descricao = Column(String(500)) # Limite de 500 caracteres
    pontuacao = Column(Float, default=5.0)
    agendas = relationship("Agenda", back_populates="profissional")

class Paciente(Base):
    __tablename__ = 'pacientes'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    forma_pagamento = Column(String(20)) # pix, credito, debito
    pontuacao = Column(Float, default=0.0)
    agendas = relationship("Agenda", back_populates="paciente")

class Agenda(Base):
    __tablename__ = 'agendas'
    id = Column(Integer, primary_key=True)
    profissional_id = Column(Integer, ForeignKey('profissionais.id'))
    paciente_id = Column(Integer, ForeignKey('pacientes.id'))
    data_hora_inicio = Column(DateTime, nullable=False)
    data_hora_fim = Column(DateTime, nullable=False)
    status = Column(String(20), default="agendado") # agendado, concluido, cancelado
    link_sala_video = Column(String(255))
    
    profissional = relationship("Profissional", back_populates="agendas")
    paciente = relationship("Paciente", back_populates="agendas")
    sessao_dados = relationship("SessaoIA", back_populates="agenda", uselist=False)

class SessaoIA(Base):
    """Tabela que guarda a transcrição vetorial para uso futuro de IA"""
    __tablename__ = 'sessoes_ia'
    id = Column(Integer, primary_key=True)
    agenda_id = Column(Integer, ForeignKey('agendas.id'))
    transcricao_texto = Column(Text)
    transcricao_vetor = Column(Vector(1536)) # Dimensão padrão para modelos como OpenAI
    
    agenda = relationship("Agenda", back_populates="sessao_dados")