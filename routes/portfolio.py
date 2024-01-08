from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from schemas.portfolio import PortfolioSchema
from services.APIHandler import APIHandler
from states.portfolio import AddForm, DeleteForm
from utils.keyboard_creating import create_portfolio_keyboard
from utils.crud import get_user_portfolios, get_portfolio_by_name

router = Router()


@router.message(Command('add_portfolio'))
async def add_portfolio_handler(message: Message, state: FSMContext):
    await state.set_state(AddForm.name)
    await message.answer(
        'Enter portfolio name: ',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(AddForm.name)
async def getting_name_handler(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddForm.deposited_money)
    await message.answer(
        'Enter deposited money: ',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(AddForm.deposited_money)
async def getting_deposited_money_handler(message: Message, state: FSMContext):
    await state.update_data(deposited_money=message.text)
    data = await state.update_data(user_id=message.from_user.id)
    try:
        portfolio = PortfolioSchema(**data)
        api_handler = APIHandler()
        await api_handler.post_object(PortfolioSchema, portfolio)
        await message.answer(
            'Portfolio added',
            reply_markup=ReplyKeyboardRemove()
        )
    except Exception as ex:
        await message.answer(
            f'Something went wrong, error: {ex}',
            reply_markup=ReplyKeyboardRemove()
        )
    finally:
        await state.clear()


@router.message(Command('delete_portfolio'))
async def delete_portfolio(message: Message, state: FSMContext):
    await state.set_state(DeleteForm.name)
    portfolios = await get_user_portfolios(message.from_user.id)
    portfolio_keyboard = create_portfolio_keyboard(portfolios)
    await message.answer(
        'Choose deleting portfolio: ',
        reply_markup=portfolio_keyboard.as_markup()
    )


@router.message(DeleteForm.name)
async def getting_portfolio_id(message: Message, state: FSMContext):
    try:
        portfolio = await get_portfolio_by_name(message.text, message.from_user.id)
        await APIHandler().delete_object(PortfolioSchema, portfolio.id)
        await message.answer(
            'Portfolio deleted',
            reply_markup=ReplyKeyboardRemove()
        )
    except Exception as ex:
        await message.answer(
            f'Something went wrong, error: {ex}',
            reply_markup=ReplyKeyboardRemove()
        )
    finally:
        await state.clear()
