from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from create_bot import bot, channel_id, admins

admin_router = Router()

@admin_router.message(F.text.contains('Check channel'))
@admin_router.message(Command('admin_check_channel'))
async def check_channel_status(message: Message):
    if message.from_user.id not in admins: # make it later as middleware
        return
        
    try:
        chat = await bot.get_chat(channel_id)
        bot_member = await bot.get_chat_member(channel_id, bot.id)
        
        permissions_text = "Bot permissions:\n"
        if hasattr(bot_member, "can_invite_users"):
            permissions_text += f"- Can invite users: {bot_member.can_invite_users}\n"
        if hasattr(bot_member, "can_restrict_members"):
            permissions_text += f"- Can restrict members: {bot_member.can_restrict_members}\n"
        
        await message.answer(
            f"Channel info:\n"
            f"- Title: {chat.title}\n"
            f"- ID: {chat.id}\n"
            f"- Type: {chat.type}\n"
            f"- Bot status: {bot_member.status}\n"
            f"{permissions_text}"
        )
    except Exception as e:
        await message.answer(f"Error checking channel: {str(e)}")