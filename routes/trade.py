from datetime import datetime

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from callbacks.portfolio import PortfolioCallback
from callbacks.trade import TradeCallback
from keyboards.KeyboardCreator import KeyboardCreator
from schemas.trade import TradeSchema
from services.UserStorageManager import UserStorageManager
from states.trade import AddForm, UpdateForm
from utils.validators import is_trade_action, isfloat, is_currency, is_mark

router = Router()


# ---------- Add trade

@router.message(Command('add_trade'))
async def add_trade_handler(message: Message):
    portfolios = await UserStorageManager(user_id=message.from_user.id).get_portfolios()
    keyboard = KeyboardCreator.create_portfolio_keyboard(portfolios, 'trade-add')
    await message.answer(
        'Choose portfolio: ',
        reply_markup=keyboard
    )


@router.callback_query(PortfolioCallback.filter(F.type == 'trade-add'))
async def getting_portfolio_id_callback(query: CallbackQuery, callback_data: PortfolioCallback, state: FSMContext):
    await state.set_state(AddForm.ticker)
    await state.update_data(portfolio_id=callback_data.id)
    await query.message.answer(
        'Enter stock ticker: ',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(AddForm.ticker)
async def get_stock_ticker_handler(message: Message, state: FSMContext):
    await state.update_data(ticker=message.text)
    await state.set_state(AddForm.action)
    keyboard = KeyboardCreator().get_trade_action_types_keyboard()
    await message.answer(
        'Choose trade action type: ',
        reply_markup=keyboard
    )


@router.message(AddForm.action)
async def get_action_type_handler(message: Message, state: FSMContext):
    if not is_trade_action(message.text.lower()):
        keyboard = KeyboardCreator().get_trade_action_types_keyboard()
        await message.answer(
            'It is not a valid trade action type, try again',
            reply_markup=keyboard
        )
        return await state.set_state(AddForm.action)
    await state.update_data(action=message.text.lower())
    await state.set_state(AddForm.value)
    await message.answer(
        'Enter trade value: ',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(AddForm.value)
async def get_trade_value_handler(message: Message, state: FSMContext):
    if not isfloat(message.text):
        await message.answer(
            'Wrong field value, try again',
            reply_markup=ReplyKeyboardRemove()
        )
        return await state.set_state(AddForm.value)
    await state.update_data(value=float(message.text))
    await state.set_state(AddForm.currency)
    keyboard = KeyboardCreator().get_currency_keyboard()
    await message.answer(
        'Choose trade currency: ',
        reply_markup=keyboard
    )


@router.message(AddForm.currency)
async def get_trade_currency_handler(message: Message, state: FSMContext):
    if not is_currency(message.text.lower()):
        keyboard = KeyboardCreator().get_currency_keyboard()
        await message.answer(
            'It is a not available currency, try again',
            reply_markup=keyboard
        )
        return await state.set_state(AddForm.currency)
    data = await state.update_data(currency=message.text.lower(), created_at=datetime.now())
    trade = TradeSchema(**data)
    await UserStorageManager(user_id=message.from_user.id).add_trade(trade)
    await state.clear()
    await message.answer(
        'Trade added',
        reply_markup=ReplyKeyboardRemove()
    )


# ---------- Get trades

@router.message(Command('get_trades'))
async def get_trades_handler(message: Message):
    portfolios = await UserStorageManager(user_id=message.from_user.id).get_portfolios()
    keyboard = KeyboardCreator.create_portfolio_keyboard(portfolios, 'trade-get')
    await message.answer(
        'Choose portfolio: ',
        reply_markup=keyboard
    )


@router.callback_query(PortfolioCallback.filter(F.type == 'trade-get'))
async def get_portfolio_trade_callback(query: CallbackQuery, callback_data: PortfolioCallback):
    trades = await UserStorageManager(user_id=query.message.from_user.id).get_trades(
        portfolio_id=callback_data.id
    )
    msg = 'No trades yet'
    msg = '\n'.join(list(map(str, trades))) if len(trades) > 0 else msg
    await query.message.answer(msg,
                               reply_markup=ReplyKeyboardRemove())


# ---------- Delete trade

@router.message(Command('delete_trade'))
async def delete_trade_handler(message: Message):
    portfolios = await UserStorageManager(user_id=message.from_user.id).get_portfolios()
    keyboard = KeyboardCreator.create_portfolio_keyboard(portfolios, 'trade-delete')
    await message.answer(
        'Choose portfolio: ',
        reply_markup=keyboard
    )


@router.callback_query(PortfolioCallback.filter(F.type == 'trade-delete'))
async def getting_portfolio_id_callback(query: CallbackQuery, callback_data: PortfolioCallback):
    trades = await UserStorageManager(user_id=query.message.from_user.id).get_trades(
        portfolio_id=callback_data.id
    )
    keyboard = KeyboardCreator().create_trade_keyboard(trades, 'delete')
    await query.message.answer(
        'Choose deleting trade: ',
        reply_markup=keyboard
    )


@router.callback_query(TradeCallback.filter(F.type == 'delete'))
async def getting_deleting_trade_id_callback(query: CallbackQuery, callback_data: TradeCallback):
    await UserStorageManager(user_id=query.message.from_user.id).delete_trade(callback_data.id)
    await query.message.answer(
        'Trade deleted',
        reply_markup=ReplyKeyboardRemove()
    )


# ---------- Update trade
@router.message(Command('update_trade'))
async def update_trade_handler(message: Message):
    portfolios = await UserStorageManager(user_id=message.from_user.id).get_portfolios()
    keyboard = KeyboardCreator().create_portfolio_keyboard(portfolios, 'trade-update')
    await message.answer(
        'Choose portfolio: ',
        reply_markup=keyboard
    )


@router.callback_query(PortfolioCallback.filter(F.type == 'trade-update'))
async def update_trade_callback(query: CallbackQuery, callback_data: PortfolioCallback):
    trades = await UserStorageManager(user_id=query.message.from_user.id).get_trades(
        portfolio_id=callback_data.id
    )
    keyboard = KeyboardCreator().create_trade_keyboard(trades, 'update')
    await query.message.answer(
        'Choose updating trade: ',
        reply_markup=keyboard
    )


@router.callback_query(TradeCallback.filter(F.type == 'update'))
async def getting_updating_trade_id_callback(query: CallbackQuery, callback_data: TradeCallback, state: FSMContext):
    await state.set_state(UpdateForm.ticker)
    await state.update_data(id=callback_data.id, portfolio_id=callback_data.portfolio_id)
    await query.message.answer(
        'Enter new ticker: ',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(UpdateForm.ticker)
async def getting_updating_ticker_handler(message: Message, state: FSMContext):
    await state.update_data(ticker=message.text)
    await state.set_state(UpdateForm.action)
    keyboard = KeyboardCreator().get_trade_action_types_keyboard()
    await message.answer(
        'Choose new action: ',
        reply_markup=keyboard
    )


@router.message(UpdateForm.action)
async def getting_updating_action_handler(message: Message, state: FSMContext):
    if not is_trade_action(message.text):
        keyboard = KeyboardCreator().get_trade_action_types_keyboard()
        await message.answer(
            'It is a not valid trade action type, try again',
            reply_markup=keyboard
        )
        return await state.set_state(UpdateForm.action)
    await state.update_data(action=message.text)
    await state.set_state(UpdateForm.value)
    await message.answer(
        'Enter new value: ',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(UpdateForm.value)
async def getting_updating_value_handler(message: Message, state: FSMContext):
    if not isfloat(message.text):
        await message.answer(
            'Wrong field value, try again',
            reply_markup=ReplyKeyboardRemove()
        )
        return await state.set_state(UpdateForm.value)
    await state.update_data(value=float(message.text))
    await state.set_state(UpdateForm.currency)
    keyboard = KeyboardCreator().get_currency_keyboard()
    await message.answer(
        'Choose currency: ',
        reply_markup=keyboard
    )


@router.message(UpdateForm.currency)
async def getting_updating_currency_handler(message: Message, state: FSMContext):
    if not is_currency(message.text):
        keyboard = KeyboardCreator().get_currency_keyboard()
        await message.answer(
            'It is a not available currency, try again',
            reply_markup=keyboard
        )
        return await state.set_state(UpdateForm.currency)
    await state.update_data(currency=message.text)
    await state.set_state(UpdateForm.mark)
    keyboard = KeyboardCreator().get_trade_marks_keyboard()
    await message.answer(
        'Choose mark: ',
        reply_markup=keyboard
    )


@router.message(UpdateForm.mark)
async def getting_updating_mark_handler(message: Message, state: FSMContext):
    if not is_mark(message.text):
        keyboard = KeyboardCreator().get_trade_marks_keyboard()
        await message.answer(
            'It is a not valid mark, try again',
            reply_markup=keyboard
        )
        return await state.set_state(UpdateForm.mark)
    await state.update_data(mark=message.text)
    await state.set_state(UpdateForm.result)
    await message.answer(
        'Enter trade result: ',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(UpdateForm.result)
async def getting_updating_result_handler(message: Message, state: FSMContext):
    if not isfloat(message.text):
        await message.answer(
            'Wrong field value, try again',
            reply_markup=ReplyKeyboardRemove()
        )
        return await state.set_state(UpdateForm.result)
    data = await state.update_data(result=float(message.text), created_at=datetime.now())
    await UserStorageManager(user_id=message.from_user.id).update_trade(data.get('id'), TradeSchema(**data))
    await message.answer(
        'Trade updated',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()
