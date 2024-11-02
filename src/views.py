import datetime
from typing import Tuple
import pandas as pd


def greetings(input_date: str) -> str:
    """Function <greetings> takes a string with date and time in form YYYY-MM-DD HH:MM:SS
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


def time_range(input_date: str) -> tuple[str, str]:
    """Function <time-range> takes a string with date and time in form YYYY-MM-DD HH:MM:SS
    and returns two parameters: start_time, end_time. It follows the rule: <end_time> is the date in the string
    and the <start_time> sets the day as the first day of the indicated month."""
    date_obj = datetime.datetime.strptime(input_date, "%Y-%m-%d %H:%M:%S")
    end_time = date_obj.strftime("%d.%m.%Y")
    new_date_obj = date_obj.replace (day=1)
    start_time = new_date_obj.strftime("%d.%m.%Y")

    return start_time, end_time


def reading_xlsx(file_path: str) -> list[dict]:
    """This function allows to read <operations.xlsx> and returns a list of
    dictionaries."""
    operations = []
    try:
        df = pd.read_excel(file_path)
        for index, row in df.iterrows():
            operations.append(row.to_dict())
    except FileNotFoundError:
        print(f"File {file_path} was not found.")
    except Exception as e:
        print(f"Error occurred: {e}.")
    return operations


def filter_by_time_range(operations: list) -> list:
    """Function"""



if __name__ == "__main__":
    print(greetings(input("Введите дату в формате YYYY-MM-DD HH:MM:SS - ")))
    print(time_range(input("Введите дату в формате YYYY-MM-DD HH:MM:SS - ")))
    print(reading_xlsx("../data/operations.xlsx"))