from bot.keyboards.keyboards import keyboard as kb
from aiogram.filters import Command
from bot.console_log import logger
from aiogram import Router
from aiogram import types

from database.manager import database
from bot.trainer import Trainer

router = Router()
bot = None

@router.message(Command('write_plan'))
async def write_plan(message: types.Message):
    logger.telegram.log_command(message.from_user.username, "/write_plan")
    
    user_id = message.from_user.id
    user = await database.user.load(user_id)
    
    args = message.text.lower().split(' ')
    name = ' '.join(args[1::])
    
    if name != '':
        if name in user.plans:
            text = '<b>Упражнения в плане:</b>\n----------------'
            id = 1
            for i in user.plans[name]:
                text += f'\n{id}) ' + i
                id += 1
        else:
            text = f'Плана "<b>{name}</b>" не существует'
    else:
        text = '<b>Вы не можете вывести план без названия!</b>'
    
    await message.reply(text)
    
@router.message(Command('create_plan'))
async def create_plan(message: types.Message):
    logger.telegram.log_command(message.from_user.username, "/create_plan")
    
    user_id = message.from_user.id
    user = await database.user.load(user_id)
    
    args = message.text.lower().split(' ')
    name = ' '.join(args[1::])
    if name != '':
        user.plans[name] = {}
        await database.user.save(user)
        await message.reply(f"""<b>Создал план тренировок [{name}]!</b>
    <code>/plan {name}</code> - установить план как план тренировок
    /all_plans - Чтобы посмотреть список планов
    /excercise_add - Добавить упражнение в план
    /delete_plan - Удалить план""")
    else:
        await message.reply(f"""<b>Вы не можете создать план без названия!</b>""")
        
@router.message(Command('all_plans'))
async def all_plans(message: types.Message, form:bool = False):
    logger.telegram.log_command(message.from_user.username, "/all_plans")
    
    user_id = message.from_user.id
    user = await database.user.load(user_id)
    
    text = 'Ваши планы: \n'
    if user.plans != {}:
        for i in user.plans:
            text += f'{i} - {len(user.plans[i])} упражнений\n'
    else:
        text = "У вас нет планов, создайте первый!\n/create_plan [название плана]"
    
    if form:
        await bot.send_message(text,
                        chat_id=message.chat.id)
    else:
        await message.answer(text)

@router.message(Command('delete_plan'))
async def delete_plan(message: types.Message):
    logger.telegram.log_command(message.from_user.username, "/delete_plan")
    
    user_id = message.from_user.id
    user = await database.user.load(user_id)
    
    args = message.text.lower().split(' ')
    name = ' '.join(args[1::])
    
    if name != '':
        if name in user.plans:
            user.plans.pop(name)
            await database.user.save(user)
        
            await message.reply(f"""<b>Удалил план тренировок <u>{name}</u>!</b>
    /all_plans - Чтобы посмотреть список планов
    /create_plan [название] - Чтобы создать план""")
        
        else:
            await message.reply(f"""<b>Плана <u>{name}</u> не существует!</b>
    /all_plans - Чтобы посмотреть список планов
    /create_plan [название] - Чтобы создать план""")
    else:
        await message.reply(f"""<b>Вы не можете удалить план без названия!</b>
    /all_plans - Чтобы посмотреть список планов
    /create_plan [название] - Чтобы создать план""")
        
@router.message(Command('plan'))
async def plan(message: types.Message):
    logger.telegram.log_command(message.from_user.username, "/plan")
    
    user_id = message.from_user.id
    user = await database.user.load(user_id)
    
    args = message.text.lower().split(' ')
    name = ' '.join(args[1::])
    if name != '':
        if user.current_plan != name:
            state, reason = await Trainer()._load_plan(name, user)
        else:
            state, reason = False, f"Тренировка <b>{name}</b> уже установлена!"
        if state:
                await message.answer(f"Поменял тренировку на план <b>{name}</b>",
                                reply_markup=await kb.basic())

        else:
            await message.answer(reason,
                                reply_markup=await kb.basic())
    else:
        await message.answer(f"Вы не можете выбрать тренировку без названия!",
                                reply_markup=await kb.basic())
        
@router.message(Command('excercise_remove'))
async def excercise_remove(message: types.Message):
    logger.telegram.log_command(message.from_user.username, "/excercise_remove")
    
    user_id = message.from_user.id
    user = await database.user.load(user_id)
    
    args = message.text.lower().split(' ')
    name = ' '.join(args[1:-1:])
    id = args[-1]
    
    if name in user.plans:
        try:
            id = int(id)-1
            if len(user.plans[name]) >= id:
                i = 0
                deleted = None
                for ex in user.plans[name]:
                    if i == id: user.plans.pop(ex); deleted = ex; break
                    i += 1
                
                await message.reply(f"""<b>Удалил упражнение <u>[{deleted}]</u> из плана <u>[{name}]</u></b>
        /all_plans - Чтобы посмотреть список планов
        <code>/excercise_add</code> - Чтобы создать упражнение""")
            
        except ValueError:
            await message.reply(f"""<b>Введите число в значение id!</b>
        <code>/excercise_remove {name} ID</code>""")
    else:
        await message.reply(f"""<b>Плана <u>{name}</u> не существует!</b>
        /all_plans - Чтобы посмотреть список планов
        <code>/create_plan </code> - Чтобы создать план""")
    
    # if name != '':
    #     if name in user.plans:
    #         user.plans[name].pop(ex)
    #         await database.user.save(user)
        
    #         await message.reply(f"""<b>Удалил план тренировок <u>{name}</u>!</b>
    # /all_plans - Чтобы посмотреть список планов
    # /create_plan [название] - Чтобы создать план""")
        
    #     else:
    #         await message.reply(f"""<b>Плана <u>{name}</u> не существует!</b>
    # /all_plans - Чтобы посмотреть список планов
    # /create_plan [название] - Чтобы создать план""")
    # else:
    #     await message.reply(f"""<b>Вы не можете удалить план без названия!</b>
    # /all_plans - Чтобы посмотреть список планов
    # /create_plan [название] - Чтобы создать план""")

# /excercise_add in bot.handlers.form_handler