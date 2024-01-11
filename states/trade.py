from aiogram.fsm.state import StatesGroup, State


class AddForm(StatesGroup):
    trade_portfolio_name = State()
    ticker = State()
    action = State()
    value = State()
    currency = State()


class GetForm(StatesGroup):
    trade_portfolio_name = State()


class DeleteForm(StatesGroup):
    trade_portfolio_name = State()
    trade_id = State()


class UpdateForm(StatesGroup):
    trade_portfolio_name = State()
    trade_id = State()
    ticker = State()
    action = State()
    value = State()
    currency = State()
    result = State()
    mark = State()
