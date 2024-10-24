from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('start test')

@start_router.message(Command('start_2'))
async def cmd_start_2(message: Message):
    await message.answer('start_2 test')

@start_router.message(F.text == '/start_3')
async def cmd_start_3(message: Message):
    await message.answer('start3 test')