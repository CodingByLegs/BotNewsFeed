from aiogram import types
from asyncpg import Connection
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
                              "WHERE user_id = $2 AND category_name = $3"
    REMOVE_CHANNEL_FROM_CATEGORY = "UPDATE custom_categories SET category_channels = " \
                                   "array_remove(category_channels, $1) " \
                                   "WHERE user_id = $2 AND category_name = $3 "
    GET_CATEGORY_CHANNELS = "SELECT category_channels FROM custom_categories " \
                            "WHERE user_id = $1 AND category_name = $2"
    GET_USER_CATEGORIES = "SELECT array_agg(category_name) FROM custom_categories " \
                          "WHERE user_id = $1"
    ADD_OUR_CATEGORY = "INSERT INTO our_categories(category_name, category_channels)" \
                       "VALUES($1,$2) "
    ADD_CHANNELS_TO_OUR_CATEGORY = "UPDATE our_categories SET category_channels = " \
                                   "array_cat(category_channels, $1) " \
                                   "WHERE category_name = $2"
    REMOVE_CHANNEL_FROM_OUR_CATEGORY = "UPDATE OUR_categories SET category_channels = " \
                                       "array_remove(category_channels, $1) " \
                                       "WHERE category_name = $2 "
    GET_OUR_CATEGORY_CHANNELS = "SELECT category_channels FROM our_categories " \
                                "WHERE category_name = $1"
    GET_OUR_CATEGORIES = "SELECT array_agg(category_name) FROM our_categories"
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

    async def remove_channel_from_news_feed(self, channel_name):
        user = types.User.get_current()
        user_id = user.id
        args = channel_name, user_id
        command = self.REMOVE_CHANNEL_FROM_NEWS_FEED
        try:
            await self.pool.fetchval(command, *args)
        except UniqueViolationError:
            pass

    async def get_news_channels(self):
        user = types.User.get_current()
        user_id = user.id
        command = self.GET_NEWS_CHANNELS
        return await self.pool.fetchval(command, user_id)

    async def set_news_period(self, news_period):
        user = types.User.get_current()
        user_id = user.id
        args = news_period, user_id
        command = self.SET_NEWS_PERIOD
        try:
            await self.pool.fetchval(command, *args)
        except UniqueViolationError:
            pass

    async def get_news_period(self):
        user = types.User.get_current()
        user_id = user.id
        command = self.GET_NEWS_PERIOD
        return await self.pool.fetchval(command, user_id)

    async def add_new_category(self, category_name, isCustom):
        user = types.User.get_current()
        user_id = user.id
        args = user_id, category_name, isCustom
        command = self.ADD_NEW_CATEGORY
        try:
            await self.pool.fetchval(command, *args)
        except UniqueViolationError:
            pass

    async def remove_category(self, category_name):
        user = types.User.get_current()
        user_id = user.id
        args = user_id, category_name
        command = self.REMOVE_CATEGORY
        try:
            await self.pool.fetchval(command, *args)
        except UniqueViolationError:
            pass

    async def add_channel_to_category(self, channel_name, category_name):
        user = types.User.get_current()
        user_id = user.id
        args = channel_name, user_id, category_name
        command = self.ADD_CHANNEL_TO_CATEGORY
        try:
            await self.pool.fetchval(command, *args)
        except UniqueViolationError:
            pass

    async def remove_channel_from_category(self, channel_name, category_name):
        user = types.User.get_current()
        user_id = user.id
        args = channel_name, user_id, category_name
        command = self.REMOVE_CHANNEL_FROM_CATEGORY
        try:
            await self.pool.fetchval(command, *args)
        except UniqueViolationError:
            pass

    async def get_category_channels(self, category_name):
        user = types.User.get_current()
        user_id = user.id
        args = user_id, category_name
        command = self.GET_CATEGORY_CHANNELS
        return await self.pool.fetchval(command, user_id, category_name)

    async def get_user_categories(self):
        user = types.User.get_current()
        user_id = user.id
        command = self.GET_USER_CATEGORIES
        return await self.pool.fetchval(command, user_id)

    async def add_our_category(self, category_name, category_channels):
        command = self.ADD_OUR_CATEGORY
        args = category_name, category_channels
        try:
            await self.pool.fetchval(command, *args)
        except UniqueViolationError:
            pass

    async def add_channels_to_our_category(self, category_channels, category_name):
        command = self.ADD_CHANNELS_TO_OUR_CATEGORY
        args = category_channels, category_name
        try:
            await self.pool.fetchval(command, *args)
        except UniqueViolationError:
            pass

    async def remove_channels_from_our_category(self, category_channels, category_name):
        command = self.REMOVE_CHANNEL_FROM_OUR_CATEGORY
        args = category_channels, category_name
        try:
            await self.pool.fetchval(command, *args)
        except UniqueViolationError:
            pass

    async def get_our_category_channels(self, category_name):
        command = self.GET_OUR_CATEGORY_CHANNELS
        return await self.pool.fetchval(command, category_name)

    async def get_our_categories(self):
        command = self.GET_OUR_CATEGORIES
        return await self.pool.fetchval(command)
db = DBComands()
