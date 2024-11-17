import datetime
import numpy as np
import pandas as pd
import json
import requests
from dotenv import load_dotenv
import os

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
        if (isinstance(operation["Дата платежа"], str) and start_time_obj <=
            datetime.datetime.strptime(operation["Дата платежа"], "%d.%m.%Y") <= end_time_obj):
            filtered_operations.append(operation)

    return filtered_operations


def get_unique_cards(filtered_transactions):
    cards_info: list = []
    if filtered_transactions:
        for transaction in filtered_transactions:
            card_number = transaction["Номер карты"]
            if card_number and pd.notna(card_number):
                cards_info.append(card_number)
    unique_cards = set(cards_info)
    return list(unique_cards)


def get_list_of_cards_info(cards_info: list, filtered_transactions: list) -> list[dict]:
    list_of_cards_info = []

    for card in cards_info:
        last_digits = card[-4:]
        total_spent = 0
        cashback = 0

        for transaction in filtered_transactions:
            if transaction["Номер карты"] == card:
                total_spent += transaction['Сумма платежа']
                # Получаем значение кэшбэка, если оно nan, добавляем 0
                cashback_value = transaction.get("Кэшбэк", 0)
                if isinstance(cashback_value, (int, float)) and not np.isnan(cashback_value):
                    cashback += cashback_value
        total_spent = round(total_spent, 2)
        list_of_cards_info.append({
            "last_digits": last_digits,
            "total_spent": total_spent,
            "cashback": cashback
        })

    return list_of_cards_info


def get_top_transactions(filtered_transactions):
    top_transactions = []
    sorted_filtered_transactions = sorted(filtered_transactions, key=lambda x: x["Сумма платежа"])
    i = 0
    for i, transaction in enumerate(sorted_filtered_transactions):
        if i < 5:
            top_transactions.append({
                "date": transaction.get("Дата платежа"),
                "amount": transaction.get("Сумма платежа"),
                "category": transaction.get("Категория"),
                "description": transaction.get("Описание")
            })
            i += 1
        else:
            break
    return top_transactions


def load_user_settings(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def get_currency_rates(currencies):
    # Пример использования API для получения курсов валют
    api_key = os.getenv("API_Key_currency")
    base_currency = 'RUB'  # Базовая валюта
    url = f'https://api.exchangerate-api.com/v4/latest/{base_currency}'

    response = requests.get(url)
    data = response.json()

    rates = {currency: data['rates'].get(currency) for currency in currencies}
    return rates

def get_stock_prices(stocks):
    # Пример использования Alpha Vantage API для получения цен акций
    api_key = os.getenv('API_Key_stokes')
    stock_prices = {}

    for stock in stocks:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock}&interval=1min&apikey={api_key}'
        response = requests.get(url)
        data = response.json()

        # Получаем последнюю цену
        try:
            last_refreshed = data['Meta Data']['3. Last Refreshed']
            last_price = data['Time Series (1min)'][last_refreshed]['1. open']
            stock_prices[stock] = float(last_price)
        except KeyError:
            stock_prices[stock] = None  # Если данные недоступны

    return stock_prices


# Пример использования
if __name__ == "__main__":
    user_data = get_user_data('user_settings.json')
    print(user_data)