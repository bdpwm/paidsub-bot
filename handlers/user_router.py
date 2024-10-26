import asyncio
from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.types import Message
from create_bot import bot, channel_id, bot_username
from db_handler.db import get_user_data
from keyboards.kbs import main_kb, profile_kb, back_to_profile_kb
from utils.utils import get_refer_id, get_now_time
from aiogram.utils.chat_action import ChatActionSender
from aiogram.methods import CreateChatInviteLink, BanChatMember, UnbanChatMember
from datetime import timedelta

user_router = Router()


@user_router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        user_info = await get_user_data(user_id=message.from_user.id)

    if user_info:
        response_text = f'{user_info.get("full_name")}, hello there!'
    else:
        refer_id = get_refer_id(command.args)
        await insert_user(user_data={
            'user_id': message.from_user.id,
            'full_name': message.from_user.full_name,
            'user_login': message.from_user.username,
            'refer_id': refer_id,
            'date_reg': get_now_time()
        })
        response_text = f'{user_info.get("full_name")}, Welcome to channel.'
        if refer_id:
            response_text = (f'{message.from_user.full_name},'
                             f'refered by - <b>{refer_id}</b>. {universe_text}')

    await message.answer(text=response_text, reply_markup=main_kb(message.from_user.id))


@user_router.message(Command('profile'))
@user_router.message(F.text.contains('My profile'))
@user_router.message(F.text.contains('Back to Menu'))
async def get_profile(message: Message):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        user_info = await get_user_data(user_id=message.from_user.id)
        text = (f"Welcome, {message.from_user.full_name}!")
    await message.answer(text, reply_markup=profile_kb(message.from_user.id))


@user_router.message(Command('pay'))
@user_router.message(F.text.contains('Pay subscription'))
async def pay_command(message: Message):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):

        # payment simulation
        await message.answer("Successfully received payment.")
        # payment simulation

        user_id = message.from_user.id
        await bot(UnbanChatMember(chat_id=channel_id, user_id=user_id))
        
        invite_link = await bot.create_chat_invite_link(
            chat_id=channel_id,
            name=f"Invite for {user_id}",
            expire_date=timedelta(minutes=5),
            member_limit=1,
            creates_join_request=False
        )

        await message.answer(f"Link to private channel: {invite_link.invite_link}\nYou have 5 minutes to activate link!")
        asyncio.create_task(remove_user_after_delay(user_id, 20))

    


# test function
async def remove_user_after_delay(user_id: int, delay: int):
    await asyncio.sleep(delay)
    await bot(BanChatMember(chat_id=channel_id, user_id=user_id, revoke_messages=True))
    print(f"{user_id} has been banned")
# delete


# inv friends handler
@user_router.message(Command('invite'))
@user_router.message(F.text.contains('Invite Friends'))
async def invite_command(message: Message):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        user_info = await get_user_data(user_id=message.from_user.id)
        text = (f'👉 Username: <code><b>{message.from_user.username}</b></code>\n'
                f'👉 Telegram ID: <code><b>{message.from_user.id}</b></code>\n'
                f'👥 Friends invited: <b>{user_info.get("count_refer")}</b>\n\n'
                f'🚀 Link to invite your friends: '
                f'<code>https://t.me/{bot_username}?start={message.from_user.id}</code>')
        await message.answer(text, reply_markup=back_to_profile_kb(message.from_user.id))

# check sub handler
