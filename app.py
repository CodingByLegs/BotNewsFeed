from aiogram import executor

from loader import dp
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify


async def on_startup(dispatcher):
    # Уведомляет про запуск
    # await on_startup_notify(dispatcher)
    pass


async def on_shutdown(dp):
    print("down")
    await dp.storage.close()
    await dp.storage.wait_closed()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
