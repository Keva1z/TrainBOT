from bot.keyboards.keyboards import keyboard as kb
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from database.manager import database
from aiogram import Router, types, F
from aiogram.filters import Command
from bot.console_log import logger


router = Router()


class Form(StatesGroup):
    plan_name = State()
    name = State()
    details = State()
    approaches = State()
    repeats = State()
    repeats_name = State()
    

@router.message(Command("cancel"))
@router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    logger.telegram.log_command(message.from_user.username, "/cancel")
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "Отменено.",
        reply_markup=await kb.basic(),
    )
   
@router.message(Command('excercise_add'))
async def excercise_add(message: types.Message, state: FSMContext):
    logger.telegram.log_command(message.from_user.username, "/excercise_add plan")
    await state.set_state(Form.plan_name)
    await message.answer(
        "<u>Введите название плана для которого создаете упражнение</u>\n\n<b>Напишите /cancel или cancel чтобы выйти из создания упражнения</b>",
        reply_markup=types.ReplyKeyboardRemove()
    )
    
@router.message(Form.plan_name)
async def excercise_name(message: types.Message, state: FSMContext):
    logger.telegram.log_command(message.from_user.username, "/excercise_add name")
    user_id = message.from_user.id
    user = await database.user.load(user_id)
    
    if message.text.lower() in user.plans:
        await state.update_data(plan_name=message.text.lower())
        await state.set_state(Form.name)
        await message.answer(
            "<u>Введите название упражнения</u>\n\n<b>Напишите /cancel или cancel чтобы выйти из создания упражнения</b>",
            reply_markup=types.ReplyKeyboardRemove(),
        )
    else:
        await message.answer(
            f"<u>Плана {message.text.lower()} не существует, введите ваш план для создания упражнения в нём (/all_plans): </u>\n\n<b>Напишите /cancel или cancel чтобы выйти из создания упражнения</b>",
            reply_markup=types.ReplyKeyboardRemove(),
        )
    
@router.message(Form.name)
async def details_plan(message: types.Message, state: FSMContext):
    logger.telegram.log_command(message.from_user.username, "/excercise_add details")
    await state.update_data(name=message.text)
    await state.set_state(Form.details)
    await message.answer(
        "<u>Введите описание упражнения</u>\n\n<b>Напишите /cancel или cancel чтобы выйти из создания упражнения</b>",
        reply_markup=types.ReplyKeyboardRemove()
    )
    
@router.message(Form.details)
async def approaches_plan(message: types.Message, state: FSMContext):
    logger.telegram.log_command(message.from_user.username, "/excercise_add approaches")
    
    await state.update_data(details=message.text)
    await state.set_state(Form.approaches)
    await message.answer(
        "<u>Введите количество подходов</u>\n\n<b>Напишите /cancel или cancel чтобы отменить создание упражнения</b>",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    
@router.message(Form.approaches)
async def repeats_plan(message: types.Message, state: FSMContext):
    logger.telegram.log_command(message.from_user.username, "/excercise_add repeats")
    
    try:
        int(message.text.lower())
    
        await state.update_data(approaches=message.text)
        await state.set_state(Form.repeats)
        await message.answer(
            "<u>Введите количество повторений (или секунд и т.п)\nПисать только число, выглядеть будет так: [кол-во повторений] [название повторений]</u>\n\n<b>Напишите /cancel или cancel чтобы отменить создание упражнения</b>",
            reply_markup=types.ReplyKeyboardRemove(),
        )
    except ValueError:
        await message.answer(
            "<u>Введите количество подходов ЧИСЛОМ (или секунд и т.п)</u>\n\n<b>Напишите /cancel или cancel чтобы отменить создание упражнения</b>",
            reply_markup=types.ReplyKeyboardRemove(),
        )
    
    
@router.message(Form.repeats)
async def repeats_name_plan(message: types.Message, state: FSMContext):
    logger.telegram.log_command(message.from_user.username, "/excercise_add repeats_name")
    try:
        int(message.text.lower())
        
        await state.update_data(repeats=message.text)
        await state.set_state(Form.repeats_name)
        await message.answer(
            "<u>Введите название повторений (разы, секунды и т.п)\nПисать только название, выглядеть будет так: [кол-во повторений] [название повторений]</u>\n\n<b>Напишите /cancel или cancel чтобы отменить создание упражнения</b>",
            reply_markup=types.ReplyKeyboardRemove(),
        )
    except ValueError:
        await message.answer(
            "<u>Введите количество повторений ЧИСЛОМ (разы, секунды и т.п)\nПисать только число, выглядеть будет так: [кол-во повторений] [название повторений]</u>\n\n<b>Напишите /cancel или cancel чтобы отменить создание упражнения</b>",
            reply_markup=types.ReplyKeyboardRemove(),
        )
    
@router.message(Form.repeats_name)
async def process_plan(message: types.Message, state: FSMContext):
    logger.telegram.log_command(message.from_user.username, "/excercise_add processing...")
    data = await state.update_data(repeats_name=message.text)
    await state.clear()
    await show_summary(message, data)
    
async def show_summary(message: types.Message, data) -> None:
    plan_name = data["plan_name"]
    name = data["name"]
    details = data["details"]
    approaches = data["approaches"]
    repeats = data["repeats"]
    repeats_name = data["repeats_name"]
    
    text = f"Добавил упражнение <b>[{name}]</b> в план <b>[{plan_name}]</b>\n/excercise_add - добавить еще упражнение\n/all_plans - все планы\n<code>/write_plan {plan_name}</code> - написать упражнения в плане"
    
    user_id = message.from_user.id
    
    user = await database.user.load(user_id)
    
    user.plans[plan_name][name] = {
        'details' : details,
        'approaches' : approaches,
        'repeats' : [repeats, repeats_name]
    }
    await database.user.save(user)
    
    await message.answer(text=text, reply_markup=await kb.basic())