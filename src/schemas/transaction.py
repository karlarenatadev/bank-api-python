from enum import Enum
from decimal import Decimal
from typing import Annotated
from pydantic import BaseModel, Field

class TransactionType(Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"

class TransactionIn(BaseModel):
    account_id: int
    type: TransactionType
    amount: Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]

    class Config:
        use_enum_values = True