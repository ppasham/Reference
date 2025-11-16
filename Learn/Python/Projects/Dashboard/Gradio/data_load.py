# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 16:51:16 2025

Load data from CSV file

@author: prashanth
"""
# ------------------------------------------------------------------
# 1) Load CSV data once
# ------------------------------------------------------------------
import pandas as pd
import warnings
from pandas import Int64Dtype, Float64Dtype, StringDtype, DataFrame

warnings.filterwarnings("ignore", category=FutureWarning, module="seaborn")
# Initialize global variable to hold CSV data
csv_data=pd.DataFrame()

def load_csv_data(filename: str) -> DataFrame:
    global csv_data
    
    # Optional: specify column dtypes if known; adjust as necessary
    dtype_dict ={
        "order_id": Int64Dtype(),
        "customer_id": Int64Dtype(),
        "product_id": Int64Dtype(),
        "quantity": Int64Dtype(),
        "price": Float64Dtype(),
        "total": Float64Dtype(),
        "customer_name": StringDtype(),
        "product_names": StringDtype(),
        "categories": StringDtype()
    }
    
    csv_data = pd.read_csv(
        filename,
        parse_dates=["order_date"],
        dayfirst=True,      # if your dates are DD/MM/YYYY format
        low_memory=False,
        dtype= dtype_dict
    )

    csv_data['order_date'] = pd.to_datetime(csv_data['order_date'], errors='coerce') # Replaces unparseable dates with NaT (Not a Time)
    return csv_data

