from typing import List

from aiogram.utils.keyboard import ReplyKeyboardBuilder
from pydantic import BaseModel


def operation_keyboard(operations: List[BaseModel]) -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    operation_pattern = 'id: {} | value: {} | created at: {}'
    [builder.button(text=operation_pattern.format(
        operation.id,
        operation.value,
        operation.created_at
    )) for operation in operations]
    return builder