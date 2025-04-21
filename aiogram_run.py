import asyncio
from create_bot import bot, dp, scheduler, init_db
from handlers.user_router import user_router
from handlers.admin_router import admin_router
from utils.scheduler import start_scheduler

async def main():
    await init_db()


    start_scheduler()    
    dp.include_router(user_router)
    dp.include_router(admin_router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())