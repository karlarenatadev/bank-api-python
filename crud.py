from sqlalchemy.orm import Session
import models
import schemas

def get_cliente_by_cpf(db: Session, cpf: str):
    # Substitui a sua antiga função 'filtrar_cliente'. Agora ele faz um SELECT no banco.
    return db.query(models.Cliente).filter(models.Cliente.cpf == cpf).first()

def criar_cliente(db: Session, cliente: schemas.ClienteCreate):
    # Prepara o dado para inserir na tabela Clientes
    db_cliente = models.Cliente(
        nome=cliente.nome,
        cpf=cliente.cpf,
        data_nascimento=cliente.data_nascimento,
        endereco=cliente.endereco
    )
    db.add(db_cliente) # Adiciona
    db.commit()        # Salva (Grava fisicamente)
    db.refresh(db_cliente)
    return db_cliente

def criar_conta(db: Session, conta: schemas.ContaCreate):
    # Conta quantas contas já existem para gerar o próximo número de conta
    qtd_contas = db.query(models.Conta).count()
    numero_conta = str(qtd_contas + 1)
    
    # Prepara o dado para inserir na tabela Contas
    db_conta = models.Conta(
        numero_conta=numero_conta,
        cliente_id=conta.cliente_id
    )
    db.add(db_conta)
    db.commit()
    db.refresh(db_conta)
    return db_conta