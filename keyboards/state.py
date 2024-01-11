from typing import List

from aiogram.utils.keyboard import ReplyKeyboardBuilder
from pydantic import BaseModel


def states_keyboard(states: List[BaseModel]) -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    state_pattern = "id: {} | USD result: {} | RUB result: {} | Created at: {}"
    [builder.button(text=state_pattern.format(state.id,
                                              state.usd_result,
                                              state.rub_result,
                                              state.created_at)) for state in states]
    return builder
