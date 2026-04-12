from sqlalchemy.orm import Session
from datetime import datetime, date
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

def depositar(db: Session, conta_id: int, transacao: schemas.TransacaoCreate):
    # Busca a conta no banco
    conta = db.query(models.Conta).filter(models.Conta.id == conta_id).first()
    if not conta:
        return None

    # Atualiza o saldo
    conta.saldo += transacao.valor

    # Cria o registro no histórico
    db_transacao = models.Transacao(
        tipo="DEPÓSITO",
        valor=transacao.valor,
        conta_id=conta.id
    )
    
    # Salva as duas alterações juntas (transação atômica)
    db.add(db_transacao)
    db.commit()
    db.refresh(conta) # Atualiza o objeto para retornar o saldo novo
    return conta

def sacar(db: Session, conta_id: int, transacao: schemas.TransacaoCreate):
    conta = db.query(models.Conta).filter(models.Conta.id == conta_id).first()
    if not conta:
        return None

    # --- REGRAS DE NEGÓCIO DA CONTA CORRENTE ---
    LIMITE_VALOR_SAQUE = 500.0
    LIMITE_QTD_SAQUES_DIARIOS = 3

    # 1. Regra: Tem saldo?
    if conta.saldo < transacao.valor:
        return "SALDO_INSUFICIENTE"
        
    # 2. Regra: Passou de 500 reais?
    if transacao.valor > LIMITE_VALOR_SAQUE:
        return "LIMITE_VALOR_EXCEDIDO"

    # 3. Regra: Já fez 3 saques hoje?
    hoje = date.today()
    # Faz um SELECT no banco contando os saques de hoje dessa conta
    saques_hoje = db.query(models.Transacao).filter(
        models.Transacao.conta_id == conta.id,
        models.Transacao.tipo == "SAQUE",
        models.Transacao.data >= datetime(hoje.year, hoje.month, hoje.day)
    ).count()

    if saques_hoje >= LIMITE_QTD_SAQUES_DIARIOS:
        return "LIMITE_SAQUES_EXCEDIDO"

    # Se passou por todas as regras, atualiza o saldo
    conta.saldo -= transacao.valor

    # Cria o registro no histórico
    db_transacao = models.Transacao(
        tipo="SAQUE",
        valor=transacao.valor,
        conta_id=conta.id
    )
    
    db.add(db_transacao)
    db.commit()
    db.refresh(conta)
    return conta