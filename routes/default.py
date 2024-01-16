import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.formatting import Text

router = Router()


@router.message(Command('cancel'))
@router.message(F.text.lower() == 'cancel')
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    await state.clear()
    await message.reply('canceled', reply_markup=ReplyKeyboardRemove())


@router.message(Command('start'))
async def start_command(message: Message):
    await message.answer('This is bot for logging investing data and getting advanced statistic')


@router.message(Command('help'))
async def help_command(message: Message):
    await message.answer('Full list of available commands:'
                         '\n/add_trade, /update_trade, /delete_trade, /get_trade'
                         '\n/add_operation, /get_operation, /update_operation, /delete_operation'
                         '\n/add_state, /get_state, /delete_state, /update_state'
                         '\n/add_portfolio, /get_portfolio, /delete_portfolio, /update_portfolio'
                         '\n/portfolio_statistic, /portfolio_chart')
