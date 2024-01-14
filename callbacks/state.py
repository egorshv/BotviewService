from aiogram.filters.callback_data import CallbackData


class StateCallback(CallbackData, prefix='state-callback'):
    type: str
    id: int
    portfolio_id: int
