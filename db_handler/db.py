from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text
from create_bot import engine, AsyncSessionLocal
from sqlalchemy.exc import NoResultFound
from db_handler.models import User, create_table_users, Base

async def initialize_users_table():
    async with AsyncSessionLocal() as session:
        try:
            await session.execute(f"SELECT 1 FROM {User.__tablename__} LIMIT 1;")
        except NoResultFound:
            await create_table_users()


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