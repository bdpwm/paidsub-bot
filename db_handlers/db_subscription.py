from datetime import date, timedelta
from create_bot import engine, AsyncSessionLocal
from sqlalchemy.sql import text
from datetime import date, timedelta


async def check_subscription(user_id: int):
    async with AsyncSessionLocal() as session:
        today = date.today()

        result = await session.execute(
            text(
                "SELECT subscription_end FROM users_reg "
                "WHERE user_id = :user_id AND subscription_status = true"
            ),
            {"user_id": user_id}
        )

        subscription_end = result.scalar_one_or_none()

        if subscription_end:
            if subscription_end < today:
                await session.execute(
                    text(
                        "UPDATE users_reg SET subscription_status = false "
                        "WHERE user_id = :user_id"
                    ),
                    {"user_id": user_id}
                )
                await session.commit()
                return False, None, bonus_days
            return True, subscription_end, bonus_days

        return False, None, 0


async def subscription_update(user_id: int, days=30):
    async with AsyncSessionLocal() as session:
        today = date.today()
        subscription_end = today + timedelta(days=days)

        await session.execute(
            text(
                "UPDATE users_reg SET subscription_status = true, "
                "subscription_start = :today, "
                "subscription_end = :subscription_end "
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
            await bot(BanChatMember(chat_id=channel_id, user_id=user_id, revoke_messages=True))
            await bot.send_message(chat_id=user_id, text=message)