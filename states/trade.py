from aiogram.fsm.state import StatesGroup, State


class AddForm(StatesGroup):
    portfolio_name = State()
    ticker = State()
    action = State()
    value = State()
    currency = State()


class GetForm(StatesGroup):
    portfolio_name = State()


class DeleteForm(StatesGroup):
    portfolio_name = State()
    trade_id = State()


class UpdateForm(StatesGroup):
    portfolio_name = State()
    trade_id = State()
    ticker = State()
    action = State()
    value = State()
    currency = State()
    result = State()
    mark = State()
