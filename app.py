from aiogram import executor

from database import Database

from loader import dp, scheduler
from binance_parser.parser_module import ParserModule
from binance_parser.statistic_module import process_daily_statistic, process_monthly_statistic
from bot.utils import on_startup_notify
from bot.utils import set_default_commands

from data.config import DB_URI


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)

    Database.on_startup(DB_URI)


if __name__ == '__main__':
    parser = ParserModule()

    scheduler.start()
    scheduler.add_job(parser.init_parsing, 'interval', seconds=60, misfire_grace_time=None)
    scheduler.add_job(process_daily_statistic, 'cron', hour=14, misfire_grace_time=None)
    scheduler.add_job(process_monthly_statistic, 'cron', day=1, hour=15, misfire_grace_time=None)

    executor.start_polling(dp, on_startup=on_startup)

