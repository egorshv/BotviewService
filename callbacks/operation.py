from aiogram.filters.callback_data import CallbackData


class OperationCallback(CallbackData, prefix='operation-callback'):
    type: str
    id: int
