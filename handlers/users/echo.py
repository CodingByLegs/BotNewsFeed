from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from loader import bot




# # Эхо хендлер, куда летят текстовые сообщения без указанного состояния
# @dp.message_handler(state=None)
# async def bot_echo(message: types.Message):
#     await message.answer(f"Эхо без состояния."
#                          f"Сообщение:\n"
#                          f"{message.text}")
#
#
# # Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
# @dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
# async def echo(message: types.Message):
#     await bot.send_message(message.chat.id, message.text + "\n" + str(message.from_user.id) + "\n" + str(message.chat.id))

@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.chat.id, message.text + "\n" + str(message.from_user.id) + "\n" + str(message.chat.id))


