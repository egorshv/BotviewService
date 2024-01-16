from aiogram.fsm.state import StatesGroup, State


class AddForm(StatesGroup):
    ticker = State()
    action = State()
    value = State()
    currency = State()


class UpdateForm(StatesGroup):
    ticker = State()
    action = State()
    value = State()
    currency = State()
    result = State()
    mark = State()
