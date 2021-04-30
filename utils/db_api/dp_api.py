from aiogram import types
from asyncpg import Connection, Record
from asyncpg.exceptions import UniqueViolationError

from loader import db


class DBComands:
    pool: Connection = db
    ADD_NEW_USER_TO_NEWS_FEED = "INSERT INTO news_feed(user_id) VALUES($1)"
    ADD_CHANNEL_TO_NEWS_FEED = "UPDATE news_feed SET news_channels = " \
                               "array_append(news_channels, $1) " \
                               "WHERE user_id = $2"
    REMOVE_CHANNEL_FROM_NEWS_FEED = "UPDATE news_feed SET news_channels = " \
                                    "array_remove(news_channels, $1) " \
                                    "WHERE user_id = $2 "
    GET_NEWS_CHANNELS = "SELECT news_channels FROM news_feed " \
                        "WHERE user_id = $1 "
    SET_NEWS_PERIOD = "UPDATE news_feed SET news_period = $1 " \
                      "WHERE user_id = $2 "
    GET_NEWS_PERIOD = "SELECT news_period FROM news_feed " \
                      "WHERE user_id = $1 "
    ADD_NEW_CATEGORY = "INSERT INTO custom_categories(user_id, category_name, is_custom) " \
                       "VALUES($1, $2, $3) "
    REMOVE_CATEGORY = "DELETE FROM custom_categories WHERE user_id = $1 and category_name = $2"
    ADD_CHANNEL_TO_CATEGORY = "UPDATE custom_categories SET category_channels = " \
                              "array_append(category_channels, $1) " \
                              "WHERE user_id = $2"
    REMOVE_CHANNEL_FROM_CATEGORY = "UPDATE custom_categories SET category_channels = " \
                                   "array_remove(category_channels, $1) " \
                                   "WHERE user_id = $2 "

    async def add_new_user(self):
        user = types.User.get_current()
        user_id = user.id
        command = self.ADD_NEW_USER_TO_NEWS_FEED
        try:
            await self.pool.fetchval(command, user_id)
        except UniqueViolationError:
            pass

    async def add_channel_to_news_feed(self, channel_name):
        user = types.User.get_current()
        user_id = user.id
        args = channel_name, user_id
        command = self.ADD_CHANNEL_TO_NEWS_FEED
        try:
            await self.pool.fetchval(command, *args)
        except UniqueViolationError:
            pass


db = DBComands()
