import datetime


def greetings(input_date: str) -> str:
    """Function greetings takes a string with date and time in form YYYY-MM-DD HH:MM:SS
    and returns the string with four different greetings depending on the time"""
    date_obj = datetime.datetime.strptime(input_date, "%Y-%m-%d %H:%M:%S")
    if 0 <= date_obj.hour < 6:
        return "Доброй ночи"
    elif 6 <= date_obj.hour < 12:
        return "Доброе утро"
    elif 12 <= date_obj.hour < 18:
        return "Добрый день"
    else:
        return "Добрый вечер"


if __name__ == "__main__":
    print(greetings(input("Введите дату в формате YYYY-MM-DD HH:MM:SS - ")))