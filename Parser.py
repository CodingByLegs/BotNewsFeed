
import json
from datetime import datetime

import pytz
from telethon.tl.functions.messages import GetHistoryRequest
from datetime import timedelta

from loader import client
from utils.db_api.dp_api import db

# Присваиваем значения внутренним переменным



async def dump_all_messages(channel):
    """Записывает json-файл с информацией о всех сообщениях канала/чата"""
    offset_msg = 0  # номер записи, с которой начинается считывание
    limit_msg = 100  # максимальное число записей, передаваемых за один раз
    all_messages = []  # список всех сообщений
    total_messages = 0
    total_count_limit = 1  # поменяйте это значение, если вам нужны не все сообщения
    timzone = pytz.timezone('Europe/Moscow')
    #period = timedelta(minutes=db.get_news_period())
    period = timedelta(minutes=1440*4)
    date_period: datetime = datetime.now(tz=timzone) - period
    print(date_period)
    messages = client.iter_messages(entity=channel, limit=1, offset_date=date_period)
    async for message in messages:
        last_msg_id = message.id
        print(message.text)
    print(last_msg_id)
    messages = client.iter_messages(entity=channel, limit=100, min_id=last_msg_id)
    last_msg_id += 1  # тк сообщения с last_nsg_id не будет парситься
    all_messages = []

    class DateTimeEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, datetime):
                return o.isoformat()
            if isinstance(o, bytes):
                return list(o)
            return json.JSONEncoder.default(self, o)

    async for message in messages:
        if message.text != "":
            if message.id != last_msg_id:
                is_current = 'false'
            else:
                is_current = 'true'
            new_message = {'message': message.text,
                           'date': message.date,
                           'message_id': message.id,
                           'current': is_current}
            all_messages.append(new_message)
    with open('channel_messages.json', 'w', encoding='utf8') as outfile:
        json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder, indent=4)
    #
    #
    # while True:
    #     history = await client(GetHistoryRequest(
    #         peer=channel,
    #         offset_id=offset_msg,
    #         offset_date=None, add_offset=0,
    #         limit=limit_msg, max_id=0, min_id=0,
    #         hash=0))
    #     if not history.messages:
    #         break
    #     messages = history.messages
    #     for message in messages:
    #         #if message.text is not "":
    #         all_messages.append(message.to_dict())
    #     offset_msg = messages[len(messages) - 1].id
    #     total_messages = len(all_messages)
    #     if total_count_limit != 0 and total_messages >= total_count_limit:
    #         break
    #
    # with open('channel_messages.json', 'w', encoding='utf8') as outfile:
    #     json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder,indent = 4)


async def parseURL(url):
    channel = await client.get_entity(url)
    await dump_all_messages(channel)
