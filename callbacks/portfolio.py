from aiogram.filters.callback_data import CallbackData


class PortfolioCallback(CallbackData, prefix='portfolio-callback'):
    type: str
    id: int
