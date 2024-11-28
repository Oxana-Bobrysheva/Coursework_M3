from unittest.mock import patch

from src.views import get_started_main

operations_for_testing = [
    {
        "Дата операции": "03.01.2018 14:55:21",
        "Дата платежа": "05.01.2018",
        "Номер карты": "*7197",
        "Статус": "OK",
        "Сумма операции": -21.0,
        "Валюта операции": "RUB",
        "Сумма платежа": -21.0,
        "Валюта платежа": "RUB",
        "Кэшбэк": 1,
        "Категория": "Красота",
        "MCC": 5977.0,
        "Описание": "OOO Balid",
        "Бонусы (включая кэшбэк)": 0,
        "Округление на инвесткопилку": 0,
        "Сумма операции с округлением": 21.0,
    },
    {
        "Дата операции": "01.01.2018 20:27:51",
        "Дата платежа": "04.01.2018",
        "Номер карты": "*7197",
        "Статус": "OK",
        "Сумма операции": -316.0,
        "Валюта операции": "RUB",
        "Сумма платежа": -316.0,
        "Валюта платежа": "RUB",
        "Кэшбэк": 1,
        "Категория": "Красота",
        "MCC": 5977.0,
        "Описание": "OOO Balid",
        "Бонусы (включая кэшбэк)": 6,
        "Округление на инвесткопилку": 0,
        "Сумма операции с округлением": 316.0,
    },
    {
        "Дата операции": "01.01.2018 12:49:53",
        "Дата платежа": "01.01.2018",
        "Номер карты": 0,
        "Статус": "OK",
        "Сумма операции": -3000.0,
        "Валюта операции": "RUB",
        "Сумма платежа": -3000.0,
        "Валюта платежа": "RUB",
        "Кэшбэк": 1,
        "Категория": "Переводы",
        "MCC": 0,
        "Описание": "Линзомат ТЦ Юность",
        "Бонусы (включая кэшбэк)": 0,
        "Округление на инвесткопилку": 0,
        "Сумма операции с округлением": 3000.0,
    },
]


@patch("src.views.get_stock_prices")
@patch("src.views.get_currency_rates")
@patch("src.views.load_user_settings")
@patch("src.views.read_xlsx")
def test_get_started_main(
    mock_read_xlsx,
    mock_load_user_settings,
    mock_get_currency_rates,
    mock_get_stock_prices,
):

    # Mocking dependencies and sample data
    mock_read_xlsx.return_value = operations_for_testing
    mock_load_user_settings.return_value = {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN"],
    }
    mock_get_currency_rates.return_value = {"USD": 100, "EUR": 105}
    mock_get_stock_prices.return_value = {"AAPL": 122, "AMZN": 13}

    # Call the function and assert the output
    assert (
        get_started_main("2018-01-05 14:55:21")
        == """{
    "greeting": "Добрый день",
    "cards": [
        {
            "last_digits": "7197",
            "total_spent": -337.0,
            "cashback": 2
        }
    ],
    "top_transactions": [
        {
            "date": "01.01.2018",
            "amount": -3000.0,
            "category": "Переводы",
            "description": "Линзомат ТЦ Юность"
        },
        {
            "date": "04.01.2018",
            "amount": -316.0,
            "category": "Красота",
            "description": "OOO Balid"
        },
        {
            "date": "05.01.2018",
            "amount": -21.0,
            "category": "Красота",
            "description": "OOO Balid"
        }
    ],
    "currency_rates": {
        "USD": 100,
        "EUR": 105
    },
    "stock_prices": {
        "AAPL": 122,
        "AMZN": 13
    }
}"""
    )
