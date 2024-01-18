import abc
from datetime import datetime
from typing import List, Tuple

from schemas.currency import Currency
from schemas.operation import OperationSchema
from schemas.portfolio import PortfolioSchema
from schemas.state import StateSchema
from schemas.trade import TradeSchema
from services.APIHandler import APIHandler


class AbstractUserStorageManager(abc.ABC):
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.api_handler = APIHandler()

    @abc.abstractmethod
    async def get_portfolios(self, **kwargs) -> List[PortfolioSchema]:
        raise NotImplemented

    @abc.abstractmethod
    async def get_portfolio(self, portfolio_id: int) -> PortfolioSchema:
        raise NotImplemented

    @abc.abstractmethod
    async def update_portfolio(self, portfolio_id: int, portfolio: PortfolioSchema) -> PortfolioSchema:
        raise NotImplemented

    @abc.abstractmethod
    async def delete_portfolio(self, portfolio_id: int) -> None:
        raise NotImplemented

    @abc.abstractmethod
    async def add_portfolio(self, portfolio: PortfolioSchema) -> PortfolioSchema:
        raise NotImplemented

    @abc.abstractmethod
    async def get_trades(self, **kwargs) -> List[TradeSchema]:
        raise NotImplemented

    @abc.abstractmethod
    async def delete_trade(self, trade_id: int) -> None:
        raise NotImplemented

    @abc.abstractmethod
    async def update_trade(self, trade_id: int, trade: TradeSchema) -> TradeSchema:
        raise NotImplemented

    @abc.abstractmethod
    async def add_trade(self, trade: TradeSchema) -> TradeSchema:
        raise NotImplemented

    @abc.abstractmethod
    async def get_states(self, **kwargs) -> List[StateSchema]:
        raise NotImplemented

    @abc.abstractmethod
    async def delete_state(self, state_id: int) -> None:
        raise NotImplemented

    @abc.abstractmethod
    async def update_state(self, state_id: int, state: StateSchema) -> StateSchema:
        raise NotImplemented

    @abc.abstractmethod
    async def add_state(self, state: StateSchema) -> StateSchema:
        raise NotImplemented

    @abc.abstractmethod
    async def get_operations(self, **kwargs) -> List[OperationSchema]:
        raise NotImplemented

    @abc.abstractmethod
    async def update_operation(self, operation_id: int, operation: OperationSchema) -> OperationSchema:
        raise NotImplemented

    @abc.abstractmethod
    async def delete_operation(self, operation_id: int) -> None:
        raise NotImplemented

    @abc.abstractmethod
    async def add_operation(self, operation: OperationSchema) -> OperationSchema:
        raise NotImplemented

    @abc.abstractmethod
    async def calculate_portfolio_precision(self, portfolio_id: int) -> float:
        raise NotImplemented

    @abc.abstractmethod
    async def calculate_portfolio_recall(self, portfolio_id: int) -> float:
        raise NotImplemented

    @abc.abstractmethod
    async def get_chart_data(self, portfolio_id: int, currency: Currency) -> List[Tuple[float, datetime]]:
        raise NotImplemented


class UserStorageManager(AbstractUserStorageManager):
    def __init__(self, user_id: int):
        super().__init__(user_id)

    async def get_portfolios(self, **kwargs) -> List[PortfolioSchema]:
        portfolios = await self.api_handler.object_list(PortfolioSchema, **kwargs, user_id=self.user_id)
        return portfolios

    async def get_portfolio(self, portfolio_id: int) -> PortfolioSchema:
        portfolio = await self.api_handler.get_object(PortfolioSchema, portfolio_id)
        return portfolio

    async def update_portfolio(self, portfolio_id: int, portfolio: PortfolioSchema) -> PortfolioSchema:
        portfolio = await self.api_handler.update_object(PortfolioSchema, portfolio_id, portfolio)
        return portfolio

    async def delete_portfolio(self, portfolio_id: int) -> None:
        await self.api_handler.delete_object(PortfolioSchema, portfolio_id)

    async def add_portfolio(self, portfolio: PortfolioSchema) -> PortfolioSchema:
        portfolio = await self.api_handler.post_object(PortfolioSchema, portfolio)
        return portfolio

    async def get_trades(self, **kwargs) -> List[TradeSchema]:
        trades = await self.api_handler.object_list(TradeSchema, **kwargs)
        return trades

    async def update_trade(self, trade_id: int, trade: TradeSchema) -> TradeSchema:
        trade = await self.api_handler.update_object(TradeSchema, trade_id, trade)
        return trade

    async def delete_trade(self, trade_id: int) -> None:
        await self.api_handler.delete_object(TradeSchema, trade_id)

    async def add_trade(self, trade: TradeSchema) -> TradeSchema:
        trade = await self.api_handler.post_object(TradeSchema, trade)
        return trade

    async def get_operations(self, **kwargs) -> List[OperationSchema]:
        operations = await self.api_handler.object_list(OperationSchema, **kwargs)
        return operations

    async def delete_operation(self, operation_id: int) -> None:
        await self.api_handler.delete_object(OperationSchema, operation_id)

    async def update_operation(self, operation_id: int, operation: OperationSchema) -> OperationSchema:
        operation = await self.api_handler.update_object(OperationSchema, operation_id, operation)
        return operation

    async def add_operation(self, operation: OperationSchema) -> OperationSchema:
        operation = await self.api_handler.post_object(OperationSchema, operation)
        return operation

    async def get_states(self, **kwargs) -> List[StateSchema]:
        states = await self.api_handler.object_list(StateSchema, **kwargs)
        return states

    async def update_state(self, state_id: int, state: StateSchema) -> StateSchema:
        state = await self.api_handler.update_object(StateSchema, state_id, state)
        return state

    async def delete_state(self, state_id: int) -> None:
        await self.api_handler.delete_object(StateSchema, state_id)

    async def add_state(self, state: StateSchema) -> StateSchema:
        state = await self.api_handler.post_object(StateSchema, state)
        return state

    async def get_chart_data(self, portfolio_id: int, currency: Currency) -> List[Tuple[float, datetime]]:
        chart_data = await self.api_handler.get_chart_data(portfolio_id, currency)
        return chart_data

    async def calculate_portfolio_recall(self, portfolio_id: int) -> float:
        portfolio = await self.api_handler.calculate_recall(PortfolioSchema, portfolio_id)
        return portfolio.last_recall

    async def calculate_portfolio_precision(self, portfolio_id: int) -> float:
        portfolio = await self.api_handler.calculate_precision(PortfolioSchema, portfolio_id)
        return portfolio.last_precision
