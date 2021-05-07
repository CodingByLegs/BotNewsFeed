from datetime import datetime


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


if __name__ == '__main__':
    my_date = MyDataJSON("2021-05-03T22:50:11+00:00")
    print(my_date.date)