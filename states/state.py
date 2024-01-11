from aiogram.fsm.state import StatesGroup, State


class AddForm(StatesGroup):
    state_portfolio_name = State()
    usd_result = State()
    rub_result = State()


class GetForm(StatesGroup):
    state_portfolio_name = State()
