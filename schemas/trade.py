from datetime import datetime
from enum import Enum
from typing import Optional
from schemas.currency import Currency

from pydantic import BaseModel, field_validator


class TradeActionType(str, Enum):
    BUY = 'buy'
    SELL = 'sell'


class TradeMark(str, Enum):
    TP = 'tp'
    TN = 'tn'
    FP = 'fp'
    FN = 'fn'


class TradeSchema(BaseModel):
    id: Optional[int] = None
    portfolio_id: int
    ticker: str
    action: TradeActionType
    value: float
    currency: Currency
    created_at: datetime
    result: Optional[float] = None
    mark: Optional[TradeMark] = None

    @field_validator('id')
    def prevent_none(cls, v):
        assert id is not None, 'id may not be None'
        return v
