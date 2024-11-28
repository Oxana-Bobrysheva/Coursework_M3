import pandas as pd

from src.reports import expenses_by_category
from src.services import analyze_cashback_categories
from src.utils import read_xlsx
from src.views import get_started_main

if __name__ == "__main__":
    input_date = input("Введите дату в формате YYYY-MM-DD HH:MM:SS - ")
    print(get_started_main(input_date))

    operations = read_xlsx("../data/operations.xlsx")
    df = pd.DataFrame(operations)
    user_input = input("Enter a year and month with space")
    user_input = list(map(int, user_input.split()))
    print(analyze_cashback_categories(operations, user_input[0], user_input[1]))

    user_input = input("Enter a category and date in form YYYY-MM-DD")
    user_input = user_input.split()
    print(expenses_by_category(df, user_input[0], user_input[1]))
