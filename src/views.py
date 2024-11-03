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


def read_xlsx(file_path: str) -> list[dict]:
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


def filter_by_time_range(operations: list, input_date: str) -> list:
    """Function <filter_by_time_range> takes list of operations and returns a new list of operations
    filtered by time range"""
    filtered_operations = []
    start_time, end_time = time_range(input_date)
    start_time_obj = datetime.datetime.strptime(start_time, "%d.%m.%Y")
    end_time_obj = datetime.datetime.strptime(end_time, "%d.%m.%Y")
    for operation in operations:
        if isinstance(operation["Дата платежа"], str) and start_time_obj <= datetime.datetime.strptime(operation["Дата платежа"], "%d.%m.%Y") <= end_time_obj:
            filtered_operations.append(operation)

    return filtered_operations



if __name__ == "__main__":
    # print(greetings(input("Введите дату в формате YYYY-MM-DD HH:MM:SS - ")))
    # print(time_range(input("Введите дату в формате YYYY-MM-DD HH:MM:SS - ")))
    # print(read_xlsx("../data/operations.xlsx"))
    print(filter_by_time_range(read_xlsx("../data/operations.xlsx"), input("Введите дату в формате YYYY-MM-DD HH:MM:SS - ")))
    print(len(filter_by_time_range(read_xlsx("../data/operations.xlsx"), input("Введите дату в формате YYYY-MM-DD HH:MM:SS - "))))
# 2021-02-15 00:00:00