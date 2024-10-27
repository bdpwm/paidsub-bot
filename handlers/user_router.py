import asyncio
from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.types import Message
from create_bot import bot, channel_id, bot_username
from db_handlers.db_user import get_user_data, insert_user
from db_handlers.db_subscription import subscription_update, check_subscription
from keyboards.kbs import main_kb, profile_kb, back_to_profile_kb
from utils.utils import get_refer_id, get_now_time
from aiogram.utils.chat_action import ChatActionSender
from aiogram.methods import CreateChatInviteLink, BanChatMember, UnbanChatMember
from datetime import timedelta

user_router = Router()


@user_router.message(CommandStart())
async def start_handler(message: Message, command: CommandObject):
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
        response_text = (f'{message.from_user.full_name}, Welcome to bot.\n')
        if refer_id:
            response_text += (f'You was refered by - <b>{refer_id}</b>\n'
                              f'You will have 7 free days of subscription when you will purchase it.')

    await message.answer(text=response_text, reply_markup=main_kb(message.from_user.id))


@user_router.message(Command('profile'))
@user_router.message(F.text.contains('My profile'))
@user_router.message(F.text.contains('Back to Menu'))
async def get_profile_handler(message: Message):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        user_info = await get_user_data(user_id=message.from_user.id)
        text = (f"Welcome, {message.from_user.full_name}!")
    await message.answer(text, reply_markup=profile_kb(message.from_user.id))


@user_router.message(Command('pay'))
@user_router.message(F.text.contains('Pay subscription'))
async def pay_subscription_handler(message: Message):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):

        # payment simulation
        await message.answer("Successfully received payment.")
        # payment simulation

        user_id = message.from_user.id

        user_data = await get_user_data(user_id)
        refer_id = user_data.get("refer_id") if user_data else None

        if refer_id:
            await bot.send_message(
                chat_id=refer_id,
                text=f"🎉 Your referral {user_id} bought subscription!"
            )

        await bot(UnbanChatMember(chat_id=channel_id, user_id=user_id))
        
        invite_link = await bot.create_chat_invite_link(
            chat_id=channel_id,
            name=f"Invite for {user_id}",
            expire_date=timedelta(minutes=5),
            member_limit=1,
            creates_join_request=False
        )
        
        await subscription_update(user_id)
        await message.answer(f"Link to private channel: {invite_link.invite_link}\nYou have 5 minutes to activate link!")
        
    


@user_router.message(F.text.contains('Invite Friends'))
async def invite_friends_handler(message: Message):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        user_info = await get_user_data(user_id=message.from_user.id)
        text = (f'👉 Username: <code><b>{message.from_user.username}</b></code>\n'
                f'👉 Telegram ID: <code><b>{message.from_user.id}</b></code>\n'
                f'👥 Friends invited: <b>{user_info.get("count_refer")}</b>\n\n'
                f'💸 Referral invite balance: <code>{user_info.get("refer_balance")}</code>\n'
                f'🚀 Link to invite your friends: '
                f'<code>https://t.me/{bot_username}?start={message.from_user.id}</code>')
        await message.answer(text, reply_markup=back_to_profile_kb(message.from_user.id))


@user_router.message(F.text.contains('Check subscription'))
async def subscription_check_handler(message: Message):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        user_info = await get_user_data(user_id=message.from_user.id)
        subscription_active, subscription_end, subscription_bonus_days = await check_subscription(user_id=message.from_user.id)
        subscription_status = "Active" if subscription_active else "Inactive"
        
        if subscription_active and subscription_end:
            subscription_end_str = subscription_end.strftime("%Y-%m-%d")
        else:
            subscription_end_str = "N/A"
        
        text = (f'📅 Subscription Status: <b>{subscription_status}</b>\n'
                f'📅 Subscription End Date: <b>{subscription_end_str}</b>\n'
                f'📅 Subscription Bonus Days: <b>{subscription_bonus_days}</b>\n\n')
        
        await message.answer(text, reply_markup=back_to_profile_kb(message.from_user.id))