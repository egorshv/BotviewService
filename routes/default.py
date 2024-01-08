from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


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
