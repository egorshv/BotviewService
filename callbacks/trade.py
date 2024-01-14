from aiogram.filters.callback_data import CallbackData


class TradeCallback(CallbackData, prefix='trade-callback'):
    type: str
    id: int
    portfolio_id: int
