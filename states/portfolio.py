from aiogram.fsm.state import StatesGroup, State


class AddForm(StatesGroup):
    name = State()
    deposited_money = State()


class DeleteForm(StatesGroup):
    name = State()


class GetForm(StatesGroup):
    name = State()


class UpdateForm(StatesGroup):
    name = State()
    new_name = State()
    new_deposited_money = State()