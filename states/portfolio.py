from aiogram.fsm.state import StatesGroup, State


class AddForm(StatesGroup):
    name = State()
    deposited_money = State()


class UpdateForm(StatesGroup):
    name = State()
    deposited_money = State()
