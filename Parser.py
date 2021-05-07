import math
import os
import json
from datetime import datetime

import pytz
from aiogram import types
from telethon.tl.functions.messages import GetHistoryRequest
from datetime import timedelta

from loader import client
from utils.MyBool import MyBool
from utils.MyDataJSON import MyDataJSON
from utils.db_api.dp_api import db

# Присваиваем значения внутренним переменным



async def dump_all_messages(channel):
    """Записывает json-файл с информацией о всех сообщениях канала/чата"""
    will_parse_flag = True
    timzone = pytz.timezone('Europe/Moscow')
    # тк datetime.now() возвращает еще и микросекунды, а в json файле их нет, приходится делать так
    date_now = datetime(year=datetime.now(tz=timzone).year, month=datetime.now(tz=timzone).month,
                        day=datetime.now(tz=timzone).day, hour=datetime.now(tz=timzone).hour,
                        minute=datetime.now(tz=timzone).minute, second=datetime.now(tz=timzone).second)
    user = types.User.get_current()
    user_id = user.id
    if channel.startswith("https://t.me/"):
        channel_name = channel.partition("https://t.me/")[2]
    elif channel.startswith("t.me/"):
        channel_name = channel.partition("t.me/")[2]
    # создаем директорию для поиска json файлов пользователя
    path_json_user_channels = f'''jsonfiles/{user_id}'''
    # получаем список файлов этой директории
    list_of_user_channels: list = os.listdir(path_json_user_channels)
    # создаем путь к каналу, которой будем парсить
    path_channel_name = f'''channel_messages_{channel_name}.json'''
    # объединяем в общий путь к файлу с названием канала
    path_to_json_file = path_json_user_channels + '/' + path_channel_name
    # ищем файл с названием канала в директории path_json_user_channels
    if list_of_user_channels.count(path_channel_name):
        will_parse_flag = False
        barrier_to_reparse_channel_count_messages = 4  # минимальное кол-во сообщений, чтобы репарсить канал
        # минимальное вреям самой актуальной новости в файле (в минутах)
        barrier_to_reparse_channel_last_news_time = timedelta(minutes=30)
        with open(path_to_json_file, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
            json_data_length = len(json_data)
            if json_data_length != 0:
                # если сообщений до конца файла меньше, чем барьер, то поднимаем флаг на репарсинг
                if json_data_length < barrier_to_reparse_channel_count_messages:
                    will_parse_flag = True
                last_news_date = MyDataJSON(json_data[0]['date'])  # подхватываем дату последней новости из json файла
                date_different = date_now - last_news_date.date  # находим разницу по времени
                if date_different < barrier_to_reparse_channel_last_news_time:
                    will_parse_flag = True
            else:
                will_parse_flag = True

    if will_parse_flag:
        limit_msg = 50  # максимальное число записей, передаваемых за один раз
        all_messages = []  # список всех сообщений

        #period = timedelta(minutes=db.get_news_period())
        period = timedelta(hours=24)
        date_period: datetime = datetime.now(tz=timzone) - period
        print(date_period)
        messages = client.iter_messages(entity=channel, limit=1, offset_date=date_period)
        async for message in messages:
            last_msg_id = message.id
            print(message.text)
        print(last_msg_id)
        messages = client.iter_messages(entity=channel, limit=limit_msg, min_id=last_msg_id)
        last_msg_id += 1  # тк сообщения с last_nsg_id не будет парситься

        class DateTimeEncoder(json.JSONEncoder):
            def default(self, o):
                if isinstance(o, datetime):
                    return o.isoformat()
                if isinstance(o, bytes):
                    return list(o)
                return json.JSONEncoder.default(self, o)

        flag = False
        async for message in messages:
            if message.text != "":
                if not flag:  # плднимаем флаг для первого подходящего сообщения и делаем его "текущим последним"
                    current_last_message = message
                    is_current = True
                    flag = True
                else:  # если нашли еще одно сообщение
                    is_current = False  # делаем его не последним
                    new_message = {'message': current_last_message.text,
                                   'date': current_last_message.date,
                                   'message_id': current_last_message.id,
                                   'current': is_current}
                    all_messages.append(new_message)  # и добавляем в all_messages
                    current_last_message = message  # новое пришедшее сообщение делаем текущим
                    is_current = True
        # после выхода из цикла добавляем последнее сообщение, которе явялется текущим (is_current = True)
        if flag:  # если новости - только картинки, то сюда не зайдем
            new_message = {'message': current_last_message.text,
                           'date': current_last_message.date,
                           'message_id': current_last_message.id,
                           'current': is_current}
            all_messages.append(new_message)
        # создание директории и запись json файла
        with open(path_to_json_file, 'w', encoding='utf8') as outfile:
            json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder, indent=4)


async def dump_news_feed():
    user = types.User.get_current()
    all_news: list = []
    user_id = user.id
    channels: list = await db.get_news_channels()
    count_of_channels = len(channels)
    dot_json_str = '.json'
    path_to_user_directory = f'''jsonfiles/{user_id}/channel_messages_'''
    news_per_dump = 20  # кол-во сообщений для единоразовго отображения
    news_from_one_channel = math.trunc(news_per_dump / count_of_channels)  # округляем вниз
    lost_news = news_per_dump % news_from_one_channel  # если кол-во каналов пользователя не кратно 20 + защита,
    # если число каналов пользователя >20
    for channel in channels:
        link_channel_to_parse = "https://t.me/" + channel
        await dump_all_messages(link_channel_to_parse)  # репариснг канала перед выводом
        current_path = path_to_user_directory + channel + dot_json_str
        with open(current_path, 'r', encoding='utf-8') as json_file:
            json_data: list = json.load(json_file)
            json_data_length = len(json_data)
            i = json_data_length - 1
            message_read = 0
            # читаем сообщения из файла пока не прочитаем news_from_one_channel раз либо, пока не дойдем до конца файла
            while i > -1 and json_data_length - 1 - i != news_from_one_channel:
                message_read += 1
                i -= 1
                news = dict(message=json_data[i]['message'],
                            date=json_data[i]['date'])
                all_news.append(news)
                json_data.pop()  # удаляем последний элемент списка, тот, который только что добавили
            if message_read == news_from_one_channel:  # если прочитали все сообщения, то проверяем
                if lost_news and len(json_data):  # если есть "потерянные" сообщения и в текущем файле еще есть
                    # сообщения, если есть, то берем одно и добираем в итоговый список
                    news = dict(message=json_data[i]['message'],
                                date=json_data[i]['date'])
                    all_news.append(news)
                    json_data.pop()
                    lost_news -= 1
            else:
                lost_news += news_from_one_channel - message_read  # если из текущего канала были считаны все нововсти
                # но их кол-во <news_from_one_channel, то пропущенные сообщения добавим к lost_news
        with open(current_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)   # обновляем json файл после изъятия новостей
    all_news.append(dict(lost_news=lost_news))  # записываем в конец списка словарь со сзначением кол-ва
    # пропущенных новостей
    return all_news


async def parseURL(url):
    channel = await client.get_entity(url)
    await dump_all_messages(channel)
