from decimal import Decimal
from typing import Annotated
from pydantic import BaseModel, Field

class AccountIn(BaseModel):
    user_id: int
    # O uso de Annotated resolve o erro do Pylance
    balance: Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]