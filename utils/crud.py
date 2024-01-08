from typing import List

from pydantic import BaseModel

from schemas.portfolio import PortfolioSchema
from services.APIHandler import APIHandler


async def get_user_portfolios(user_id: int) -> List[BaseModel]:
    api_handler = APIHandler()
    portfolios = await api_handler.object_list(PortfolioSchema, user_id=user_id)
    return portfolios


async def get_portfolio_by_name(name: str, user_id: int) -> BaseModel:
    api_handler = APIHandler()
    [portfolio] = await api_handler.object_list(PortfolioSchema, name=name, user_id=user_id)
    return portfolio
