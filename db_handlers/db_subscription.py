import logging
from datetime import date, timedelta
from create_bot import engine, AsyncSessionLocal, bot, channel_id
from sqlalchemy.sql import text
from datetime import date, timedelta
from aiogram.methods import BanChatMember


async def check_subscription(user_id: int):
    async with AsyncSessionLocal() as session:
        today = date.today()

        result = await session.execute(
            text(
                "SELECT subscription_end, bonus_days FROM users_reg "
                "WHERE user_id = :user_id AND subscription_status = true"
            ),
            {"user_id": user_id}
        )

        row = result.fetchone()
        if row:
            subscription_end, bonus_days = row
            if subscription_end < today:
                await session.execute(
                    text(
                        "UPDATE users_reg SET subscription_status = false "
                        "WHERE user_id = :user_id"
                    ),
                    {"user_id": user_id}
                )
                await session.commit()
                return False, None, bonus_days or 0
            return True, subscription_end, bonus_days or 0

        bonus_result = await session.execute(
            text("SELECT bonus_days FROM users_reg WHERE user_id = :user_id"),
            {"user_id": user_id}
        )
        bonus_days = bonus_result.scalar() or 0
        return False, None, bonus_days


async def subscription_update(user_id: int, days=30):
    async with AsyncSessionLocal() as session:
        today = date.today()
        
        result = await session.execute(
            text("SELECT bonus_days FROM users_reg WHERE user_id = :user_id"),
            {"user_id": user_id}
        )
        bonus_days = result.scalar() or 0
        
        subscription_end = today + timedelta(days=days + bonus_days)

        await session.execute(
            text(
                "UPDATE users_reg SET subscription_status = true, "
                "subscription_start = :today, "
                "subscription_end = :subscription_end, "
                "bonus_days = 0 "
                "WHERE user_id = :user_id"
            ),
            {
                "user_id": user_id,
                "today": today,
                "subscription_end": subscription_end
            }
        )
        await session.commit()


async def daily_check_subscriptions():
    async with AsyncSessionLocal() as session:
        today = date.today()

        query = text(
            "SELECT user_id FROM users_reg "
            "WHERE subscription_end < :today AND subscription_status = true"
        )

        result = await session.execute(query, {"today": today})
        expired_users = result.scalars().all()

        for user_id in expired_users:
            try:
                await bot(BanChatMember(chat_id=channel_id, user_id=user_id, revoke_messages=True))
                await bot.send_message(
                    chat_id=user_id, 
                    text="Your subscription has expired. Please renew it to continue accessing the channel."
                )
                await session.execute(
                    text("UPDATE users_reg SET subscription_status = false WHERE user_id = :user_id"),
                    {"user_id": user_id}
                )
            except Exception as e:
                logging.error(f"Error processing expired user {user_id}: {e}")
        
        await session.commit()