import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from asyncpg_lite import DatabaseManager
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from urllib.parse import urlparse

# .env in base directory
load_dotenv()

scheduler = AsyncIOScheduler(timezone='Europe/Bratislava')
admins = [int(admin_id) for admin_id in os.getenv('ADMINS').split(',')]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# postgre connection
parsed_url = urlparse(os.getenv("PG_LINK"))
port = parsed_url.port if parsed_url.port is not None else 5432

db_url = (
    f"postgresql://{parsed_url.username}:{parsed_url.password}"
    f"@{parsed_url.hostname}:{port}{parsed_url.path}"
)

db_manager = DatabaseManager(db_url=db_url, deletion_password=os.getenv('ROOT_PASS'))

bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())