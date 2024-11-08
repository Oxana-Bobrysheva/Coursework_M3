import pandas as pd
from pycodestyle import continued_indentation

from src.utils import get_cards, read_xlsx
from src.utils import greetings

def get_started_main():
    input_date = input("Введите дату в формате YYYY-MM-DD HH:MM:SS - ")
    file_path = "../data/operations.xlsx"
    cards_info = get_cards(file_path, input_date)
    json_answer = {"greeting": greetings(input_date)}

    return cards_info


if __name__ == "__main__":
    print(get_started_main())
# 2021-02-15 00:00:00