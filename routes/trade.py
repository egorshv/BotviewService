from datetime import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.portfolio_keyboards import create_portfolio_keyboard
from keyboards.trade_keyboards import trade_action_types, trade_currency
from schemas.trade import TradeSchema
from services.APIHandler import APIHandler
from states.trade import AddForm, GetForm
from utils.crud import get_user_portfolios, get_portfolio_by_name, get_trades_by_portfolio_id

router = Router()


# ---------- Add trade

@router.message(Command('add_trade'))
async def add_trade_handler(message: Message, state: FSMContext):
    await state.set_state(AddForm.portfolio_name)
    portfolios = await get_user_portfolios(message.from_user.id)
    keyboard = create_portfolio_keyboard(portfolios)
    await message.answer(
        'Choose portfolio: ',
        reply_markup=keyboard.as_markup()
    )


@router.message(AddForm.portfolio_name)
async def get_portfolio_name_handler(message: Message, state: FSMContext):
    portfolio = await get_portfolio_by_name(message.text, message.from_user.id)
    await state.update_data(portfolio_id=portfolio.id)
    await state.set_state(AddForm.ticker)
    await message.answer(
        'Enter stock ticker: ',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(AddForm.ticker)
async def get_stock_ticker_handler(message: Message, state: FSMContext):
    await state.update_data(ticker=message.text)
    await state.set_state(AddForm.action)
    keyboard = trade_action_types()
    await message.answer(
        'Choose trade action type: ',
        reply_markup=keyboard.as_markup()
    )


@router.message(AddForm.action)
async def get_action_type_handler(message: Message, state: FSMContext):
    await state.update_data(action=message.text.lower())
    await state.set_state(AddForm.value)
    await message.answer(
        'Enter trade value: ',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(AddForm.value)
async def get_trade_value_handler(message: Message, state: FSMContext):
    await state.update_data(value=float(message.text))
    await state.set_state(AddForm.currency)
    keyboard = trade_currency()
    await message.answer(
        'Choose trade currency: ',
        reply_markup=keyboard.as_markup()
    )


@router.message(AddForm.currency)
async def get_trade_currency_handler(message: Message, state: FSMContext):
    await state.update_data(currency=message.text.lower())
    data = await state.update_data(created_at=datetime.now())
    trade = TradeSchema(**data)
    await APIHandler().post_object(TradeSchema, trade)
    await state.clear()
    await message.answer(
        'Trade added',
        reply_markup=ReplyKeyboardRemove()
    )


# ---------- Get trades

@router.message(Command('get_trades'))
async def get_trades_handler(message: Message, state: FSMContext):
    await state.set_state(GetForm.portfolio_name)
    portfolios = await get_user_portfolios(message.from_user.id)
    keyboard = create_portfolio_keyboard(portfolios)
    await message.answer(
        'Choose portfolio: ',
        reply_markup=keyboard.as_markup()
    )


@router.message(GetForm.portfolio_name)
async def get_trades_portfolio_name_handler(message: Message, state: FSMContext):
    portfolio = await get_portfolio_by_name(message.text, message.from_user.id)
    trades = await get_trades_by_portfolio_id(portfolio.id, message.from_user.id)
    trade_pattern = """
        ---------------------
        ticker: {}
        action: {}
        value: {}
        currency: {}
        created_at: {}
        result: {}
        mark: {}
    """
    trades_strings = [trade_pattern.format(
        trade.ticker,
        trade.action,
        trade.value,
        trade.currency,
        trade.created_at,
        trade.result,
        trade.mark
    ) for trade in trades]
    await message.answer('\n'.join(trades_strings),
                         reply_markup=ReplyKeyboardRemove())
    await state.clear()

# ---------- Delete trades
