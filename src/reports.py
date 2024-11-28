import json
import logging
from datetime import datetime, timedelta

import pandas as pd

from src.utils import read_xlsx

# Logging settings
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def expenses_by_category(df: pd.DataFrame, category: str, reference_date: str) -> str:
    """Function returns expenses by categories for a three-month period in form of JSON string."""
    logger.info(
        "Starting expense analysis for category: '%s' starting from date: '%s'",
        category,
        reference_date,
    )

    # Converting date of the report into datetime
    reference_date = datetime.strptime(reference_date, "%Y-%m-%d")

    # Setting three-month period
    start_date = reference_date - timedelta(days=90)
    end_date = reference_date

    df["Дата платежа"] = pd.to_datetime(
        df["Дата платежа"], format="%d.%m.%Y", dayfirst=True
    )
    # Filtering data by category and date
    filtered_df = df[
        (df["Категория"] == category)
        & (df["Дата платежа"] >= start_date)
        & (df["Дата платежа"] <= end_date)
    ]

    # Checking if filtered_df is empty
    if filtered_df.empty:
        logger.warning(
            "No expenses found for category: '%s' in the period from %s to %s",
            category,
            start_date.date(),
            end_date.date(),
        )
        return json.dumps({}, ensure_ascii=False)

    # Summing up the expenses by category
    total_expenses = round(filtered_df["Сумма платежа"].sum(), 2)

    logger.info("Total expenses for category '%s': %d", category, total_expenses)

    # Returning the result in JSON string
    return json.dumps(
        {"category": category, "total_expenses": total_expenses},
        ensure_ascii=False,
        indent=2,
    )


if __name__ == "__main__":
    operations = read_xlsx("../data/operations.xlsx")

    df = pd.DataFrame(operations)

    result = expenses_by_category(df, "Супермаркеты", "2021-05-01")
    print(result)
