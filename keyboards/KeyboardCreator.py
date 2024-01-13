from typing import List

from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from schemas.currency import Currency
from schemas.operation import OperationSchema
from schemas.portfolio import PortfolioSchema
from schemas.state import StateSchema
from schemas.trade import TradeSchema, TradeActionType, TradeMark


class KeyboardCreator:
    def __init__(self):
        self.operation_pattern = 'id: {} | value: {} | created at: {}'
        self.state_pattern = 'id: {} | USD result: {} | RUB result: {} | Created at: {}'
        self.trade_pattern = 'id: {} | ticker: {} | action: {} | value: {} | created_at: {}'

    @staticmethod
    def create_portfolio_keyboard(portfolios: List[PortfolioSchema]) -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        for portfolio in portfolios:
            builder.button(text=portfolio.name)

        return builder.as_markup(resize_keyboard=True)

    def create_operation_keyboard(self, operations: List[OperationSchema]) -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        [builder.button(text=self.operation_pattern.format(
            operation.id,
            operation.value,
            operation.created_at
        )) for operation in operations]
        return builder.as_markup(resize_keyboard=True)

    def create_state_keyboard(self, states: List[StateSchema]) -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        [builder.button(text=self.state_pattern.format(state.id,
                                                       state.usd_result,
                                                       state.rub_result,
                                                       state.created_at)) for state in states]
        return builder.as_markup(resize_keyboard=True)

    def create_trade_keyboard(self, trades: List[TradeSchema]) -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        [builder.button(text=self.trade_pattern.format(trade.id,
                                                       trade.ticker,
                                                       trade.action,
                                                       trade.value,
                                                       trade.created_at))
         for trade in trades]
        return builder.as_markup(resize_keyboard=True)

    @staticmethod
    def get_trade_action_types_keyboard() -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        [builder.button(text=btn) for btn in TradeActionType]
        return builder.as_markup(resize_keyboard=True)

    @staticmethod
    def get_trade_marks_keyboard() -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        [builder.button(text=btn) for btn in TradeMark]
        return builder.as_markup(resize_keyboard=True)

    @staticmethod
    def get_currency_keyboard() -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        [builder.button(text=btn) for btn in Currency]
        return builder.as_markup(resize_keyboard=True)
