import sqlalchemy as sa
from src.database import database
from src.exceptions import AccountNotFoundError, BusinessError
from src.models.account import accounts
from src.models.transaction import TransactionType, transactions
from src.schemas.transaction import TransactionIn

class TransactionService:
    @database.transaction()
    async def create(self, transaction: TransactionIn, current_user_id: int):
        # 1. Busca a conta e valida se pertence ao utilizador autenticado
        query = accounts.select().where(accounts.c.id == transaction.account_id)
        account = await database.fetch_one(query)
        
        if not account:
            raise AccountNotFoundError
        
        if account.user_id != current_user_id:
            raise BusinessError("Acesso negado: Esta conta não lhe pertence.")

        # 2. Validação de saldo para levantamentos
        if transaction.type == TransactionType.WITHDRAWAL:
            if float(account.balance) < transaction.amount:
                raise BusinessError("Saldo insuficiente para realizar a operação.")

        # 3. Registo da transação
        transaction_id = await self.__register_transaction(transaction)
        
        # 4. Atualização ATÓMICA do saldo no banco de dados
        await self.__update_balance_atomic(transaction)

        return await database.fetch_one(transactions.select().where(transactions.c.id == transaction_id))

    async def __update_balance_atomic(self, transaction: TransactionIn):
        # O cálculo é feito no SQL: balance = balance + amount (ou - amount)
        if transaction.type == TransactionType.WITHDRAWAL:
            new_balance_expression = accounts.c.balance - transaction.amount
        else:
            new_balance_expression = accounts.c.balance + transaction.amount

        command = (
            accounts.update()
            .where(accounts.c.id == transaction.account_id)
            .values(balance=new_balance_expression)
        )
        await database.execute(command)

    async def __register_transaction(self, transaction: TransactionIn) -> int:
        command = transactions.insert().values(
            account_id=transaction.account_id,
            type=transaction.type,
            amount=transaction.amount,
        )
        return await database.execute(command)