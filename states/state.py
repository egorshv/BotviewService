from aiogram.fsm.state import StatesGroup, State


class AddForm(StatesGroup):
    usd_result = State()
    rub_result = State()


class UpdateForm(StatesGroup):
    usd_result = State()
    rub_result = State()
