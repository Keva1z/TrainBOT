from aiogram import Router, F
from aiogram import types
from bot.handlers.menu_command_handler import help, info, profile, rewards, training
from bot.console_log import logger

from database.manager import database

router = Router()

@router.message(F.text)
async def message(message: types.Message):
    
    text = message.text
    
    user_id = message.from_user.id
    username = message.from_user.username
    user_name = message.from_user.first_name
    
    user = await database.user.load(user_id)
    
    if user.name != user_name or user.username != username:
        user.name = user_name
        user.username = username
        
        await database.user.save(user)
        logger.database.log(f"User {user_id} changed name or username successfully")
    
    if text == '🏆 Мои награды':
        bot_msg = await message.answer("⏳ Получаю данные призов...")
        await rewards(message, user=user, bot_msg=bot_msg)
    
    elif text == 'ℹ️ Информация о тренировках':
        bot_msg = await message.answer("⏳ Получаю информацию о тренировках...")
        await info(message, user=user, bot_msg=bot_msg)
        
    elif text == '🦾 Упражнение':
        bot_msg = await message.answer("⏳ Получаю тренировку...")
        await training(message, user=user, bot_msg=bot_msg)
        
    elif text == '👤 Профиль':
        bot_msg = await message.answer("⏳ Получаю данные профиля...")
        await profile(message, user=user, bot_msg=bot_msg)
        
    elif text == '❓ Комманды':
        bot_msg = await message.answer("⏳ Получаю все комманды...")
        await help(message, bot_msg=bot_msg)
        