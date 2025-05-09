from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text
from create_bot import engine, AsyncSessionLocal, bonus_days, subscription_cost, subscription_percent
from sqlalchemy.exc import NoResultFound
from db_handlers.models import User, Base
from datetime import date, timedelta


async def insert_user(user_data: dict):
    user_data.setdefault('count_refer', 0)

    async with AsyncSessionLocal() as session:
        async with session.begin():
            stmt = text("""
                INSERT INTO users_reg (user_id, full_name, user_login, refer_id, count_refer, date_reg)
                VALUES (:user_id, :full_name, :user_login, :refer_id, :count_refer, :date_reg)
                ON CONFLICT (user_id) DO UPDATE
                SET full_name = EXCLUDED.full_name,
                    user_login = EXCLUDED.user_login,
                    refer_id = EXCLUDED.refer_id,
                    count_refer = EXCLUDED.count_refer,
                    date_reg = EXCLUDED.date_reg
            """)
            await session.execute(stmt, user_data)

            if user_data.get('refer_id'):
                refer_stmt = text("""
                    UPDATE users_reg
                    SET count_refer = count_refer + 1
                    WHERE user_id = :refer_id
                """)
                await session.execute(refer_stmt, {"refer_id": user_data['refer_id']})

                user_data['bonus_days'] = bonus_days
                bonus_stmt = text("""
                    UPDATE users_reg
                    SET bonus_days = :bonus_days
                    WHERE user_id = :user_id
                """)
                await session.execute(bonus_stmt, user_data)
 
                refer_bonus = int(subscription_cost * subscription_percent)
                refer_bonus_stmt = text("""
                    UPDATE users_reg
                    SET refer_balance = refer_balance + :refer_bonus
                    WHERE user_id = :refer_id
                """)
                await session.execute(refer_bonus_stmt, {"refer_id": user_data['refer_id'], "refer_bonus": refer_bonus})


async def get_user_data(user_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            text("SELECT * FROM users_reg WHERE user_id = :user_id"),
            {"user_id": user_id}
        )
        user_data = result.fetchone()
        
        if user_data:
            columns = result.keys()
            return dict(zip(columns, user_data))
    return None


async def get_all_users(count=False):
    async with AsyncSessionLocal() as session:
        if count:
            result = await session.execute(text("SELECT COUNT(*) FROM users_reg"))
            return result.scalar()
        else:
            result = await session.execute(text("SELECT * FROM users_reg"))
            return [dict(row) for row in result.fetchall()]