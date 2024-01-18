import pytest

from schemas.currency import Currency
from schemas.operation import OperationSchema
from schemas.portfolio import PortfolioSchema
from schemas.state import StateSchema
from schemas.trade import TradeSchema
from services.APIHandler import APIHandler


@pytest.mark.skip()
@pytest.mark.asyncio
async def test_api_handler_get(test_get_portfolio):
    post_portfolio = await APIHandler().post_object(PortfolioSchema, test_get_portfolio)
    get_portfolio = await APIHandler().get_object(PortfolioSchema, post_portfolio.id)
    assert post_portfolio == get_portfolio


@pytest.mark.skip()
@pytest.mark.asyncio
async def test_api_handler_post(test_post_trade):
    post_trade = await APIHandler().post_object(TradeSchema, test_post_trade)
    assert post_trade.ticker == test_post_trade.ticker
    assert post_trade.action == test_post_trade.action
    assert post_trade.portfolio_id == test_post_trade.portfolio_id
    assert post_trade.value == test_post_trade.value


@pytest.mark.skip()
@pytest.mark.asyncio
async def test_api_handler_update(test_updated_operation,
                                  test_updating_operation):
    post_operation = await APIHandler().post_object(OperationSchema, test_updating_operation)
    updated_operation = await APIHandler().update_object(OperationSchema, post_operation.id, test_updated_operation)
    assert updated_operation == test_updated_operation


@pytest.mark.skip()
@pytest.mark.asyncio
async def test_api_handler_list(test_state_list):
    for state in test_state_list:
        await APIHandler().post_object(StateSchema, state)
    state_list = await APIHandler().object_list(StateSchema, portfolio_id=253)
    assert len(state_list) == len(test_state_list)
    assert state_list[0].usd_result == test_state_list[0].usd_result
    assert state_list[0].rub_result == test_state_list[0].rub_result


@pytest.mark.asyncio
async def test_calculate_recall():
    recall = await APIHandler().calculate_recall(PortfolioSchema, 5)
    assert recall


@pytest.mark.asyncio
async def test_calculate_precision():
    precision = await APIHandler().calculate_precision(PortfolioSchema, 5)
    assert precision


@pytest.mark.asyncio
async def test_get_chart_data():
    chart_data = await APIHandler().get_chart_data(3, Currency.USD)
    assert chart_data
