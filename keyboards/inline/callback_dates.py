from aiogram.utils.callback_data import CallbackData

channel_callback = CallbackData("channel", "channel_name", "page")
channel_callback_with_category = CallbackData("channel", "channel_name", "category_name", "page")
delete_channel_callback = CallbackData("delete", "answer", "channel_name", "page")
special_delete_channel_callback = CallbackData("delete", "answer", "channel_name", "category_name", "page")
action_callback = CallbackData("action", "action_name", "page")
special_action_callback = CallbackData("action", "action_name", "page", "name_of_channel")
action_callback_with_category = CallbackData("action", "action_name", "page", "category_name")
page_callback = CallbackData("page", "page_number",
                             "rotation")  # ииспользуется для навигации по страницам с списком каналов новостной ленты
special_page_callback = CallbackData("page", "page_number", "rotation", "name_of_channel")
page_callback_with_category = CallbackData("page", "page_number", "rotation", "category_name")
category_callback = CallbackData("category", "category_name")
delete_category_callback = CallbackData("delete", "category_name")

