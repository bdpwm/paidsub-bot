import asyncio
from create_bot import bot, dp, scheduler
from handlers.user_router import user_router


async def main():
    dp.include_router(user_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())