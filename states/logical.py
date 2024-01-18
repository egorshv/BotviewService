from aiogram.fsm.state import StatesGroup, State


class GetChart(StatesGroup):
    currency = State()


class SetMark(StatesGroup):
    mark = State()
