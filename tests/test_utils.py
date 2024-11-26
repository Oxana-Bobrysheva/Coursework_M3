import unittest

import pandas as pd
import pytest
from unittest.mock import mock_open, patch, Mock
import json
from datetime import datetime
from src.utils import (greetings, time_range, filter_by_time_range,
                       get_unique_cards, get_list_of_cards_info, get_top_transactions,
                       load_user_settings, get_currency_rates, get_stock_prices, read_xlsx)

@pytest.fixture
def mock_logger():
    with patch('src.utils.logger') as mock_logger:
        yield mock_logger

@pytest.mark.parametrize("input_date, expected_greeting", [
    ("2022-01-01 03:00:00", "Доброй ночи"),
    ("2022-01-01 08:00:00", "Доброе утро"),
    ("2022-01-01 15:00:00", "Добрый день"),
    ("2022-01-01 20:00:00", "Добрый вечер")
])
def test_greetings(input_date, expected_greeting, mock_logger):
    assert greetings(input_date) == expected_greeting
    mock_logger.info.assert_called_once_with("Entering greetings function")


def test_time_range():
    # Test case 1: Input date with the first day of the month
    input_date_1 = "2022-01-01 08:00:00"
    start_time_1, end_time_1 = time_range(input_date_1)
    assert start_time_1 == "01.01.2022"
    assert end_time_1 == "01.01.2022"

    # Test case 2: Input date with a different day of the month
    input_date_2 = "2022-03-15 12:30:00"
    start_time_2, end_time_2 = time_range(input_date_2)
    assert start_time_2 == "01.03.2022"
    assert end_time_2 == "15.03.2022"

def test_read_xlsx(tmp_path):
    # Create a temporary Excel file for testing
    test_data = {
        'A': [1, 2, 3],
        'B': ['foo', 'bar', 'baz']
    }
    test_df = pd.DataFrame(test_data)
    test_file_path = tmp_path / "test_operations.xlsx"
    test_df.to_excel(test_file_path, index=False)

    # Test reading the temporary Excel file
    operations = read_xlsx(test_file_path)

    # Check if the operations list is not empty
    assert len(operations) > 0

def test_filter_by_time_range():
    # Mock operations data for testing
    operations = [
        {"Дата платежа": "01.01.2022"},
        {"Дата платежа": "15.01.2022"},
        {"Дата платежа": "25.01.2022"},
        {"Дата платежа": "10.02.2022"},
    ]

    # Set input date for filtering
    input_date = "2022-01-15 00:00:00"

    # Test filtering operations based on the time range
    filtered_operations = filter_by_time_range(operations, input_date)

    # Check if the filtered_operations list contains the expected operations
    assert len(filtered_operations) == 2
    assert filtered_operations[0]["Дата платежа"] == "01.01.2022"
    assert filtered_operations[1]["Дата платежа"] == "15.01.2022"


def test_get_unique_cards():
    # Mock filtered transactions data for testing
    filtered_transactions = [
        {"Номер карты": "1234"},
        {"Номер карты": "5678"},
        {"Номер карты": "1234"},
        {"Номер карты": "9999"},
    ]

    # Test extracting unique card numbers
    unique_cards = get_unique_cards(filtered_transactions)

    # Check if the unique_cards list contains the expected unique card numbers
    assert len(unique_cards) == 3
    assert "1234" in unique_cards
    assert "5678" in unique_cards
    assert "9999" in unique_cards


def test_get_list_of_cards_info():
    # Mock cards_info and filtered_transactions data for testing
    cards_info = ["1234567890123456", "9876543210987654"]
    filtered_transactions = [
        {"Номер карты": "1234567890123456", "Сумма платежа": 100, "Кэшбэк": 5},
        {"Номер карты": "1234567890123456", "Сумма платежа": 50, "Кэшбэк": 2},
        {"Номер карты": "9876543210987654", "Сумма платежа": 75, "Кэшбэк": 3},
    ]

    # Test aggregating information about cards
    list_of_cards_info = get_list_of_cards_info(cards_info, filtered_transactions)

    # Check if the list_of_cards_info contains the expected card information
    assert len(list_of_cards_info) == 2
    assert list_of_cards_info[0] == {"last_digits": "3456", "total_spent": 150.0, "cashback": 7}
    assert list_of_cards_info[1] == {"last_digits": "7654", "total_spent": 75.0, "cashback": 3}


def test_get_top_transactions():
    # Mock filtered_transactions data for testing
    filtered_transactions = [
        {"Дата платежа": "01.01.2022", "Сумма платежа": 100, "Категория": "Groceries", "Описание": "Grocery shopping"},
        {"Дата платежа": "15.01.2022", "Сумма платежа": 75, "Категория": "Dining", "Описание": "Restaurant bill"},
        {"Дата платежа": "25.01.2022", "Сумма платежа": 50, "Категория": "Shopping", "Описание": "Online purchase"},
        {"Дата платежа": "10.02.2022", "Сумма платежа": 200, "Категория": "Travel", "Описание": "Flight ticket"},
        {"Дата платежа": "05.02.2022", "Сумма платежа": 150, "Категория": "Entertainment", "Описание": "Concert tickets"},
    ]

    # Test getting top transactions
    top_transactions = get_top_transactions(filtered_transactions)

    # Check if the top_transactions list contains the top 5 transactions based on payment amount
    assert len(top_transactions) == 5
    assert top_transactions == [
        {"date": "25.01.2022", "amount": 50, "category": "Shopping", "description": "Online purchase"},
        {"date": "15.01.2022", "amount": 75, "category": "Dining", "description": "Restaurant bill"},
        {"date": "01.01.2022", "amount": 100, "category": "Groceries", "description": "Grocery shopping"},
        {"date": "05.02.2022", "amount": 150, "category": "Entertainment", "description": "Concert tickets"},
        {"date": "10.02.2022", "amount": 200, "category": "Travel", "description": "Flight ticket"},
    ]

class TestLoadUserSettings(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    def test_load_user_settings(self, mock_open):
        result = load_user_settings("test_file.json")
        self.assertEqual(result, {"key": "value"})


class TestGetCurrencyRates(unittest.TestCase):

    @patch('src.utils.requests.get')
    def test_get_currency_rates(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "rates": {
                "USD": 1.23,
                "EUR": 0.89
            }
        }
        mock_get.return_value = mock_response

        currencies = ["USD", "EUR"]
        expected_rates = {
            "USD": 1.23,
            "EUR": 0.89
        }

        result = get_currency_rates(currencies)
        self.assertEqual(result, expected_rates)


class TestGetStockPrices(unittest.TestCase):

    @patch('src.utils.requests.get')
    def test_get_stock_prices(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "Meta Data": {"3. Last Refreshed": "2022-01-01 16:00:00"},
            "Time Series (1min)": {
                "2022-01-01 16:00:00": {"1. open": "100.0"}
            }
        }
        mock_get.return_value = mock_response

        stocks = ["AAPL", "GOOGL"]
        expected_prices = {
            "AAPL": 100.0,
            "GOOGL": 100.0
        }

        result = get_stock_prices(stocks)
        self.assertEqual(result, expected_prices)