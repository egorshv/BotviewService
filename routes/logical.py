from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, FSInputFile

from callbacks.portfolio import PortfolioCallback
from callbacks.trade import TradeCallback
from keyboards.KeyboardCreator import KeyboardCreator
from schemas.currency import Currency
from schemas.trade import TradeMark
from services.ChartCreator import ChartCreator
from services.UserStorageManager import UserStorageManager
from settings import CHART_FILENAME
from states.logical import GetChart, SetMark
from utils.charts import get_portfolio_chart_data
from utils.validators import is_currency, is_mark

router = Router()


# ---------- Calculate precision

@router.message(Command('calculate_precision'))
async def calculate_precision_handler(message: Message):
    portfolios = await UserStorageManager(user_id=message.from_user.id).get_portfolios()
    keyboard = KeyboardCreator().create_portfolio_keyboard(portfolios, 'precision-calculate')
    await message.answer(
        'Choose portfolio: ',
        reply_markup=keyboard
    )


@router.callback_query(PortfolioCallback.filter(F.type == 'precision-calculate'))
async def calculate_precision_callback(query: CallbackQuery, callback_data: PortfolioCallback):
    precision = await UserStorageManager(user_id=query.message.from_user.id).calculate_portfolio_precision(
        portfolio_id=callback_data.id
    )
    await query.message.answer(
        f'Current portfolio precision: {precision}',
        reply_markup=ReplyKeyboardRemove()
    )


# ---------- Calculate recall

@router.message(Command('calculate_recall'))
async def calculate_recall(message: Message):
    portfolios = await UserStorageManager(user_id=message.from_user.id).get_portfolios()
    keyboard = KeyboardCreator().create_portfolio_keyboard(portfolios, 'recall-calculate')
    await message.answer(
        'Choose portfolio: ',
        reply_markup=keyboard
    )


@router.callback_query(PortfolioCallback.filter(F.type == 'recall-calculate'))
async def calculate_recall_callback(query: CallbackQuery, callback_data: PortfolioCallback):
    recall = await UserStorageManager(user_id=query.message.from_user.id).calculate_portfolio_recall(
        portfolio_id=callback_data.id
    )
    await query.message.answer(
        f'Current recall: {recall}',
        reply_markup=ReplyKeyboardRemove()
    )


# ---------- Get chart

@router.message(Command('get_chart'))
async def get_chart_handler(message: Message):
    portfolios = await UserStorageManager(user_id=message.from_user.id).get_portfolios()
    keyboard = KeyboardCreator().create_portfolio_keyboard(portfolios, 'chart-get')
    await message.answer(
        'Choose portfolio: ',
        reply_markup=keyboard
    )


@router.callback_query(PortfolioCallback.filter(F.type == 'chart-get'))
async def get_chart_callback(query: CallbackQuery, callback_data: PortfolioCallback, state: FSMContext):
    await state.set_state(GetChart.currency)
    await state.update_data(portfolio_id=callback_data.id)
    keyboard = KeyboardCreator().get_currency_keyboard()
    await query.message.answer(
        'Choose currency: ',
        reply_markup=keyboard
    )


@router.message(GetChart.currency)
async def getting_chart_currency_handler(message: Message, state: FSMContext):
    if not is_currency(message.text):
        await state.set_state(GetChart.currency)
        keyboard = KeyboardCreator().get_currency_keyboard()
        return await message.answer(
            'Wrong currency value, try again',
            reply_markup=keyboard
        )

    data = await state.get_data()
    portfolio = await UserStorageManager(user_id=message.from_user.id).get_portfolio(
        portfolio_id=data.get('portfolio_id')
    )

    chart_data = await get_portfolio_chart_data(
        user_id=message.from_user.id,
        portfolio_name=portfolio.name,
        portfolio_id=data.get('portfolio_id'),
        currency=Currency(message.text)
    )

    chart_creator = ChartCreator(CHART_FILENAME)
    chart_creator.create_line_chart(chart_data, f'{portfolio.name}: {message.text}')
    chart_file = FSInputFile(CHART_FILENAME)
    await message.answer_document(chart_file)
    await state.clear()


# ---------- Set trade mark

@router.message(Command('set_trade_mark'))
async def set_trade_mark_handler(message: Message):
    portfolios = await UserStorageManager(user_id=message.from_user.id).get_portfolios()
    keyboard = KeyboardCreator().create_portfolio_keyboard(portfolios, 'trade-mark-set')
    await message.answer(
        'Choose portfolio: ',
        reply_markup=keyboard
    )


@router.callback_query(PortfolioCallback.filter(F.type == 'trade-mark-set'))
async def set_trade_mark_callback(query: CallbackQuery, callback_data: PortfolioCallback):
    trades = await UserStorageManager(user_id=query.message.from_user.id).get_trades(
        portfolio_id=callback_data.id
    )
    keyboard = KeyboardCreator().create_trade_keyboard(trades, 'mark-set')
    await query.message.answer(
        'Choose trade: ',
        reply_markup=keyboard
    )


@router.callback_query(TradeCallback.filter(F.type == 'mark-set'))
async def get_trade_mark_callback(query: CallbackQuery, callback_data: TradeCallback, state: FSMContext):
    await state.set_state(SetMark.mark)
    await state.update_data(id=callback_data.id)

    keyboard = KeyboardCreator().get_trade_marks_keyboard()
    await query.message.answer(
        'Choose mark: ',
        reply_markup=keyboard
    )


@router.message(SetMark.mark)
async def set_mark_handler(message: Message, state: FSMContext):
    if not is_mark(message.text):
        keyboard = KeyboardCreator().get_trade_marks_keyboard()
        await message.answer(
            'Wrong trade mark value, try again',
            reply_markup=keyboard
        )
        return await state.set_state(SetMark.mark)

    data = await state.update_data(mark=TradeMark(message.text))
    storage_manager = UserStorageManager(user_id=message.from_user.id)

    [trade] = await storage_manager.get_trades(
        id=data.get('id')
    )
    trade.mark = data.get('mark')
    await storage_manager.update_trade(
        trade_id=trade.id,
        trade=trade
    )
    await message.answer(
        'Trade marked',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()
