import asyncio
from aiogram import Bot, Dispatcher
from database.manager import database

from dotenv import load_dotenv
import os

from bot.handlers import (
    start_handler,
    menu_handler,
    menu_command_handler,
    callback_handler,
    form_handler,
    plan_commands_handler,
    profile_commands_handler,
    rewards_command_handler,
)

async def main() -> None:
    load_dotenv('misc/.env')
    
    token = os.getenv('TOKEN_API')
    bot = Bot(token=token, parse_mode='html')
    dp = Dispatcher()
    
    menu_command_handler.bot = bot
    callback_handler.bot = bot
    profile_commands_handler.bot = bot
    
    dp.include_routers(
        rewards_command_handler.router,
        profile_commands_handler.router,
        plan_commands_handler.router,
        form_handler.router,
        menu_command_handler.router,
        start_handler.router,
        menu_handler.router,
        callback_handler.router,
    )
    
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    database.load()
    asyncio.run(main())


