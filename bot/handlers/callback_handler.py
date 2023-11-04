from aiogram import Router
from aiogram import types
from bot.keyboards.keyboards import keyboard as kb
from bot.handlers.menu_command_handler import training, help
from bot.trainer import Trainer
import random

from database.manager import database

router = Router()
bot = None

class b_msg():
    def __init__(self, id):
        self.message_id = id
        
        
@router.callback_query(lambda c: c.data)
async def handle_callback_query(call: types.CallbackQuery):
    data = call.data
    user_id = call.from_user.id
    user = await database.user.load(user_id)
    
    
    
    if "PAGE+" in data: 
        message = call.message
        page = int(data.split()[-1])
        await help(message, message, page=page+1)
        
    elif "PAGE-" in data:
        message = call.message
        page = int(data.split()[-1])
        await help(message, message, page=page-1)
    
    elif "PAGE_START" in data:
        message = call.message
        await help(message, message, page=1)
    
    if "ACCEPTED" in data:
        status, id, p_id, msg, a = data.split()
        id = int(id)
        p_id = int(p_id)
        msg_id = int(msg)
        
        if status == "ACCEPTED":
            await bot.delete_message(chat_id=id, message_id=msg_id+1)
            await bot.edit_message_text(text = "Вы приняли партнёра!",
                                chat_id=id,
                                message_id= msg_id)
            await bot.send_message(chat_id=p_id,
                                   text="Пользователь согласился стать вашим партнером",
                                   reply_markup=await kb.basic())
            user.partner_id = p_id
            partner = await database.user.load(p_id)
            partner.partner_id = id
            await database.user.save(user)
            await database.user.save(partner)
        else:
            await bot.send_message(chat_id=id,
                                   text="Пользователь отказался стать вашим партнером",
                                   reply_markup=await kb.basic())
    
    elif data == "NEXT":
        message = call.message
        
        await bot.delete_message(chat_id=message.chat.id,
                                 message_id=message.message_id)
        
        bot_msg = await message.answer("⏳ Получаю тренировку...")
        await training(message, user, bot_msg)
    
    elif data == "STOP":
        message = call.message
        
        text = "Заканчиваем сжигать жир, вы так и остались жп"
        
        await bot.edit_message_text(text = text,
                                chat_id=message.chat.id,
                                message_id= message.message_id)
        
    
    elif data == "COMPLETED":
        user.completed += 1
        user.completed_today += 1
        if user.completed % 5 == 0:
            if user.partner_id is None:
                if len(user.rewards) > 0:
                    prize_id = random.randint(0, len(user.rewards)-1)
                    user.rewards[prize_id].count += 1
                    text = f"Вы выполнили тренировку, молодец!\nВаш приз - <b>{user.rewards[prize_id].name}</b>"
                    user.completed = 0
                else:
                    text = f"Вы выполнили тренировку, молодец!\nНо у вас нету созданных наград, вы ничего не получили("
                    user.completed = 0
            else:
                partner = await database.user.load(user.partner_id)
                if len(partner.rewards) > 0:
                    prize_id = random.randint(0, len(partner.rewards)-1)
                    partner.rewards[prize_id].count += 1
                    text = f"Вы выполнили тренировку, молодец!\nВаш приз - <b>{partner.rewards[prize_id].name}</b>"
                    user.completed = 0
                else:
                   text = f"Вы выполнили тренировку, молодец!\nНо у вашего партнёра нету созданных наград, вы ничего не получили(" 
                await database.user.save(partner)
        else:
            text = f"""Вы выполнили тренировку, <b>умница!</b>
<b>Выполнено сегодня</b> - <u><b>{user.completed_today}</b></u>
<b>До следующего приза еще</b> - <u><b>{5 - user.completed} тренировок</b></u>"""
        user.active = False
        user.active_message = None
        await database.user.save(user)
        
        message = call.message

        await bot.edit_message_text(text = text,
                                chat_id=message.chat.id,
                                message_id= message.message_id,
                                reply_markup=await kb.next())
    elif data == "AGAIN":
        message = call.message
        
        text = "Хорошо, слушаюсь вас!"
        
        await bot.edit_message_text(text = text,
                                chat_id=message.chat.id,
                                message_id= message.message_id)
        
        await Trainer()._load_last_plan(user)
        bot_msg = await message.answer("⏳ Получаю тренировку...")
        await training(message, user, bot_msg)
        
    elif data == "NOT_AGAIN":
        message = call.message
        
        text = "Ну нет, так нет"
        
        await bot.edit_message_text(text = text,
                                chat_id=message.chat.id,
                                message_id= message.message_id)
    
    elif data == "Male":
        message = call.message
        
        text = "Поменял пол на мужской"
        
        user.sex = "MALE"
        await database.user.save(user)
        
        await bot.edit_message_text(text = text,
                                chat_id=message.chat.id,
                                message_id= message.message_id)
    
    elif data == "Female":
        message = call.message
        
        text = "Поменял пол на женский"
        
        user.sex = "FEMALE"
        await database.user.save(user)
        
        await bot.edit_message_text(text = text,
                                chat_id=message.chat.id,
                                message_id= message.message_id)
        
    await bot.answer_callback_query(callback_query_id=call.id)