from aiogram.fsm.state import StatesGroup, State


class AddForm(StatesGroup):
    portfolio_name = State()
    operation_value = State()


class GetForm(StatesGroup):
    operation_portfolio_name = State()


class DeleteForm(StatesGroup):
    operation_portfolio_name = State()
    operation_id = State()


class UpdateForm(StatesGroup):
    operation_portfolio_name = State()
    operation_id = State()
    operation_value = State()
