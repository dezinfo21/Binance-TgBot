from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from data import config


bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

job_defaults = {
    'coalesce': False,
    'max_instances': 5
}

scheduler = AsyncIOScheduler(job_defaults=job_defaults, timezone='Europe/Budapest')
