import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from db_handler.models import Base
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from urllib.parse import urlparse

# .env in base directory
load_dotenv()
scheduler = AsyncIOScheduler(timezone='Europe/Bratislava')
admins = [int(admin_id) for admin_id in os.getenv('ADMINS').split(',')]
channel_id = os.getenv('CHANNEL_ID')


# logging settings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# postgre connection
parsed_url = urlparse(os.getenv("PG_LINK"))
port = parsed_url.port if parsed_url.port is not None else 5432

db_url = (
    f"postgresql+asyncpg://{parsed_url.username}:{parsed_url.password}"
    f"@{parsed_url.hostname}:{port}{parsed_url.path}"
)

engine = create_async_engine(db_url, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())