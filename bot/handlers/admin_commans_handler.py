from aiogram import Router
from aiogram.filters import Command
from aiogram import types
from bot.console_log import logger
from bot.admin_list import admin_list
import json

from database.manager import database, User

router = Router()
dispatcher = None
bot = None
resetter = None

@router.message(Command('say'))
async def help(message: types.Message):
    if message.from_user.id in admin_list:
        logger.telegram.log_command(message.from_user.username, "/say")
        
        text = message.text[4::]
        
        text = f"<b>[ADMIN]</b> {text}"
        
        for user_id in await database.user.get_ids():
            try:
                await bot.send_message(chat_id=user_id,
                                    text=text)
            except Exception as e:
                print(user_id, ' ошибка отправки сообщения')
                
@router.message(Command('stop'))
async def help(message: types.Message):
    if message.from_user.id in admin_list:
        logger.telegram.log_command(message.from_user.username, "/stop")
        
        await dispatcher.stop_polling()
        resetter.stop()