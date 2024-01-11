from datetime import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.portfolio import create_portfolio_keyboard
from keyboards.trade import trade_action_types, trade_currency, trade_keyboard, trade_marks
from schemas.trade import TradeSchema
from services.APIHandler import APIHandler
from states.trade import AddForm, GetForm, DeleteForm, UpdateForm
from utils.crud import get_user_portfolios, get_portfolio_by_name, get_trades_list, delete_trade, update_trade

router = Router()


# ---------- Add trade

@router.message(Command('add_trade'))
async def add_trade_handler(message: Message, state: FSMContext):
    await state.set_state(AddForm.trade_portfolio_name)
    portfolios = await get_user_portfolios(message.from_user.id)
    keyboard = create_portfolio_keyboard(portfolios)
    await message.answer(
        'Choose portfolio: ',
        reply_markup=keyboard.as_markup(resize_keyboard=True)
    )


@router.message(AddForm.trade_portfolio_name)
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
        reply_markup=keyboard.as_markup(resize_keyboard=True)
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
        reply_markup=keyboard.as_markup(resize_keyboard=True)
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
    await state.set_state(GetForm.trade_portfolio_name)
    portfolios = await get_user_portfolios(message.from_user.id)
    keyboard = create_portfolio_keyboard(portfolios)
    await message.answer(
        'Choose portfolio: ',
        reply_markup=keyboard.as_markup(resize_keyboard=True)
    )


@router.message(GetForm.trade_portfolio_name)
async def get_trades_portfolio_name_handler(message: Message, state: FSMContext):
    portfolio = await get_portfolio_by_name(message.text, message.from_user.id)
    trades = await get_trades_list(portfolio_id=portfolio.id)
    msg = 'No trades yet'
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
    msg = '\n'.join(trades_strings) if len(trades) > 0 else msg
    await message.answer(msg,
                         reply_markup=ReplyKeyboardRemove())
    await state.clear()


# ---------- Delete trades

@router.message(Command('delete_trade'))
async def delete_trade_handler(message: Message, state: FSMContext):
    await state.set_state(DeleteForm.trade_portfolio_name)
    portfolios = await get_user_portfolios(message.from_user.id)
    keyboard = create_portfolio_keyboard(portfolios)
    await message.answer(
        'Choose portfolio: ',
        reply_markup=keyboard.as_markup(resize_keyboard=True)
    )


@router.message(DeleteForm.trade_portfolio_name)
async def getting_deleting_trade_portfolio_name_handler(message: Message, state: FSMContext):
    await state.set_state(DeleteForm.trade_id)
    portfolio = await get_portfolio_by_name(name=message.text,
                                            user_id=message.from_user.id)
    trades = await get_trades_list(portfolio_id=portfolio.id)
    keyboard = trade_keyboard(trades)
    await message.answer(
        "Choose deleting trade: ",
        reply_markup=keyboard.as_markup(resize_keyboard=True)
    )


@router.message(DeleteForm.trade_id)
async def deleting_portfolio_trade_handler(message: Message, state: FSMContext):
    msg = message.text
    trade_id = int(msg[4:msg.index('|') - 1])
    await delete_trade(trade_id)
    await message.answer(
        'Trade deleted',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()


# ---------- Delete trades
@router.message(Command('update_trade'))
async def update_trade_handler(message: Message, state: FSMContext):
    await state.set_state(UpdateForm.trade_portfolio_name)
    portfolios = await get_user_portfolios(message.from_user.id)
    keyboard = create_portfolio_keyboard(portfolios)
    await message.answer(
        'Choose portfolio: ',
        reply_markup=keyboard.as_markup(resize_keyboard=True)
    )


@router.message(UpdateForm.trade_portfolio_name)
async def getting_updating_portfolio_name_handler(message: Message, state: FSMContext):
    await state.set_state(UpdateForm.trade_id)
    portfolio = await get_portfolio_by_name(
        name=message.text,
        user_id=message.from_user.id
    )
    await state.update_data(portfolio_id=portfolio.id)
    trades = await get_trades_list(portfolio_id=portfolio.id)
    keyboard = trade_keyboard(trades)
    await message.answer(
        'Choose updating trade: ',
        reply_markup=keyboard.as_markup(resize_keyboard=True)
    )


@router.message(UpdateForm.trade_id)
async def getting_updating_trade_id_handler(message: Message, state: FSMContext):
    msg = message.text
    await state.update_data(id=int(msg[4:msg.index('|') - 1]))
    await state.set_state(UpdateForm.ticker)
    await message.answer(
        'Enter new ticker: ',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(UpdateForm.ticker)
async def getting_updating_ticker_handler(message: Message, state: FSMContext):
    await state.update_data(ticker=message.text)
    await state.set_state(UpdateForm.action)
    keyboard = trade_action_types()
    await message.answer(
        'Choose new action: ',
        reply_markup=keyboard.as_markup(resize_keyboard=True)
    )


@router.message(UpdateForm.action)
async def getting_updating_action_handler(message: Message, state: FSMContext):
    await state.update_data(action=message.text)
    await state.set_state(UpdateForm.value)
    await message.answer(
        'Enter new value: ',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(UpdateForm.value)
async def getting_updating_value_handler(message: Message, state: FSMContext):
    await state.update_data(value=float(message.text))
    await state.set_state(UpdateForm.currency)
    keyboard = trade_currency()
    await message.answer(
        'Choose currency: ',
        reply_markup=keyboard.as_markup(resize_keyboard=True)
    )


@router.message(UpdateForm.currency)
async def getting_updating_currency_handler(message: Message, state: FSMContext):
    await state.update_data(currency=message.text)
    await state.set_state(UpdateForm.mark)
    keyboard = trade_marks()
    await message.answer(
        'Choose mark: ',
        reply_markup=keyboard.as_markup(resize_keyboard=True)
    )


@router.message(UpdateForm.mark)
async def getting_updating_mark_handler(message: Message, state: FSMContext):
    await state.update_data(mark=message.text)
    await state.set_state(UpdateForm.result)
    await message.answer(
        'Enter trade result: ',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(UpdateForm.result)
async def getting_updating_result_handler(message: Message, state: FSMContext):
    data = await state.update_data(result=float(message.text), created_at=datetime.now())
    await update_trade(data.get('id'), TradeSchema(**data))
    await message.answer(
        'Trade updated',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()
