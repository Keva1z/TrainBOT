from bot.keyboards.keyboards import keyboard as kb
from aiogram.filters import Command
from bot.console_log import logger
from aiogram import Router
from aiogram import types

from database.manager import database

router = Router()
bot = None

@router.message(Command('set_sex'))
async def set_sex(message: types.Message):
    logger.telegram.log_command(message.from_user.username, "/set_sex")

    bot_msg = await message.answer("⏳ Запускаю программу смены пола...")
    
    text = f"""<b>Выберите пол</b>"""
    
    chatID = message.chat.id
    msg_id = bot_msg.message_id
    await bot.edit_message_text(text = text,
                                chat_id= chatID,
                                message_id= msg_id,
                                reply_markup=await kb.sex())
    
@router.message(Command('set_partner'))
async def set_partner(message: types.Message):
    logger.telegram.log_command(message.from_user.username, "/set_partner")
    
    user_id = message.from_user.id
    user = await database.user.load(user_id)
    
    commands = message.text.split(' ')
    arg1 = commands[-1]
    try:
        arg1 = int(arg1)
        if user.partner_id is None:
            if arg1 in await database.user.get_ids():
                partner = await database.user.load(arg1)
                if partner.partner_id is None:
                    msg_id = await bot.send_message(chat_id=arg1,
                                        text=f'<a href="tg://user?id={arg1}">Пользователь</a> хочет стать вашим партнером.'
                                        )
                    keyboard = await kb.acc_decl(arg1, user_id, msg_id)
                    await bot.send_message(chat_id=arg1,
                                        text=f'Согласиться / Отказаться',
                                        reply_markup=keyboard,
                                        )
                else:
                    await message.answer("У человека уже есть партнёр!")
            else:
                await message.answer(f"Похоже вы ввели неверный ID, или партнер не пользуется ботом!",
                                    reply_markup=await kb.basic())
        else:
            await message.answer("У вас уже есть партнёр!")
    except ValueError:
        await message.answer(f"Пожалуйста, введите число как аргумент комманды",
                                parse_mode="HTML",
                                reply_markup=await kb.basic())
        
@router.message(Command('leave_partner'))
async def leave_partner(message: types.Message):
    logger.telegram.log_command(message.from_user.username, "/leave_partner")
    
    user_id = message.from_user.id
    user = await database.user.load(user_id)
    partner_id = user.partner_id
    partner = await database.user.load(partner_id)
    user.partner_id = None
    partner.partner_id = None
    await database.user.save([user, partner])
    
    await message.answer(f'Вы вышли из партнёрства с <b>{partner.name}</b>',
                         reply_markup=await kb.basic())
    
    await bot.send_message(chat_id=partner_id,
                           text=f'Ваш партнёр <b>{user.name}</b> вышел из партнёрства!',
                           reply_markup=await kb.basic())
    
@router.message(Command('start_weight'))
async def start_weight(message: types.Message):
    logger.telegram.log_command(message.from_user.username, "/start_weight")
    
    user_id = message.from_user.id
    user = await database.user.load(user_id)
    
    command = message.text.split(' ')
    arg1 = command[-1]
    try: 
        arg1 = float(arg1)
        user.start_weight = arg1
        await message.answer(f"Обновил ваш начальный вес!",
                                reply_markup=await kb.basic())
        await database.user.save(user)
    except: 
        await message.answer(f"Пожалуйста, введите число как аргумент комманды",
                                reply_markup=await kb.basic())
        
@router.message(Command('set_weight'))
async def set_weight(message: types.Message):
    logger.telegram.log_command(message.from_user.username, "/set_weight")
    
    user_id = message.from_user.id
    user = await database.user.load(user_id)
    
    command = message.text.split(' ')
    arg1 = command[-1]
    try: 
        arg1 = float(arg1)
        user.current_weight = arg1
        await message.answer(f"Обновил ваш текущий вес!",
                                reply_markup=await kb.basic())
        await database.user.save(user)
    except: 
        await message.answer(f"Пожалуйста, введите число как аргумент комманды",
                                reply_markup=await kb.basic())