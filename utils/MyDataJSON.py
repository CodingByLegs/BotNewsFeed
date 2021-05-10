from datetime import datetime, timedelta

import pytz


def from_int_time_to_str(hour_int, minute_int, second_int = None):
    if hour_int < 10:
        result = '0' + str(hour_int)
    else:
        result = str(hour_int)
    result += ':'
    if minute_int < 10:
        result += '0' + str(minute_int)
    else:
        result += str(minute_int)
    if second_int is not None:
        result += ':'
        if second_int < 10:
            result += '0' + str(second_int)
        else:
            result += str(second_int)
    return result


class MyDataJSON(object):
    def __init__(self, json_date: str):
        date = json_date.split('T')[0]
        time = json_date.split('T')[1]
        date = date.split('-')
        year = int(date[0])
        month = int(date[1])
        day = int(date[2])
        time_main = time.split('+')[0]
        time_tz = time.split('+')[1]
        time_main = time_main.split(':')
        time_tz = time_tz.split(':')
        hour = int(time_main[0])
        minute = int(time_main[1])
        second = int(time_main[2])
        time_tz_hour = int(time_tz[0])
        time_tz_minute = int(time_tz[1])
        if minute + time_tz_minute > 59:
            minute = minute + time_tz_minute - 60
            hour += 1
            if hour + time_tz_hour > 23:
                hour = hour + time_tz_hour - 24
                day += 1  # на этом и остановимся)
        self.date = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
