from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

class keyboard:
    async def basic() -> ReplyKeyboardMarkup:
        Button1 = KeyboardButton(text="ℹ️ Информация о тренировках")
        Button2 = KeyboardButton(text="🏆 Мои награды")
        Button3 = KeyboardButton(text="🦾 Упражнение")
        Button4 = KeyboardButton(text="👤 Профиль")
        Button5 = KeyboardButton(text="❓ Комманды")
        
        
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[Button4],[Button2, Button3],[Button1, Button5]])
        return keyboard
    
    async def complete() -> InlineKeyboardMarkup:
        button1 = InlineKeyboardButton(text='✅ Выполнил', callback_data='COMPLETED')
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button1]])
        return keyboard
    
    async def again() -> InlineKeyboardMarkup:
        button1 = InlineKeyboardButton(text='✅ Да', callback_data='AGAIN')
        button2 = InlineKeyboardButton(text='❌ Нет', callback_data='NOT_AGAIN')
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button1, button2]])
        return keyboard
    
    async def next() -> InlineKeyboardMarkup:
        button1 = InlineKeyboardButton(text='🦿 Следующая', callback_data=(f'NEXT'))
        button2 = InlineKeyboardButton(text='❌ Закончить', callback_data=(f'STOP'))
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button1, button2]])
        return keyboard
    
    async def sex() -> InlineKeyboardMarkup:
        button1 = InlineKeyboardButton(text='💙 Парень', callback_data='Male')
        button2 = InlineKeyboardButton(text='💖 Девушка', callback_data='Female')
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button1, button2]])
        return keyboard
    
    async def acc_decl(id: int, p_id:int, msg) -> InlineKeyboardMarkup:
        button1 = InlineKeyboardButton(text='✅ Принять', callback_data=(f'ACCEPTED {id} {p_id} {msg.message_id} PARTNER'))
        button2 = InlineKeyboardButton(text='❌ Отклонить', callback_data=(f'DECLINE {id} {p_id} {msg.message_id} PARTNER'))
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button1, button2]])
        return keyboard
    
    async def pager(max_pages: int, curr_page: int) -> InlineKeyboardMarkup:
        buttons = []
        if curr_page > 1:
            buttons.append(InlineKeyboardButton(text=' ◀️ ', callback_data=(f'PAGE- {curr_page}')))
            buttons.append(InlineKeyboardButton(text=' ↩️ ', callback_data=(f'PAGE_START')))
        
        if curr_page == 1:
            buttons.append(InlineKeyboardButton(text='  ', callback_data=(f'FEED')))
            buttons.append(InlineKeyboardButton(text='  ', callback_data=(f'FEED')))
        
        if curr_page < max_pages:
            buttons.append(InlineKeyboardButton(text=' ▶️ ', callback_data=(f'PAGE+ {curr_page}')))
            
        if curr_page == max_pages:
            buttons.append(InlineKeyboardButton(text='  ', callback_data=(f'FEED')))
        
        return InlineKeyboardMarkup(inline_keyboard=[buttons])
        
        
    