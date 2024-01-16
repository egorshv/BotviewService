from typing import List

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from callbacks.operation import OperationCallback
from callbacks.portfolio import PortfolioCallback
from callbacks.state import StateCallback
from callbacks.trade import TradeCallback
from schemas.currency import Currency
from schemas.operation import OperationSchema
from schemas.portfolio import PortfolioSchema
from schemas.state import StateSchema
from schemas.trade import TradeSchema, TradeActionType, TradeMark


class KeyboardCreator:
    @staticmethod
    def create_portfolio_keyboard(portfolios: List[PortfolioSchema], callback_type: str) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        for portfolio in portfolios:
            builder.button(
                text=portfolio.name,
                callback_data=PortfolioCallback(
                    type=callback_type,
                    id=portfolio.id
                )
            )

        return builder.as_markup(resize_keyboard=True)

    def create_operation_keyboard(self, operations: List[OperationSchema], callback_type: str) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        [builder.button(text=f"id: {operation.id} | value: {operation.value} | created at: {operation.created_at}",
                        callback_data=OperationCallback(
                            type=callback_type,
                            id=operation.id
                        )) for operation in operations]
        return builder.as_markup(resize_keyboard=True)

    def create_state_keyboard(self, states: List[StateSchema], callback_type: str) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        [builder.button(
            text=f"USD result: {state.usd_result} | RUB result: {state.rub_result} | created at: {state.created_at}",
            callback_data=StateCallback(
                type=callback_type,
                id=state.id,
                portfolio_id=state.portfolio_id
            )
            ) for state in states]
        return builder.as_markup(resize_keyboard=True)

    def create_trade_keyboard(self, trades: List[TradeSchema], callback_type: str) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        [builder.button(text=f"ticker: {trade.ticker} | action: {trade.action} | value: {trade.value}"
                             f"created at: {trade.created_at}",
                        callback_data=TradeCallback(
                            type=callback_type,
                            id=trade.id,
                            portfolio_id=trade.portfolio_id
                        ))
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
