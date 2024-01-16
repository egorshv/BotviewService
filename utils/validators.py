from schemas.currency import Currency
from schemas.trade import TradeActionType, TradeMark


def isfloat(number: str) -> bool:
    return number.replace('.', '', 1).isdigit()


def is_trade_action(action: str) -> bool:
    return action in TradeActionType


def is_currency(currency: str) -> bool:
    return currency in Currency


def is_mark(mark: str) -> bool:
    return mark in TradeMark
