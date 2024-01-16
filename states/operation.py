from aiogram.fsm.state import StatesGroup, State


class AddForm(StatesGroup):
    operation_value = State()


class DeleteForm(StatesGroup):
    operation_portfolio_name = State()
    operation_id = State()


class UpdateForm(StatesGroup):
    operation_value = State()
