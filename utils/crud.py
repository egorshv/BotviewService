from typing import List

from pydantic import BaseModel

from schemas.operation import OperationSchema
from schemas.portfolio import PortfolioSchema
from schemas.state import StateSchema
from schemas.trade import TradeSchema
from services.APIHandler import APIHandler


async def get_user_portfolios(user_id: int) -> List[BaseModel]:
    api_handler = APIHandler()
    portfolios = await api_handler.object_list(PortfolioSchema, user_id=user_id)
    return portfolios


async def get_portfolio_by_name(name: str, user_id: int) -> BaseModel:
    api_handler = APIHandler()
    [portfolio] = await api_handler.object_list(PortfolioSchema, name=name, user_id=user_id)
    return portfolio


async def update_portfolio(name: str, user_id: int, new_name: str, new_deposited_money: float) -> None:
    portfolio = await get_portfolio_by_name(name, user_id)

    updated_portfolio = PortfolioSchema(
        id=portfolio.id,
        name=new_name,
        deposited_money=new_deposited_money,
        last_precision=portfolio.last_precision,
        last_recall=portfolio.last_recall,
        user_id=portfolio.user_id
    )

    await APIHandler().update_object(PortfolioSchema, portfolio.id, updated_portfolio)


async def get_trade(trade_id: int) -> BaseModel:
    trade = await APIHandler().get_object(TradeSchema, trade_id)
    return trade


async def get_trades_list(**kwargs) -> List[BaseModel]:
    trades = await APIHandler().object_list(TradeSchema, **kwargs)
    return trades


async def delete_trade(trade_id: int) -> None:
    await APIHandler().delete_object(TradeSchema, trade_id)


async def update_trade(trade_id: int, trade: TradeSchema) -> BaseModel:
    trade = await APIHandler().update_object(TradeSchema, trade_id, trade)
    return trade


async def get_states_list(**kwargs) -> List[BaseModel]:
    states = await APIHandler().object_list(StateSchema, **kwargs)
    return states


async def delete_state(state_id: int) -> None:
    await APIHandler().delete_object(StateSchema, state_id)


async def update_state(state_id: int, state: StateSchema) -> BaseModel:
    state = await APIHandler().update_object(StateSchema, state_id, state)
    return state


async def get_operation_list(**kwargs) -> List[BaseModel]:
    operations = await APIHandler().object_list(OperationSchema, **kwargs)
    return operations
