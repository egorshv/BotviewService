from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.portfolio import create_portfolio_keyboard
from schemas.portfolio import PortfolioSchema
from services.APIHandler import APIHandler
from states.portfolio import AddForm, DeleteForm, GetForm, UpdateForm
from utils.crud import get_user_portfolios, get_portfolio_by_name, update_portfolio

router = Router()


# ---------- Add portfolio

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


# ---------- Delete portfolio

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


# ---------- Get portfolio


@router.message(Command('get_portfolio'))
async def get_portfolio_handler(message: Message, state: FSMContext):
    portfolios = await get_user_portfolios(message.from_user.id)
    portfolio_keyboard = create_portfolio_keyboard(portfolios)
    await state.set_state(GetForm.name)
    await message.answer(
        'Choose getting portfolio: ',
        reply_markup=portfolio_keyboard.as_markup()
    )


@router.message(GetForm.name)
async def getting_portfolio_name(message: Message, state: FSMContext):
    try:
        portfolio = await get_portfolio_by_name(message.text, message.from_user.id)
        await message.answer(
            f'Portfolio {portfolio.name}\n'
            f'id: {portfolio.id}\n'
            f'Last precision: {portfolio.last_precision}\n'
            f'Last recall: {portfolio.last_recall}\n'
            f'Deposited money: {portfolio.deposited_money}\n',
            reply_markup=ReplyKeyboardRemove()
        )
    except Exception as ex:
        await message.answer(
            f'Something went wrong, error: {ex}',
            reply_markup=ReplyKeyboardRemove()
        )
    finally:
        await state.clear()


# ---------- Update portfolio

@router.message(Command('update_portfolio'))
async def update_portfolio_handler(message: Message, state: FSMContext):
    portfolios = await get_user_portfolios(message.from_user.id)
    portfolio_keyboard = create_portfolio_keyboard(portfolios)
    await state.set_state(UpdateForm.name)
    await message.answer(
        'Choose updating portfolio: ',
        reply_markup=portfolio_keyboard.as_markup()
    )


@router.message(UpdateForm.name)
async def getting_update_name_handler(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(UpdateForm.new_name)
    await message.answer(
        'Enter new name: ',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(UpdateForm.new_name)
async def getting_updating_field_handler(message: Message, state: FSMContext):
    await state.update_data(new_name=message.text)
    await state.set_state(UpdateForm.new_deposited_money)
    await message.answer(
        'Enter new deposited money: ',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(UpdateForm.new_deposited_money)
async def getting_updating_field_handler(message: Message, state: FSMContext):
    try:
        data = await state.update_data(new_deposited_money=float(message.text))
        await update_portfolio(data.get('name'),
                               message.from_user.id,
                               data.get('new_name'),
                               data.get('new_deposited_money'))

        await message.answer(
            'Portfolio updated',
            reply_markup=ReplyKeyboardRemove()
        )
    except Exception as e:
        await message.answer(
            f'Something went wrong: {e}',
            reply_markup=ReplyKeyboardRemove()
        )
    finally:
        await state.clear()
