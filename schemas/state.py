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
