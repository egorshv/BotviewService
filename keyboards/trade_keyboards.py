from typing import List

from aiogram.utils.keyboard import ReplyKeyboardBuilder
from pydantic import BaseModel

from schemas.currency import Currency
from schemas.trade import TradeActionType, TradeMark


def trade_action_types() -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    [builder.button(text=btn) for btn in TradeActionType]
    return builder


def trade_marks() -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    [builder.button(text=btn) for btn in TradeMark]
    return builder


def trade_currency() -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    [builder.button(text=btn) for btn in Currency]
    return builder


def trade_keyboard(trades: List[BaseModel]) -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    pattern = 'id: {} | ticker: {} | action: {} | value: {} | created_at: {}'
    [builder.button(text=pattern.format(trade.id,
                                        trade.ticker,
                                        trade.action,
                                        trade.value,
                                        trade.created_at))
     for trade in trades]
    return builder
