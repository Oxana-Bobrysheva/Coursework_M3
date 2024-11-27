import unittest
from unittest.mock import MagicMock, patch

from src.services import analyze_cashback_categories


class TestAnalyzeCashbackCategories(unittest.TestCase):

    @patch("src.services.pd.DataFrame")
    @patch("src.services.pd.to_datetime")
    @patch("src.services.json.dumps")
    @patch("src.services.logger")
    def test_analyze_cashback_categories(
        self, mock_logger, mock_json, mock_to_datetime, mock_df
    ):
        operations = [
            {"Дата платежа": "01.01.2022", "Категория": "Grocery", "Кэшбэк": 5.0},
            {"Дата платежа": "05.01.2022", "Категория": "Clothing", "Кэшбэк": 3.5},
            {"Дата платежа": "10.01.2022", "Категория": "Grocery", "Кэшбэк": 2.0},
        ]

        year = 2022
        month = 1

        mock_df.return_value = MagicMock()
        mock_to_datetime.return_value = MagicMock()
        mock_json.return_value = '{"Grocery": 7.0, "Clothing": 3.5}'

        result = analyze_cashback_categories(operations, year, month)

        mock_logger.info.assert_called_with(
            "Starting cashback analysis for year: %d, month: %d", year, month
        )
        mock_df.assert_called_with(operations)
        mock_to_datetime.assert_called()
        mock_json.assert_called_with({}, ensure_ascii=False)

        self.assertEqual(result, '{"Grocery": 7.0, "Clothing": 3.5}')


if __name__ == "__main__":
    unittest.main()
