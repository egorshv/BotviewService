from aiogram.utils.keyboard import ReplyKeyboardBuilder


def trade_action_types() -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    [builder.button(text=btn) for btn in ['BUY', 'SELL']]
    return builder


def trade_currency() -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    [builder.button(text=btn) for btn in ['USD', 'RUB', 'CNY']]
    return builder
