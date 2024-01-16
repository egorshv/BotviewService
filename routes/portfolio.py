from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from pydantic import ValidationError

from callbacks.portfolio import PortfolioCallback
from keyboards.KeyboardCreator import KeyboardCreator
from schemas.portfolio import PortfolioSchema
from services.UserStorageManager import UserStorageManager
from states.portfolio import AddForm, UpdateForm
from aiohttp.client_exceptions import ClientConnectorError

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
    if not message.text.isdigit():
        await message.answer(
            'Wrong field value, try again.',
            reply_markup=ReplyKeyboardRemove()
        )
        return await state.set_state(AddForm.deposited_money)

    data = await state.update_data(user_id=message.from_user.id, deposited_money=int(message.text))
    try:
        portfolio = PortfolioSchema(**data)
        await UserStorageManager(user_id=message.from_user.id).add_portfolio(portfolio)
        await message.answer(
            'Portfolio added',
            reply_markup=ReplyKeyboardRemove()
        )
    except ValidationError:
        await message.answer(
            f'Validation error, try again',
            reply_markup=ReplyKeyboardRemove()
        )
    except ClientConnectorError:
        await message.answer(
            'Network error, try again',
            reply_markup=ReplyKeyboardRemove()
        )
    finally:
        await state.clear()


# ---------- Delete portfolio

@router.message(Command('delete_portfolio'))
async def delete_portfolio_handler(message: Message):
    portfolios = await UserStorageManager(user_id=message.from_user.id).get_portfolios()
    portfolio_keyboard = KeyboardCreator().create_portfolio_keyboard(portfolios, 'delete')
    await message.answer(
        'Choose deleting portfolio: ',
        reply_markup=portfolio_keyboard
    )


@router.callback_query(PortfolioCallback.filter(F.type == 'delete'))
async def deleting_portfolio_callback(query: CallbackQuery, callback_data: PortfolioCallback):
    await UserStorageManager(user_id=query.message.from_user.id).delete_portfolio(
        callback_data.id
    )
    await query.message.answer(
        'Portfolio deleted',
        reply_markup=ReplyKeyboardRemove()
    )


# ---------- Get portfolio


@router.message(Command('get_portfolio'))
async def get_portfolio_handler(message: Message):
    portfolios = await UserStorageManager(user_id=message.from_user.id).get_portfolios()
    portfolio_keyboard = KeyboardCreator().create_portfolio_keyboard(portfolios, 'get')
    await message.answer(
        'Choose getting portfolio: ',
        reply_markup=portfolio_keyboard
    )


@router.callback_query(PortfolioCallback.filter(F.type == 'get'))
async def portfolio_id_callback(query: CallbackQuery, callback_data: PortfolioCallback):
    portfolio = await UserStorageManager(user_id=query.message.from_user.id).get_portfolio(
        callback_data.id
    )
    await query.message.answer(
        f'Portfolio {portfolio.name}\n'
        f'id: {portfolio.id}\n'
        f'Last precision: {portfolio.last_precision}\n'
        f'Last recall: {portfolio.last_recall}\n'
        f'Deposited money: {portfolio.deposited_money}\n',
        reply_markup=ReplyKeyboardRemove()
    )


# ---------- Update portfolio

@router.message(Command('update_portfolio'))
async def update_portfolio_handler(message: Message):
    portfolios = await UserStorageManager(user_id=message.from_user.id).get_portfolios()
    portfolio_keyboard = KeyboardCreator().create_portfolio_keyboard(portfolios, 'update')
    await message.answer(
        'Choose updating portfolio: ',
        reply_markup=portfolio_keyboard
    )


@router.callback_query(PortfolioCallback.filter(F.type == 'update'))
async def update_portfolio_callback(query: CallbackQuery, callback_data: PortfolioCallback, state: FSMContext):
    await state.set_state(UpdateForm.name)
    await state.update_data(id=callback_data.id)
    await query.message.answer(
        f'Enter new name: ',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(UpdateForm.name)
async def getting_updating_field_handler(message: Message, state: FSMContext):
    await state.update_data(name=message.text, user_id=message.from_user.id)
    await state.set_state(UpdateForm.deposited_money)
    await message.answer(
        f'Enter new deposited money: ',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(UpdateForm.deposited_money)
async def getting_updating_field_handler(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer(
            'Wrong field value, try again',
            reply_markup=ReplyKeyboardRemove()
        )
        return await state.set_state(UpdateForm.deposited_money)

    data = await state.update_data(deposited_money=float(message.text))
    try:
        portfolio = PortfolioSchema(**data)
        await UserStorageManager(user_id=portfolio.user_id).update_portfolio(
            portfolio_id=portfolio.id,
            portfolio=portfolio
        )
        await message.answer(
            'Portfolio updated',
            reply_markup=ReplyKeyboardRemove()
        )
    except ValidationError:
        await message.answer(
            'Validation error, try again',
            reply_markup=ReplyKeyboardRemove()
        )
    except ClientConnectorError:
        await message.answer(
            'Network error, try again',
            reply_markup=ReplyKeyboardRemove()
        )
    finally:
        await state.clear()
