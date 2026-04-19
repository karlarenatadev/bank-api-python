from fastapi import APIRouter, Depends
from src.security import login_required
from src.schemas.transaction import TransactionIn
from src.services.transaction import TransactionService

router = APIRouter()
service = TransactionService()

@router.post("/transactions")
async def create_transaction(
    transaction: TransactionIn,
    user_data: dict = Depends(login_required) # Injeta o user_id do JWT
):
    return await service.create(transaction, current_user_id=user_data["user_id"])