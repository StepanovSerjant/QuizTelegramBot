from aiogram.utils.executor import start_webhook

from data.config import WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_URL
from database.services import create_db
from handlers import dp
from loader import bot


async def on_startup(dp):
    """ Данный код исполняется после запуска """
    create_db()
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    """ Данный код исполняется перед падением """
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
