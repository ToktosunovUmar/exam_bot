import asyncio
from aiogram import Bot
import logging

from bot_config import bot, dp, database
from handlers.survey import survey_router
from handlers.echo import echo_router


async def on_startup(bot: Bot):
    print("запустился")
    database.create_tables()


async def main():
    dp.startup.register(on_startup)
    dp.include_router(survey_router)
    dp.include_router(echo_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
