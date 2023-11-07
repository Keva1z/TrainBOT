from bot.keyboards.keyboards import keyboard as kb
from aiogram.filters import Command
from bot.console_log import logger
from aiogram import Router
from aiogram import types

from database.manager import database, Unit

router = Router()
bot = None

@router.message(Command('use'))
async def use(message: types.Message):
    logger.telegram.log_command(message.from_user.username, "/use")
    
    user_id = message.from_user.id
    user = await database.user.load(user_id)
    
    command = message.text.split(' ')
    arg1 = command[-1]
    try: arg1 = int(arg1)
    except ValueError:
        await message.answer("Введите число как аргумент комманды!",
                                reply_markup=await kb.basic())
        return False
    if user.partner_id is None:
        if arg1 in range(1, len(user.rewards)+1):
            if user.rewards[arg1-1].count > 0:
                text_for_me = f"""Вы использовали <b>'{user.rewards[arg1-1].name}'</b> выполните для себя это!"""
                await message.answer(text_for_me,
                                parse_mode="HTML",
                                reply_markup=await kb.basic())
                user.rewards[arg1-1].count -= 1
                await database.user.save(user)
            else:
                await message.answer(f"У вас нет наград с ID {arg1}, проверьте, может быть их количество 0?",
                                reply_markup=await kb.basic())
        else:
            await message.answer(f"Награды с номером {arg1} не существует",
                                reply_markup=await kb.basic())
            
    else:
        partner = await database.user.load(user.partner_id)
        abbr = 'а' if partner.sex == 'FEMALE' else ''
        if arg1 in range(1, len(partner.rewards)+1):
            if partner.rewards[arg1-1].count > 0:
                chat_id = user.partner_id
                text_for_me = f"""{user.name} использовал{abbr} <b>'{partner.rewards[arg1-1].name}'</b> немедленно выполнять!"""
                await bot.send_message(chat_id, "<b>===== ALERT =====</b>")
                await bot.send_message(chat_id, text_for_me)
                await bot.send_message(chat_id, text_for_me)
                await bot.send_message(chat_id, text_for_me)
                await bot.send_message(chat_id, "<b>===== ALERT =====</b>")
                await message.answer(f'Отправил уведомление {partner.name}!',
                                reply_markup=await kb.basic())
                partner.rewards[arg1-1].count -= 1
                await database.user.save(partner)
            else:
                await message.answer(f"У вас нет наград с ID {arg1}, проверьте, может быть их количество 0?",
                                reply_markup=await kb.basic())
        else:
            await message.answer(f"Награды с номером {arg1} не существует",
                                reply_markup=await kb.basic())
            
@router.message(Command('my_rewards'))
async def my_rewards(message: types.Message):
    logger.telegram.log_command(message.from_user.username, "/my_rewards")
    
    user_id = message.from_user.id
    user = await database.user.load(user_id)
    
    text = f"<b>{user.name}</b>, вот награды созданные вами: \n"
    prizes = ""
    id = 1
    for prize in user.rewards:
        prizes += f"{id}) <b>{prize.name}</b> - <b>{prize.count}</b>\n"
        id += 1
    text += prizes
    await message.answer(text = text)
    
@router.message(Command('remove_reward'))
async def remove_reward(message: types.Message):
    logger.telegram.log_command(message.from_user.username, "/remove_reward")
    
    
    user_id = message.from_user.id
    user = await database.user.load(user_id)
    
    args = message.text.split(' ')
    if len(args) > 1:
        try:
            arg1 = int(args[1])
            if arg1 in range(1, len(user.rewards)+1):
                prize = user.rewards.pop(arg1-1)
                await database.user.save(user)
                
                await message.answer(f"Удалил награду '{prize.name}'",
                                    reply_markup=await kb.basic())

            else:
                await message.answer(f"Награды с номером {arg1} не существует",
                                    reply_markup=await kb.basic())
        except ValueError:
            await message.answer(f"Введите <u>число</u> как аргумент команды",
                                reply_markup=await kb.basic())

@router.message(Command('add_reward'))
async def add_reward(message: types.Message):
    logger.telegram.log_command(message.from_user.username, "/add_reward")
    
    user_id = message.from_user.id
    reward_list = await database.reward.load(user_id)
    
    args = message.text.lower().split(' ')
    name = ' '.join(args[1::])
    if name != '':
        await database.reward.add(name, reward_list)
        await message.reply(f"""<b>Добавил в список наград [{name}]!</b>""")
    else:
        await message.reply(f"""<b>Вы не можете создать награду без названия!</b>""")