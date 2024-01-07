from typing import Optional

from pydantic import BaseModel, field_validator


class PortfolioSchema(BaseModel):
    id: Optional[int] = None
    name: str
    last_precision: Optional[float] = 0
    last_recall: Optional[float] = 0
    user_id: int
    deposited_money: int = 0

    @field_validator('id')
    def prevent_none(cls, v):
        assert id is not None, 'id may not be None'
        return v
