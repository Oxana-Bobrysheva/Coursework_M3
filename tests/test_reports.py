import unittest
from unittest.mock import patch

import pandas as pd

from src.reports import expenses_by_category


class TestExpensesByCategory(unittest.TestCase):

    @patch("src.reports.json.dumps")
    @patch("src.reports.logger")
    def test_expenses_by_category(self, mock_logger, mock_json):
        test_data = {
            "Дата платежа": ["01.01.2022", "05.01.2022", "10.01.2022"],
            "Категория": ["Grocery", "Clothing", "Grocery"],
            "Сумма платежа": [50.0, 30.0, 20.0],
        }

        df = pd.DataFrame(test_data)
        category = "Grocery"
        reference_date = "2022-01-15"

        mock_json.return_value = '{"category": "Grocery", "total_expenses": 70.0}'

        result = expenses_by_category(df, category, reference_date)

        mock_logger.info.assert_called_with(
            "Total expenses for category '%s': %d", category, 70.0
        )
        mock_json.assert_called_with(
            {"category": category, "total_expenses": 70.0}, ensure_ascii=False, indent=2
        )

        self.assertEqual(result, '{"category": "Grocery", "total_expenses": 70.0}')


if __name__ == "__main__":
    unittest.main()
