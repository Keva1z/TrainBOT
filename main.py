import asyncio
from aiogram import Bot, Dispatcher
from database.manager import database
from bot.console_log import logger
from threading import Thread
import os
import schedule
import time

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
    admin_commans_handler,
)

def resetter():
    
    print("Started daily resetter")
    
    def reset_daily():
        async def reset():
            logger.database.log("Resetting daily database data...")
            for user_id in database.user.get_ids():
                user = await database.user.load(user_id)
                user.completed_today = 0
                await database.user.save(user)
                
        loop.run_until_complete(reset())
        
    
    loop = asyncio.new_event_loop()
    
    schedule.every().day.do(reset_daily)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
    

async def main() -> None:
    load_dotenv('misc/.env')
    
    token = os.getenv('TOKEN_API')
    bot = Bot(token=token, parse_mode='html')
    dp = Dispatcher()
    
    menu_command_handler.bot = bot
    callback_handler.bot = bot
    profile_commands_handler.bot = bot
    admin_commans_handler.bot = bot
    
    dp.include_routers(
        admin_commans_handler.router,
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
    os.system('cls')
    logger.database.log("Loading database...")
    database.load()
    resetter = Thread(target=resetter).start()
    asyncio.run(main())


