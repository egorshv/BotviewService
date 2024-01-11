from datetime import datetime

from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router

from keyboards.portfolio_keyboards import create_portfolio_keyboard
from schemas.state import StateSchema
from services.APIHandler import APIHandler
from states.state import AddForm, GetForm
from utils.crud import get_user_portfolios, get_portfolio_by_name, get_states_list

router = Router()


# ---------- Add state
@router.message(Command('add_state'))
async def add_state_handler(message: Message, state: FSMContext):
    await state.set_state(AddForm.state_portfolio_name)
    portfolios = await get_user_portfolios(user_id=message.from_user.id)
    keyboard = create_portfolio_keyboard(portfolios)
    await message.answer(
        'Choose portfolio: ',
        reply_markup=keyboard.as_markup(resize_keyboard=True)
    )


@router.message(AddForm.state_portfolio_name)
async def getting_state_portfolio_id_handler(message: Message, state: FSMContext):
    portfolio = await get_portfolio_by_name(
        name=message.text,
        user_id=message.from_user.id
    )
    await state.update_data(portfolio_id=portfolio.id)
    await state.set_state(AddForm.rub_result)
    await message.answer(
        'Enter portfolio RUB result: ',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(AddForm.rub_result)
async def getting_rub_result_handler(message: Message, state: FSMContext):
    await state.update_data(rub_result=float(message.text))
    await state.set_state(AddForm.usd_result)
    await message.answer(
        'Enter portfolio USD result: ',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(AddForm.usd_result)
async def getting_usd_result_handler(message: Message, state: FSMContext):
    data = await state.update_data(usd_result=float(message.text), created_at=datetime.now())
    state_object = StateSchema(**data)
    await APIHandler().post_object(StateSchema, state_object)
    await message.answer(
        'State added',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()


# ---------- Get states

@router.message(Command('get_states'))
async def get_state_handler(message: Message, state: FSMContext):
    await state.set_state(GetForm.state_portfolio_name)
    portfolios = await get_user_portfolios(user_id=message.from_user.id)
    keyboard = create_portfolio_keyboard(portfolios)
    await message.answer(
        'Choose portfolio: ',
        reply_markup=keyboard.as_markup(resize_keyboard=True)
    )


@router.message(GetForm.state_portfolio_name)
async def getting_portfolio_name_handler(message: Message, state: FSMContext):
    portfolio = await get_portfolio_by_name(
        name=message.text,
        user_id=message.from_user.id
    )
    states = await get_states_list(portfolio_id=portfolio.id)
    state_pattern = """
    -------------
    USD result: {}
    RUB result: {}
    Created at: {}
    """
    states_string = '\n'.join(
        [state_pattern.format(state.usd_result, state.rub_result, state.created_at) for state in states]
    )
    msg = 'No states yet' if len(states) < 0 else states_string
    await message.answer(
        msg,
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()
