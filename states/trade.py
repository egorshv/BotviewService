from aiogram.fsm.state import StatesGroup, State


class AddForm(StatesGroup):
    portfolio_name = State()
    ticker = State()
    action = State()
    value = State()
    currency = State()


class GetForm(StatesGroup):
    portfolio_name = State()
