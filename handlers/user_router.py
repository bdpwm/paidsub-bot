from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.types import Message
from create_bot import bot
from keyboards.kbs import main_kb
from db_handler.db import get_user_data, insert_user, initialize_users_table
from utils.utils import get_refer_id, get_now_time
from aiogram.utils.chat_action import ChatActionSender

user_router = Router()


@user_router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject):
    # await initialize_users_table()

    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        user_info = await get_user_data(user_id=message.from_user.id)

    if user_info:
        response_text = f'{user_info.get("full_name")}, You already in channel.'
    else:
        refer_id = get_refer_id(command.args)
        await insert_user(user_data={
            'user_id': message.from_user.id,
            'full_name': message.from_user.full_name,
            'user_login': message.from_user.username,
            'refer_id': refer_id,
            'date_reg': get_now_time()
        })
        if refer_id:
            response_text = (f'{message.from_user.full_name},'
                             f'refered by - <b>{refer_id}</b>. {universe_text}')

    await message.answer(text=response_text, reply_markup=main_kb(message.from_user.id))


@user_router.message(Command('profile'))
@user_router.message(F.text.contains('My profile'))
async def get_profile(message: Message):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        user_info = await get_user_data(user_id=message.from_user.id)
        text = (f'👉 Telegram ID: <code><b>{message.from_user.id}</b></code>\n'
                f'👥 Friends invited: <b>{user_info.get("count_refer")}</b>\n\n'
                f'🚀 Link to invite your friends: '
                f'<code>https://t.me/easy_refer_bot?start={message.from_user.id}</code>')
    await message.answer(text, reply_markup=main_kb(message.from_user.id))