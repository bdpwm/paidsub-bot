from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from create_bot import admins


def main_kb(user_telegram_id: int):
    kb_list = [[KeyboardButton(text="My profile")]]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Menu"
    )


def profile_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="Check sub")],
        [KeyboardButton(text="Invite Friends")],
        [KeyboardButton(text="Pay subscription")],
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Profile Menu"
    )

def back_to_profile_kb(user_telegram_id: int):
    kb_list = [[KeyboardButton(text="Back to Menu")]]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Back to Profile Menu"
    )