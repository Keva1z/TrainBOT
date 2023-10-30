from aiogram import Router
from aiogram.filters import CommandStart
from aiogram import types
from bot.console_log import logger
from bot.keyboards.keyboards import keyboard

from database.manager import database

router = Router()

@router.message(CommandStart())
async def start(message: types.Message):
    username = message.from_user.username
    logger.telegram.log_command(username, "/start")
    
    user_id = message.from_user.id
    name = message.from_user.first_name
    username = message.from_user.username
    
    user = await database.user.load(user_id)
    
    if user.name is None:
        user = await database.user.new(user_id, name, username)
    else:
        logger.database.log(f"User '{user_id} already exists!")
    
    text = f"""<b>Привет, {name}!</b>
                    
Я - Твой помощник для тренировок в телеграмм 📱.
Я помогу тебе тренироваться, а ты будешь получать за это <b>награды</b>
Для подробностей зайди в меню <u>'Информации о тренировках'</u>"""

    await message.answer(text, reply_markup=await keyboard.basic())
    
    