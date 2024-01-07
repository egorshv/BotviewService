from datetime import datetime

import pytest
from aiohttp import web

from schemas.currency import Currency
from schemas.operation import OperationSchema
from schemas.portfolio import PortfolioSchema
from schemas.state import StateSchema
from schemas.trade import TradeSchema, TradeActionType


@pytest.fixture
def test_get_portfolio():
    test_get_portfolio = PortfolioSchema(
        id=1,
        name='some',
        user_id=235
    )
    return web.Response(body=test_get_portfolio.model_dump())


@pytest.fixture
def test_post_trade():
    test_post_trade = TradeSchema(
        portfolio_id=1,
        ticker='',
        action=TradeActionType.BUY,
        value=199,
        currency=Currency.USD,
        created_at=datetime.now()
    )
    return web.Response(body=test_post_trade.model_dump())


@pytest.fixture
def test_updated_operation():
    test_updated_operation = OperationSchema(
        id=1,
        portfolio_id=1,
        value=194,
        created_at=datetime.now()
    )
    return web.Response(body=test_updated_operation.model_dump())


@pytest.fixture
def test_state_list():
    test_state_list = StateSchema(
        id=1,
        portfolio_id=253,
        usd_result=13,
        rub_result=32,
        created_at=datetime.now()
    )
    return web.Response(body=test_state_list.model_dump())


def prepare_test_routes(app,
                        test_get_portfolio,
                        test_post_trade,
                        test_updated_operation,
                        test_state_list) -> None:
    app.router.add_get('/portfolio/1', test_get_portfolio)
    app.router.add_post('/trade', test_post_trade)
    app.router.add_put('/operation', test_updated_operation)
    app.router.add_get(f'/state?portfolio_id=253', test_state_list)


@pytest.fixture
async def test_client(aiohttp_client,
                      test_get_portfolio,
                      test_post_trade,
                      test_updated_operation,
                      test_state_list):
    app = web.Application()
    prepare_test_routes(app, test_get_portfolio, test_post_trade, test_updated_operation, test_state_list)
    client = await aiohttp_client(app)
    return client
