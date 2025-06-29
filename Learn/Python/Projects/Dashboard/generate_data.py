# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 16:29:15 2025

@author: prash
"""

# generate the 1m record CSV file
#
import polars as pl
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def generate_data(nrows: int, filename: str) -> pd.DataFrame:
    names = np.asarray(
        [
            "Laptop",
            "Smartphone",
            "Desk",
            "Chair",
            "Monitor",
            "Printer",
            "Paper",
            "Pen",
            "Notebook",
            "Coffee Maker",
            "Cabinet",
            "Plastic Cups",
        ]
    )

    categories = np.asarray(
        [
            "Electronics",
            "Electronics",
            "Office",
            "Office",
            "Electronics",
            "Electronics",
            "Stationery",
            "Stationery",
            "Stationery",
            "Electronics",
            "Office",
            "Sundry",
        ]
    )

    product_id = np.random.randint(len(names), size=nrows)
    quantity = np.random.randint(1, 11, size=nrows)
    price = np.random.randint(199, 10000, size=nrows) / 100

    # Generate random dates between 2010-01-01 and 2023-12-31
    start_date = datetime(2010, 1, 1)
    end_date = datetime(2023, 12, 31)
    date_range = (end_date - start_date).days

    # Create random dates as np.array and convert to string format
    order_dates = np.array([(start_date + timedelta(days=np.random.randint(
        0, date_range))).strftime('%Y-%m-%d') for _ in range(nrows)])

    # Define columns
    from typing import Any
    columns: dict[str, np.ndarray | list[Any] | np.generic] = {
        "order_id": np.arange(nrows),
        "order_date": order_dates,
        "customer_id": np.random.randint(100, 1000, size=nrows),
        "customer_name": [f"Customer_{i}"
                          for i in np.random.randint(2**15, size=nrows)],
        "product_id": product_id + 200,
        "product_names": names[product_id],
        "categories": categories[product_id],
        "quantity": quantity,
        "price": price,
        "total": price * quantity,
    }

    # Create Polars DataFrame and write to CSV with explicit delimiter
    df = pd.DataFrame(columns)
    # Ensure comma is used as the delimiter
    df.to_csv(filename, sep=',', index=False)
    return df

# Generate 100,000 rows of data with random order_date and save to CSV
# generate(100, "C:\\temp\\sales_data1.csv")
