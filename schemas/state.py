from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator


class StateSchema(BaseModel):
    id: Optional[int] = None
    portfolio_id: int
    usd_result: float
    rub_result: float
    created_at: datetime

    @field_validator('id')
    def prevent_none(cls, v):
        assert id is not None, 'id may not be None'
        return v

    def __str__(self):
        return (f'id: {self.id} | USD result: {self.usd_result} | RUB result: {self.rub_result}'
                f' | created at: {self.created_at}')
