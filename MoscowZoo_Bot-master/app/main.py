import asyncio
import logging
import os
import sys

from aiogram import Dispatcher, Bot
from aiogram.types import BotCommandScopeAllPrivateChats

from dotenv import find_dotenv, load_dotenv

from handlers.user_private import user_private_router
from app.common.get_animal_pic import get_animal_router
from handlers.quiz_handler import quiz_router
from common.bot_cmds_list import private


load_dotenv(find_dotenv())

ALLOWED_UPDATES = ['message', ]

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher()
dp.include_routers(user_private_router, get_animal_router, quiz_router)


async def main():

    await bot.set_my_commands(commands=private, scope=BotCommandScopeAllPrivateChats())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
