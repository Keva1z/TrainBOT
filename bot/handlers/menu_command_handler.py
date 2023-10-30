from aiogram import Router
from aiogram.filters import Command
from aiogram import types
from bot.console_log import logger
from bot.keyboards.keyboards import keyboard as kb
from bot.trainer import Trainer

from database.manager import database, User

router = Router()
bot = None

@router.message(Command('help'))
async def help(message, bot_msg: types.Message = None, page: int = 1):
    logger.telegram.log_command(message.from_user.username, "/help")
    page0 = f"""<b>---Как пользоваться списком команд---</b>
    
ℹ️ <u><b>Аргумент</b></u> - Значение пользователя которое <u>подставляется</u> вместо <b>[...]</b>
  Команды с аргументами копируются простым нажатием на текст    

Команды которые подсвечиваются <u>так:</u> /command
Являются командами <b>без аргументов</b>.
На такие команды можно <b>просто нажать</b> не вписывая ничего.

Команды которые подсвечиваются <u>так:</u> <code>/command [ARG1]</code>
Являются командами <b>с аргументами</b>

К примеру команда <code>/create_plan [название плана]</code>
Вводить ее нужно <u>так</u>: <code>/create_plan разминка</code>"""

    page1 = f"""<b>---Планы тренировок---</b>

- /all_plans - Показывает список всех ваших планов тренировок
- /excercise_add - Вызывает диалог создания упражнения для плана
- <code>/excercise_remove [название упражнения] [ID упражнения]</code> - Удаляет упражнение из плана
- <code>/create_plan [название плана]</code> - создает новый план тренировок
- <code>/write_plan [название плана]</code> - Выводит все названия упражнений в плане
- <code>/delete_plan [название плана]</code> - удаляет существующий план тренировок
- <code>/plan [название плана]</code> - Устанавливает план для тренировок"""

    page2 = f"""<b>---Профиль---</b>

- /set_sex - Смена пола в профиле
- /leave_partner - Выйти из партнёрства
- <code>/set_partner [ID партнера]</code> - Отправление заявки для совместного выполнения заданий
- <code>/set_weight [Киллограмы]</code> - Выставление текущего веса
- <code>/start_weight [Киллограмы]</code> - Выставление начального веса"""

    page3 = f"""<b>---Список наград---</b>

- /my_rewards - Список наград которые добавили вы (В режиме партнёра)
- <code>/use [ID Награды]</code> - использует награду если он у вас есть
- <code>/add_reward [Название награды]</code> - Добавляет награду за задания
- <code>/remove_reward [ID Награды]</code> - Удаляет награду
"""

    page4 = f"""<b>---Команды меню---</b>
    
- /profile - Открыть ваш профиль
- /help - Открыть данное меню
- /info - Информация о тренировках
- /rewards - Награды за выполнение тренировок
- /training - Начать тренировку
"""

    page5 = f"""<b>---Остальное---</b>

- /help - Вызыв данного текста с коммандами
- /cancel или просто cancel - работает только в создании упражнения в план"""

    pages = [page0, page1, page2, page3, page4, page5]
    
    text = f"""{pages[page-1]}
    
<b>Страница: {page}/{len(pages)}</b>
"""
    
    chatID = message.chat.id
    if bot_msg is not None: 
        msg_id = bot_msg.message_id
        await bot.edit_message_text(text = text,
                                chat_id= chatID,
                                message_id= msg_id,
                                reply_markup=await kb.pager(len(pages), page))
    else: 
        await bot.send_message(text = text, chat_id= chatID, reply_markup=await kb.pager(len(pages), page))

@router.message(Command('info'))
async def info(message,
                user: User.USER = None,
                bot_msg: types.Message = None):
    logger.telegram.log_command(message.from_user.username, "/info")
    
    if user is None: user = await database.user.load(message.from_user.id)
    
    text = f"""<b>{user.name}</b>, вот вся информация:

--------Тренировки--------

Упражнения выдаются в формате подходы и повторения. 
Повторения - то сколько вы делаете одно упражнение по кол-ву раз без отдыха
Подходы - То сколько раз вы выполняете повторения, между подходами перерыв 1-5 минут

--------Награды--------

Награды даются за выполнение 5 упражнений.
Награда выдается случайно из предложенного списка
Награда - способ поощерения себя или партнёра за выполнение заданий

------------------------

Данный бот создан для того чтобы было удобно
вести систему поощерений для тренировок, хранить
программы тренировок в одном месте и мотивировать
партнёра тренироваться благодаря наградам."""
    
    chatID = message.chat.id
    if bot_msg is not None: 
        msg_id = bot_msg.message_id
        await bot.edit_message_text(text = text,
                                chat_id= chatID,
                                message_id= msg_id)
    else: 
        await bot.send_message(text = text, chat_id= chatID)

