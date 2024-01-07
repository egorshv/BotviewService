import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode

from settings import TOKEN


async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(bot=bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
