from datetime import datetime

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from callbacks.portfolio import PortfolioCallback
from callbacks.state import StateCallback
from keyboards.KeyboardCreator import KeyboardCreator
from schemas.state import StateSchema
from services.UserStorageManager import UserStorageManager
from states.state import AddForm, UpdateForm

router = Router()


# ---------- Add state
@router.message(Command('add_state'))
async def add_state_handler(message: Message):
    portfolios = await UserStorageManager(user_id=message.from_user.id).get_portfolios()
    keyboard = KeyboardCreator.create_portfolio_keyboard(portfolios, 'state-add')
    await message.answer(
        'Choose portfolio: ',
        reply_markup=keyboard
    )


@router.callback_query(PortfolioCallback.filter(F.type == 'state-add'))
async def getting_portfolio_id_callback(query: CallbackQuery, callback_data: PortfolioCallback, state: FSMContext):
    await state.set_state(AddForm.rub_result)
    await state.update_data(portfolio_id=callback_data.id)
    await query.message.answer(
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
    await UserStorageManager(user_id=message.from_user.id).add_state(state_object)
    await message.answer(
        'State added',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()


# ---------- Get states

@router.message(Command('get_states'))
async def get_state_handler(message: Message):
    portfolios = await UserStorageManager(user_id=message.from_user.id).get_portfolios()
    keyboard = KeyboardCreator.create_portfolio_keyboard(portfolios, 'state-get')
    await message.answer(
        'Choose portfolio: ',
        reply_markup=keyboard
    )


@router.callback_query(PortfolioCallback.filter(F.type == 'state-get'))
async def getting_state_by_portfolio_id_callback(query: CallbackQuery, callback_data: PortfolioCallback):
    states = await UserStorageManager(user_id=query.message.from_user.id).get_states(
        portfolio_id=callback_data.id
    )
    states_string = '\n'.join(list(map(str, states)))
    msg = 'No states yet' if not states_string else states_string
    await query.message.answer(
        msg,
        reply_markup=ReplyKeyboardRemove()
    )


# ---------- Delete state


@router.message(Command('delete_state'))
async def delete_state_handler(message: Message):
    portfolios = await UserStorageManager(user_id=message.from_user.id).get_portfolios()
    keyboard = KeyboardCreator.create_portfolio_keyboard(portfolios, 'state-delete')
    await message.answer(
        'Choose portfolio: ',
        reply_markup=keyboard
    )


@router.callback_query(PortfolioCallback.filter(F.type == 'state-delete'))
async def getting_portfolio_id_callback(query: CallbackQuery, callback_data: PortfolioCallback):
    states = await UserStorageManager(user_id=query.message.from_user.id).get_states(
        portfolio_id=callback_data.id
    )
    keyboard = KeyboardCreator().create_state_keyboard(states, 'delete')
    await query.message.answer(
        'Choose deleting state: ',
        reply_markup=keyboard
    )


@router.callback_query(StateCallback.filter(F.type == 'delete'))
async def delete_state_callback(query: CallbackQuery, callback_data: StateCallback):
    await UserStorageManager(user_id=query.message.from_user.id).delete_state(callback_data.id)
    await query.message.answer(
        'State deleted',
        reply_markup=ReplyKeyboardRemove()
    )


# ---------- Update state

@router.message(Command('update_state'))
async def update_state_handler(message: Message):
    portfolios = await UserStorageManager(user_id=message.from_user.id).get_portfolios()
    keyboard = KeyboardCreator.create_portfolio_keyboard(portfolios, 'state-update')
    await message.answer(
        'Choose portfolio: ',
        reply_markup=keyboard
    )


@router.callback_query(PortfolioCallback.filter(F.type == 'state-update'))
async def getting_portfolio_id_callback(query: CallbackQuery, callback_data: PortfolioCallback):
    states = await UserStorageManager(user_id=query.message.from_user.id).get_states(
        portfolio_id=callback_data.id
    )
    keyboard = KeyboardCreator().create_state_keyboard(states, 'update')
    await query.message.answer(
        'Choose updating state: ',
        reply_markup=keyboard
    )


@router.callback_query(StateCallback.filter(F.type == 'update'))
async def getting_updating_state_id_callback(query: CallbackQuery, callback_data: StateCallback, state: FSMContext):
    await state.set_state(UpdateForm.rub_result)
    await state.update_data(id=callback_data.id, portfolio_id=callback_data.portfolio_id)
    await query.message.answer(
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
    await UserStorageManager(user_id=message.from_user.id).update_state(state_object.id, state_object)
    await state.clear()
    await message.answer(
        'State updated',
        reply_markup=ReplyKeyboardRemove()
    )
