from typing import List

from pydantic import BaseModel

from schemas.portfolio import PortfolioSchema
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


async def get_trades_by_portfolio_id(portfolio_id: int, user_id: int) -> List[BaseModel]:
    trades = await APIHandler().object_list(TradeSchema,
                                            portfolio_id=portfolio_id,
                                            user_id=user_id)
    return trades
