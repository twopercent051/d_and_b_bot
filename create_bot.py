import logging
import os

import redis
import betterlogging as bl

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tgbot.config import load_config
from tgbot.middlewares.config import ConfigMiddleware
# from tgbot.misc.google_sheets import GoogleSheets

config = load_config(".env")
r = redis.Redis(host=config.rds.host, port=config.rds.port, db=config.rds.db)
storage = RedisStorage(redis=r) if config.tg_bot.use_redis else MemoryStorage()
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

DATABASE_URL = f'postgresql+asyncpg://{config.db.user}:{config.db.password}@{config.db.host}:5432/{config.db.database}'
dp = Dispatcher()
scheduler = AsyncIOScheduler()

logger = logging.getLogger(__name__)
log_level = logging.INFO
bl.basic_colorized_config(level=log_level)

admin_group = config.misc.admin_group

# google_sheet = GoogleSheets()

secret_file = os.path.join(os.getcwd(), config.google.secret_file)
spreadsheet_id = config.google.spreadsheet_id
sheet_name = config.google.sheet_name


def register_global_middlewares(dp: Dispatcher, config):
    dp.message.outer_middleware(ConfigMiddleware(config))
    dp.callback_query.outer_middleware(ConfigMiddleware(config))
