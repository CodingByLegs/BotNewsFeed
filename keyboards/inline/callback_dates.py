from aiogram.utils.callback_data import CallbackData

channel_callback = CallbackData("channel", "channel_name", "page_number")
page_callback = CallbackData("page", "page_number",
                             "rotation")  # ииспользуется для навигации по страницам с списком каналов новостной ленты
