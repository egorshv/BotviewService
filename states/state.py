from aiogram.fsm.state import StatesGroup, State


class AddForm(StatesGroup):
    state_portfolio_name = State()
    usd_result = State()
    rub_result = State()


class GetForm(StatesGroup):
    state_portfolio_name = State()


class DeleteForm(StatesGroup):
    state_portfolio_name = State()
    state_id = State()


class UpdateForm(StatesGroup):
    state_portfolio_name = State()
    state_id = State()
    usd_result = State()
    rub_result = State()