@router.message(Command('profile'))
async def profile(message,
                 user: User.USER = None,
                bot_msg: types.Message = None):
    
    logger.telegram.log_command(message.from_user.username, "/profile")
    
    if user is None: user = await database.user.load(message.from_user.id)
    
    partner = await database.user.load(user.partner_id)
    partner_name = partner.name
    
    text = f""".
<b>   ---Персональные данные---</b>
    
<b>Имя</b> - <b>{user.name}</b>
<b>Пол</b> - <b>{user.sex}</b>
<b>ID</b> - <code>{user.userid}</code>

<b>   ---Данные о тренировках---</b>

<b>Выполнено тренировок за сегодня</b> - <b>{user.completed_today}</b>
<b>Тренировок до приза</b> - <b>{5 - user.completed}</b>
<b>Всего тренировочных планов</b> - <b>{len(user.plans)}</b>

<b>   ---Данные о весе---</b>

<b>Ваш текущий вес</b> - <u>{user.current_weight}kg</u> <b>(/set_weight KG)</b>
<b>Вес с которого начали</b> - <u>{user.start_weight}kg</u> <b>(/start_weight KG)</b>
<b>Вы сбросили</b> - <u>{user.start_weight - user.current_weight} kg</u>

<b>   ---Данные о партнере---</b>

<b>Партнер</b> - <a href="tg://user?id={user.partner_id}">{partner_name}</a>
"""
    if user.partner_id is not None:
        text += f"""
<b>Имя</b> - <b>{partner.name}</b>
<b>Пол</b> - <b>{partner.sex}</b>
<b>ID</b> - <code>{partner.userid}</code>

<b>Выполнено тренировок за сегодня</b> - <b>{partner.completed_today}</b>"""
    
    chatID = message.chat.id
    if bot_msg is not None: 
        msg_id = bot_msg.message_id
        await bot.edit_message_text(text = text,
                                chat_id= chatID,
                                message_id= msg_id)
    else: 
        await bot.send_message(text = text, chat_id= chatID)
        
@router.message(Command('rewards'))
async def rewards(message,
                 user: User.USER = None,
                bot_msg: types.Message = None):
    logger.telegram.log_command(message.from_user.username, '/rewards')
    
    if user is None: user = await database.user.load(message.from_user.id)
    
    text = f"<b>{user.name}</b>, вот ваши награды: \n"
    prizes = ""
    id = 1
    if user.partner_id is None:
        for unit in user.rewards:
            prizes += f"{id}) <b>{unit.name}</b> - <b>{unit.count}</b>\n"
            id += 1
    else:
        partner = await database.reward.load(user.partner_id)
        for unit in partner.rewards:
            prizes += f"{id}) <b>{unit.name}</b> - <b>{unit.count}</b>\n"
            id += 1
    text += prizes
    text += "\n\nЧтобы использовать награду напишите <code>/use [Номер награды]</code>"
    chatID = message.chat.id
    if bot_msg is not None: 
        msg_id = bot_msg.message_id
        await bot.edit_message_text(text = text,
                                chat_id= chatID,
                                message_id= msg_id)
    else: 
        await bot.send_message(text = text, chat_id= chatID)
        
@router.message(Command('training'))        
async def training(message,
                 user: User.USER = None,
                bot_msg: types.Message = None):
    
    chatID = message.chat.id
    if bot_msg is not None: 
        msg_id = bot_msg.message_id
    
    if user is None: user = await database.user.load(message.from_user.id)
    
    active = False
    
    logger.telegram.log_command(message.from_user.username, '/training')
    if user.current_plan:
        if len(user.plans[user.current_plan]) >= 5:
        
            if user.active:
                text = f"""У вас уже есть активная тренировка!"""
                keyboard = None
            else:
                ex = await Trainer().get_exercise(user)
                text = f"{ex}\n\nСовет: {await Trainer().get_tip()}"
                if ex is not None:
                    keyboard = await kb.complete()
                    active = True
                else:
                    text = "У вас больше нет заданий, хотите начать заного?"
                    keyboard = await kb.again()
    

        else:
            text = "В плане недостаточно заданий или их вовсе нет!\nНапишите /all_plans чтобы посмотреть какие планы у вас есть и сколько в них заданий"
            keyboard = None
    else:
            text = "У вас не выбран план.\nНапишите /all_plans чтобы посмотреть какие планы у вас есть"
            keyboard = None
    
    if user.active:
        if bot_msg is not None:
            await bot.delete_message(chat_id=chatID, message_id=msg_id)
        await bot.send_message(chat_id=chatID,
                               text=text,
                               reply_to_message_id=user.active_message)
    else:
        if bot_msg is not None:
            new_message = await bot.edit_message_text(text = text,
                                        chat_id= chatID,
                                        message_id= msg_id,
                                        reply_markup=keyboard)
        else:
            new_message = await bot.send_message(text = text, chat_id = chatID, reply_markup=keyboard)
        if active:
            user.active_message = new_message.message_id
            user.active = True
        
    await database.user.save(user)