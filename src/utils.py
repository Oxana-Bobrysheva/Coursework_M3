import datetime
import numpy as np
import pandas as pd
import json
import requests
import os
import logging
from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def greetings(input_date: str) -> str:
    """Function <greetings> takes a string with date and time in form YYYY-MM-DD HH:MM:SS
    and returns the string with four different greetings depending on the time"""
    logger.info("Entering greetings function")
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
    logger.info("Entering time_range function")
    date_obj = datetime.datetime.strptime(input_date, "%Y-%m-%d %H:%M:%S")
    end_time = date_obj.strftime("%d.%m.%Y")
    new_date_obj = date_obj.replace(day=1)
    start_time = new_date_obj.strftime("%d.%m.%Y")
    logger.info("Exiting time_range function")
    return start_time, end_time


def read_xlsx(file_path: str) -> list[dict]:
    """This function allows to read <operations.xlsx> and returns a list of
    dictionaries."""
    logger.info("Entering read_xlsx function")
    operations = []
    try:
        df = pd.read_excel(file_path)
        for index, row in df.iterrows():
            operations.append(row.to_dict())
    except FileNotFoundError:
        logger.error(f"File {file_path} was not found.")
        print(f"File {file_path} was not found.")
    except Exception as e:
        logger.error(f"Error occurred: {e}.")
        print(f"Error occurred: {e}.")
    logger.info("Exiting read_xlsx function")
    return operations


def filter_by_time_range(operations: list, input_date: str) -> list:
    """Function <filter_by_time_range> takes list of operations and returns a new list of operations
    filtered by time range"""
    logger.info("Entering filter_by_time_range function")
    filtered_operations = []
    start_time, end_time = time_range(input_date)
    start_time_obj = datetime.datetime.strptime(start_time, "%d.%m.%Y")
    end_time_obj = datetime.datetime.strptime(end_time, "%d.%m.%Y")
    for operation in operations:
        if (
            isinstance(operation["Дата платежа"], str)
            and start_time_obj
            <= datetime.datetime.strptime(operation["Дата платежа"], "%d.%m.%Y")
            <= end_time_obj
        ):
            filtered_operations.append(operation)
    logger.info("Exiting filter_by_time_range function")
    return filtered_operations


def get_unique_cards(filtered_transactions):
    """Function that gets a set of card numbers from filtered list of operations"""
    logger.info("Entering get_unique_cards function")
    cards_info: list = []
    if filtered_transactions:
        for transaction in filtered_transactions:
            card_number = transaction["Номер карты"]
            if card_number and pd.notna(card_number):
                cards_info.append(card_number)
    unique_cards = set(cards_info)
    logger.info("Exiting get_unique_cards function")
    return list(unique_cards)


def get_list_of_cards_info(cards_info: list, filtered_transactions: list) -> list[dict]:
    """Function that gets requested information about cards"""
    logger.info("Entering get_list_of_cards_info function")
    list_of_cards_info = []

    for card in cards_info:
        last_digits = card[-4:]
        total_spent = 0
        cashback = 0

        for transaction in filtered_transactions:
            if transaction["Номер карты"] == card:
                total_spent += transaction["Сумма платежа"]
                # We get the value of cashback, if it is nan, we add 0
                cashback_value = transaction.get("Кэшбэк", 0)
                if isinstance(cashback_value, (int, float)) and not np.isnan(
                    cashback_value
                ):
                    cashback += cashback_value
        total_spent = round(total_spent, 2)
        list_of_cards_info.append(
            {
                "last_digits": last_digits,
                "total_spent": total_spent,
                "cashback": cashback,
            }
        )
    logger.info("Exiting get_list_of_cards_info function")
    return list_of_cards_info


def get_top_transactions(filtered_transactions):
    """Function that gets top-5 operations from the list of operations"""
    logger.info("Entering get_top_transactions function")
    top_transactions = []
    sorted_filtered_transactions = sorted(
        filtered_transactions, key=lambda x: x["Сумма платежа"]
    )
    i = 0
    for i, transaction in enumerate(sorted_filtered_transactions):
        if i < 5:
            top_transactions.append(
                {
                    "date": transaction.get("Дата платежа"),
                    "amount": transaction.get("Сумма платежа"),
                    "category": transaction.get("Категория"),
                    "description": transaction.get("Описание"),
                }
            )
            i += 1
        else:
            break
    logger.info("Exiting get_top_transactions function")
    return top_transactions


def load_user_settings(file_path):
    """Function that reads information from json file"""
    logger.info("Entering load_user_settings function")
    with open(file_path, "r") as file:
        return json.load(file)


def get_currency_rates(currencies):
    """Function that makes API request and returns currency information"""
    logger.info("Entering get_currency_rates function")
    api_key = os.getenv("API_Key_currency")
    base_currency = "RUB"  # Базовая валюта
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"

    response = requests.get(url)
    data = response.json()

    rates = {currency: data["rates"].get(currency) for currency in currencies}
    logger.info("Exiting get_currency_rates function")
    return rates


def get_stock_prices(stocks):
    logger.info("Entering get_stock_prices function")
    # Alpha Vantage API for stocks
    api_key = os.getenv("API_Key_stokes")
    stock_prices = {}

    for stock in stocks:
        url = (
            f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock}"
            f"&interval=1min&apikey={api_key}"
        )
        response = requests.get(url)
        data = response.json()

        # We get mean price
        try:
            last_refreshed = data["Meta Data"]["3. Last Refreshed"]
            last_price = data["Time Series (1min)"][last_refreshed]["1. open"]
            stock_prices[stock] = float(last_price)
        except KeyError:
            logger.error(f"Error occurred: KeyError.")
            stock_prices[stock] = None  # Если данные недоступны
    logger.info("Exiting get_stock_prices function")
    return stock_prices
