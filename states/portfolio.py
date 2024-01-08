from aiogram.fsm.state import StatesGroup, State


class AddForm(StatesGroup):
    name = State()
    deposited_money = State()

class DeleteForm(StatesGroup):
    name = State()
