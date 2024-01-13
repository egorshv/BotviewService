from datetime import datetime
from typing import List

import pytest

from schemas.currency import Currency
from schemas.operation import OperationSchema
from schemas.portfolio import PortfolioSchema
from schemas.state import StateSchema
from schemas.trade import TradeSchema, TradeActionType


@pytest.fixture
def test_portfolios() -> List[PortfolioSchema]:
    return [
        PortfolioSchema(
            id=3259,
            user_id=11111111,
            name=''
        ),
        PortfolioSchema(
            id=3258,
            user_id=11111111,
            name=''
        ),
        PortfolioSchema(
            id=3257,
            user_id=11111111,
            name=''
        ),
        PortfolioSchema(
            id=3256,
            user_id=11111111,
            name=''
        ),
        PortfolioSchema(
            id=3255,
            user_id=11111111,
            name=''
        )
    ]


@pytest.fixture
def test_portfolio() -> PortfolioSchema:
    return PortfolioSchema(
        id=462,
        name='get portfolio',
        user_id=452
    )


@pytest.fixture
def test_updated_portfolio() -> PortfolioSchema:
    return PortfolioSchema(
        id=462,
        name='updated portfolio',
        user_id=452
    )


@pytest.fixture
def test_trades() -> List[TradeSchema]:
    return [
        TradeSchema(
            id=1,
            portfolio_id=32,
            ticker='',
            action=TradeActionType.BUY,
            value=0,
            currency=Currency.USD,
            created_at=datetime.now()
        ),
        TradeSchema(
            id=2,
            portfolio_id=32,
            ticker='',
            action=TradeActionType.BUY,
            value=0,
            currency=Currency.USD,
            created_at=datetime.now()
        ), TradeSchema(
            id=3,
            portfolio_id=32,
            ticker='',
            action=TradeActionType.BUY,
            value=0,
            currency=Currency.USD,
            created_at=datetime.now()
        ), TradeSchema(
            id=4,
            portfolio_id=32,
            ticker='',
            action=TradeActionType.BUY,
            value=0,
            currency=Currency.USD,
            created_at=datetime.now()
        ), TradeSchema(
            id=5,
            portfolio_id=32,
            ticker='',
            action=TradeActionType.BUY,
            value=0,
            currency=Currency.USD,
            created_at=datetime.now()
        )
    ]


@pytest.fixture
def test_trade() -> TradeSchema:
    return TradeSchema(
        id=6,
        portfolio_id=3232,
        ticker='',
        action=TradeActionType.BUY,
        value=0,
        currency=Currency.USD,
        created_at=datetime.now()
    )


@pytest.fixture
def test_updated_trade() -> TradeSchema:
    return TradeSchema(
        id=6,
        portfolio_id=3232,
        ticker='UPD',
        action=TradeActionType.BUY,
        value=0,
        currency=Currency.USD,
        created_at=datetime.now()
    )


@pytest.fixture
def test_operations() -> List[OperationSchema]:
    return [
        OperationSchema(
            id=21,
            portfolio_id=4920,
            value=129,
            created_at=datetime.now()
        ),
        OperationSchema(
            id=22,
            portfolio_id=4920,
            value=229,
            created_at=datetime.now()
        ),
        OperationSchema(
            id=23,
            portfolio_id=4920,
            value=777,
            created_at=datetime.now()
        ),
    ]


@pytest.fixture
def test_operation() -> OperationSchema:
    return OperationSchema(
        id=24,
        portfolio_id=4921,
        value=7779,
        created_at=datetime.now()
    )


@pytest.fixture
def test_updated_operation() -> OperationSchema:
    return OperationSchema(
        id=24,
        portfolio_id=4921,
        value=777,
        created_at=datetime.now()
    )


@pytest.fixture
def test_states() -> List[StateSchema]:
    return [
        StateSchema(
            id=23,
            portfolio_id=111,
            usd_result=15,
            rub_result=3,
            created_at=datetime.now()
        ),
        StateSchema(
            id=24,
            portfolio_id=111,
            usd_result=17,
            rub_result=2,
            created_at=datetime.now()
        ),
        StateSchema(
            id=25,
            portfolio_id=111,
            usd_result=18,
            rub_result=9,
            created_at=datetime.now()
        ),
        StateSchema(
            id=26,
            portfolio_id=111,
            usd_result=11,
            rub_result=4,
            created_at=datetime.now()
        )
    ]


@pytest.fixture
def test_state() -> StateSchema:
    return StateSchema(
        id=27,
        portfolio_id=111,
        usd_result=111,
        rub_result=4,
        created_at=datetime.now()
    )


@pytest.fixture
def test_updated_state() -> StateSchema:
    return StateSchema(
        id=27,
        portfolio_id=111,
        usd_result=1,
        rub_result=4,
        created_at=datetime.now()
    )
