from aiogram.utils.callback_data import CallbackData

channel_callback = CallbackData("channel", "channel_name", "page")
delete_channel_callback = CallbackData("delete", "answer", "channel_name", "page")
action_callback = CallbackData("action", "action_name", "page")
special_action_callback = CallbackData("action", "action_name", "page", "name_of_channel")
page_callback = CallbackData("page", "page_number",
                             "rotation")  # ииспользуется для навигации по страницам с списком каналов новостной ленты
special_page_callback = CallbackData("page", "page_number", "rotation", "name_of_channel")
category_callback = CallbackData("category", "category_name")

