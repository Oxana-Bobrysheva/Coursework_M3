from dotenv import load_dotenv

from src.utils import get_unique_cards, get_list_of_cards_info, greetings, filter_by_time_range, read_xlsx, \
    get_top_transactions, load_user_settings, get_currency_rates, get_stock_prices


def get_started_main():
    input_date = input("Введите дату в формате YYYY-MM-DD HH:MM:SS - ")
    json_answer = {"greeting": greetings(input_date)}

    file_path = "../data/operations.xlsx"
    filtered_transactions = filter_by_time_range(read_xlsx(file_path), input_date)

    cards_info = get_unique_cards(filtered_transactions)

    new_key = "cards"
    nested_dict = get_list_of_cards_info(cards_info, filtered_transactions)
    json_answer[new_key] = nested_dict

    new_key = "top_transactions"
    nested_dict = get_top_transactions(filtered_transactions)
    json_answer[new_key] = nested_dict

    settings = load_user_settings('../user_settings.json')
    currencies = settings.get('user_currencies', [])
    stocks = settings.get('user_stocks', [])

    new_key = "currency_rates"
    nested_dict = get_currency_rates(currencies)
    json_answer[new_key] = nested_dict

    new_key = "stock_prices"
    nested_dict = get_stock_prices(stocks)
    json_answer[new_key] = nested_dict

    return json_answer


if __name__ == "__main__":
    print(get_started_main())
# 2021-02-15 10:00:00