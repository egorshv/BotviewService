from typing import List

from aiogram.utils.keyboard import ReplyKeyboardBuilder
from pydantic import BaseModel


def create_portfolio_keyboard(portfolios: List[BaseModel]) -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    for portfolio in portfolios:
        builder.button(text=portfolio.name)

    return builder
