from aiogram import Router
from aiogram import types


router = Router()
bot = None

@router.errors()
async def pass_error(exeption: types.ErrorEvent) -> None:
    return None