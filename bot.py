import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from routes import default, portfolio, trade, state, operation, logical

from settings import TOKEN


async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(bot=bot)

    dp.include_routers(default.router,
                       portfolio.router,
                       trade.router,
                       state.router,
                       operation.router,
                       logical.router,
                       )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
