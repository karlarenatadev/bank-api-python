from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cpf = Column(String(11), unique=True, index=True, nullable=False)
    data_nascimento = Column(DateTime)
    endereco = Column(String)

    # Relacionamento: Um cliente pode ter VÁRIAS contas
    contas = relationship("Conta", back_populates="cliente")

class Conta(Base):
    __tablename__ = "contas"

    id = Column(Integer, primary_key=True, index=True)
    numero_conta = Column(String, unique=True, index=True, nullable=False)
    agencia = Column(String, default="0001")
    saldo = Column(Float, default=0.0)
    
    # Chave Estrangeira: A quem pertence esta conta?
    cliente_id = Column(Integer, ForeignKey("clientes.id"))

    # Relacionamentos bidirecionais
    cliente = relationship("Cliente", back_populates="contas")
    transacoes = relationship("Transacao", back_populates="conta")

class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)  # Ex: "SAQUE" ou "DEPÓSITO"
    valor = Column(Float, nullable=False)
    data = Column(DateTime, default=datetime.utcnow)
    
    # Chave Estrangeira: De qual conta foi essa transação?
    conta_id = Column(Integer, ForeignKey("contas.id"))

    # Relacionamento de volta para a conta
    conta = relationship("Conta", back_populates="transacoes")