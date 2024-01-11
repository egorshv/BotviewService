import logging
from datetime import datetime

from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router

from keyboards.portfolio import create_portfolio_keyboard
from keyboards.state import states_keyboard
from schemas.state import StateSchema
from services.APIHandler import APIHandler
from states.state import AddForm, GetForm, DeleteForm, UpdateForm
from utils.crud import get_user_portfolios, get_portfolio_by_name, get_states_list, delete_state, update_state

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
    msg = 'No states yet' if not states_string else states_string
    await message.answer(
        msg,
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()


# ---------- Delete state


@router.message(Command('delete_state'))
async def delete_state_handler(message: Message, state: FSMContext):
    await state.set_state(DeleteForm.state_portfolio_name)
    portfolios = await get_user_portfolios(user_id=message.from_user.id)
    keyboard = create_portfolio_keyboard(portfolios)
    await message.answer(
        'Choose portfolio: ',
        reply_markup=keyboard.as_markup(resize_keyboard=True)
    )


@router.message(DeleteForm.state_portfolio_name)
async def getting_deleting_state_portfolio_id_handler(message: Message, state: FSMContext):
    await state.set_state(DeleteForm.state_id)
    portfolio = await get_portfolio_by_name(
        name=message.text,
        user_id=message.from_user.id
    )
    states = await get_states_list(portfolio_id=portfolio.id)
    keyboard = states_keyboard(states)
    await message.answer(
        'Choose deleting state: ',
        reply_markup=keyboard.as_markup(resize_keyboard=True)
    )


@router.message(DeleteForm.state_id)
async def getting_deleting_state_id_handler(message: Message, state: FSMContext):
    msg = message.text
    state_id = int(msg[4:msg.index("|") - 1])
    logging.log(msg=state_id, level=logging.INFO)
    await delete_state(state_id)
    await message.answer(
        'State deleted',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()


# ---------- Update state

@router.message(Command('update_state'))
async def update_state_handler(message: Message, state: FSMContext):
    await state.set_state(UpdateForm.state_portfolio_name)
    portfolios = await get_user_portfolios(user_id=message.from_user.id)
    keyboard = create_portfolio_keyboard(portfolios)
    await message.answer(
        'Choose portfolio: ',
        reply_markup=keyboard.as_markup(resize_keyboard=True)
    )


@router.message(UpdateForm.state_portfolio_name)
async def getting_updating_state_portfolio_id_handler(message: Message, state: FSMContext):
    portfolio = await get_portfolio_by_name(
        name=message.text,
        user_id=message.from_user.id
    )
    states = await get_states_list(portfolio_id=portfolio.id)
    await state.update_data(portfolio_id=portfolio.id)
    keyboard = states_keyboard(states)
    await message.answer(
        'Choose updating state: ',
        reply_markup=keyboard.as_markup(resize_keyboard=True)
    )
    await state.set_state(UpdateForm.state_id)


@router.message(UpdateForm.state_id)
async def getting_updating_state_id_handler(message: Message, state: FSMContext):
    msg = message.text
    state_id = int(msg[4:msg.index('|') - 1])
    await state.update_data(id=state_id)
    await state.set_state(UpdateForm.rub_result)
    await message.answer(
        'Enter RUB result: ',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(UpdateForm.rub_result)
async def getting_updating_state_rub_result_handler(message: Message, state: FSMContext):
    await state.update_data(rub_result=float(message.text))
    await state.set_state(UpdateForm.usd_result)
    await message.answer(
        'Enter USD result: ',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(UpdateForm.usd_result)
async def getting_updating_state_usd_result_handler(message: Message, state: FSMContext):
    data = await state.update_data(usd_result=float(message.text), created_at=datetime.now())
    state_object = StateSchema(**data)
    await update_state(state_object.id, state_object)
    await state.clear()
    await message.answer(
        'State updated',
        reply_markup=ReplyKeyboardRemove()
    )
