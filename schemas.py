from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

# ==========================================
# SCHEMAS DE TRANSAÇÃO
# ==========================================
class TransacaoBase(BaseModel):
    valor: float = Field(..., gt=0, description="O valor deve ser maior que zero")

class TransacaoCreate(TransacaoBase):
    tipo: str = Field(..., description="SAQUE ou DEPOSITO")

class TransacaoResponse(TransacaoBase):
    id: int
    tipo: str
    data: datetime

    class Config:
        from_attributes = True  # Permite ler os dados diretamente do SQLAlchemy (models.py)

# ==========================================
# SCHEMAS DE CONTA
# ==========================================
class ContaBase(BaseModel):
    numero_conta: str
    agencia: str = "0001"

class ContaCreate(ContaBase):
    cliente_id: int

class ContaResponse(ContaBase):
    id: int
    saldo: float
    transacoes: List[TransacaoResponse] = [] # Traz o histórico embutido!

    class Config:
        from_attributes = True

# ==========================================
# SCHEMAS DE CLIENTE
# ==========================================
class ClienteBase(BaseModel):
    nome: str
    cpf: str = Field(..., min_length=11, max_length=11, description="CPF deve ter 11 dígitos")
    endereco: str

class ClienteCreate(ClienteBase):
    data_nascimento: datetime

class ClienteResponse(ClienteBase):
    id: int
    contas: List[ContaResponse] = [] # Traz as contas do cliente embutidas

    class Config:
        from_attributes = True