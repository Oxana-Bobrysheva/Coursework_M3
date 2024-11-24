import json
import pandas as pd
import logging

from src.utils import read_xlsx

# Logging setting
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def analyze_cashback_categories(operations: list[dict], year: int, month: int) -> str:
    """Function for analysis of profitability of the category of increased cashback.
    Returns JSON string."""
    logger.info("Starting cashback analysis for year: %d, month: %d", year, month)
    if operations == []:
        return f"File {operations} is empty"

    else:
        # Converting the data into a Data Frame for easy analysis
        df = pd.DataFrame(operations)

        # Converting the date into datetime format
        df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], format="%d.%m.%Y")

        # Filtering data according to year and month
        filtered_df = df[
            (df["Дата платежа"].dt.year == year) & (df["Дата платежа"].dt.month == month)
        ]

        # Checking if data is not empty
        if filtered_df.empty:
            logger.warning("No transactions found for year: %d, month: %d", year, month)
            return json.dumps({}, ensure_ascii=False)

        # Grouping by categories and sum up the cashback
        cashback_analysis = filtered_df.groupby("Категория")["Кэшбэк"].sum().to_dict()

        logger.info("Cashback analysis completed: %s", cashback_analysis)

        # Returning the result in JSON format
        return json.dumps(cashback_analysis, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    operations = read_xlsx("../data/operations.xlsx")

    result = analyze_cashback_categories(operations, 2021, 11)
    print(result)
