from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models
import schemas
import crud

# Cria as tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Bancária - Karla Renata",
    description="Sistema transacional construído com FastAPI e SQLAlchemy",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"mensagem": "API Bancária Operacional. Acesse /docs para a documentação."}

# Rota para Criar um Cliente (Método POST)
@app.post("/clientes/", response_model=schemas.ClienteResponse)
def criar_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    # O FastAPI já validou se os dados vieram no formato do Schema. 
    # Agora checamos se o CPF já existe no banco:
    db_cliente = crud.get_cliente_by_cpf(db, cpf=cliente.cpf)
    if db_cliente:
        raise HTTPException(status_code=400, detail="CPF já cadastrado.")
    
    return crud.criar_cliente(db=db, cliente=cliente)

# Rota para Criar uma Conta (Método POST)
@app.post("/contas/", response_model=schemas.ContaResponse)
def criar_conta(conta: schemas.ContaCreate, db: Session = Depends(get_db)):
    # Checa se o cliente existe antes de criar a conta para ele
    cliente = db.query(models.Cliente).filter(models.Cliente.id == conta.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    
    return crud.criar_conta(db=db, conta=conta)

# Rota para Depósito
@app.post("/contas/{conta_id}/deposito", response_model=schemas.ContaResponse)
def realizar_deposito(conta_id: int, transacao: schemas.TransacaoCreate, db: Session = Depends(get_db)):
    conta_atualizada = crud.depositar(db=db, conta_id=conta_id, transacao=transacao)
    
    if not conta_atualizada:
        raise HTTPException(status_code=404, detail="Conta não encontrada.")
    
    return conta_atualizada

# Rota para Saque
@app.post("/contas/{conta_id}/saque", response_model=schemas.ContaResponse)
def realizar_saque(conta_id: int, transacao: schemas.TransacaoCreate, db: Session = Depends(get_db)):
    conta_atualizada = crud.sacar(db=db, conta_id=conta_id, transacao=transacao)
    
    if not conta_atualizada:
        raise HTTPException(status_code=404, detail="Conta não encontrada.")
    
    # Traduz os bloqueios da regra de negócio para o usuário
    if conta_atualizada == "SALDO_INSUFICIENTE":
        raise HTTPException(status_code=400, detail="Operação falhou! Saldo insuficiente.")
    if conta_atualizada == "LIMITE_VALOR_EXCEDIDO":
        raise HTTPException(status_code=400, detail="Operação falhou! O valor excede o limite de R$ 500,00.")
    if conta_atualizada == "LIMITE_SAQUES_EXCEDIDO":
        raise HTTPException(status_code=400, detail="Operação falhou! Número máximo de 3 saques diários excedido.")
    
    return conta_atualizada