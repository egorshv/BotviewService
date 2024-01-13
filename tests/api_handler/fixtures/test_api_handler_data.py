from datetime import datetime
from typing import List

import pytest

from schemas.currency import Currency
from schemas.operation import OperationSchema
from schemas.portfolio import PortfolioSchema
from schemas.state import StateSchema
from schemas.trade import TradeSchema, TradeActionType


@pytest.fixture
def test_get_portfolio() -> PortfolioSchema:
    get_portfolio = PortfolioSchema(
        id=1,
        name='some',
        user_id=235
    )
    return get_portfolio


@pytest.fixture
def test_post_trade():
    post_trade = TradeSchema(
        portfolio_id=1,
        ticker='',
        action=TradeActionType.BUY,
        value=199,
        currency=Currency.USD,
        created_at=datetime.now()
    )
    return post_trade

@pytest.fixture
def test_updating_operation() -> OperationSchema:
    updating_operation = OperationSchema(
        id=1,
        portfolio_id=1,
        value=100,
        created_at=datetime.now()
    )
    return updating_operation


@pytest.fixture
def test_updated_operation() -> OperationSchema:
    updated_operation = OperationSchema(
        id=1,
        portfolio_id=1,
        value=194,
        created_at=datetime.now()
    )
    return updated_operation


@pytest.fixture
def test_state_list() -> List[StateSchema]:
    state_list = [StateSchema(
        portfolio_id=253,
        usd_result=13,
        rub_result=32,
        created_at=datetime.now()
    )]
    return state_list

