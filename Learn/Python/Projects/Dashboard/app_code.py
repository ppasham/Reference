# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 16:51:16 2025

Generate data
Load data
Query data
Display data

@author: prash
"""
import logging
import generate_data as ds
import polars as pl;
from pandasql import sqldf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[logging.StreamHandler(),  # Output to console
                                  logging.FileHandler('app.log')]) # Output to a file
_data  = pd.DataFrame()
DEBUG = True
class appFacade:
    
    def __init__(self, sales_records: int, filename: str):
        self.load_data(sales_records, filename)
    
    def __enter__(self):
        print(f"Entering context for app Facade")
        return self  # Return the instance itself

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Exiting context for app Facade")
        if exc_type:
            print(f"An exception occurred: {exc_val}")
            # Optionally handle the exception and return True to suppress it
            # return True

    def load_data(self, nrows: int, filename: str):
        self._data = ds.generate_data(nrows, filename)        

    def get_data(self, start_date, end_date, category) -> pd.DataFrame | None:
        # Query the data to get sales data within the specified date range and category
        sales_data= self._data[(self._data['order_date'] >= start_date) & (self._data['order_date'] <= end_date)]
        query= f"""
                SELECT 
                    order_id, order_date, customer_id, customer_name, 
                    product_id, product_names, categories, quantity, price, 
                    (price * quantity) as revenue
                FROM sales_data
                WHERE (categories = 'All Categories' OR categories = '{category}')
                ORDER BY order_date, order_id
            """        
        # Format the query with parameters
        query = query.format(category=category)
        # Execute the query using pandasql
        items = sqldf(query, locals())      
        print(f"Query executed successfully")
        return items
    def get_date_range(self) -> pd.DataFrame|None:
        sales_data= self._data
        sales_data["order_date"] = pd.to_datetime(sales_data["order_date"], format='%Y-%m-%d')
        min_date = sales_data['order_date'].min()
        max_date = sales_data['order_date'].max()
        return pd.DataFrame({'Min_Date': [min_date], 'Max_Date': [max_date]})       
    def get_unique_categories(self) -> pd.DataFrame:
        # Query the data to get unique categories
        unique_categories = pd.DataFrame({'categories': self._data['categories'].unique()}).sort_values('categories')
        unique_categories = pd.concat([unique_categories, pd.DataFrame({"categories": ["All Categories"]})], ignore_index=True)
        return unique_categories
    def get_dashboard_stats(self,start_date, end_date, category) -> pd.DataFrame |None:
        # Query the data to get dashboard stats
        sales_data= self._data[(self._data['order_date'] >= start_date) & (self._data['order_date'] <= end_date)]        
        query_stats = f"""
        WITH
        category_totals AS (
            SELECT 
                categories,
                SUM(price * quantity) as category_revenue
            FROM sales_data
            WHERE  (categories = 'All Categories' OR categories = '{category}')
            GROUP BY categories
            ),
        top_category AS (
            SELECT categories
            FROM category_totals
            ORDER BY category_revenue DESC
            LIMIT 1
            ),        
        overall_stats AS (
            SELECT 
                SUM(price * quantity) as total_revenue,
                COUNT(DISTINCT order_id) as total_orders,
                SUM(price * quantity) / COUNT(DISTINCT order_id) 
                as avg_order_value
            FROM sales_data
            WHERE  (categories = 'All Categories' OR categories = '{category}')
            )
        SELECT 
            os.total_revenue,   
            os.total_orders,
            os.avg_order_value,
            (SELECT categories FROM top_category) as top_category
        FROM overall_stats os 
    """ 
        if DEBUG:
            print(f"Querying dashboard stats for {start_date} to {end_date} in category {category}")
            print(self._data)
        # Format the query with parameters
        query_stats = query_stats.format(category=category)
        # Execute the query using pandasql
        stats = sqldf(query_stats, locals())
        return stats
    def get_plot_data(self, start_date, end_date, category) -> pd.DataFrame | None:
        sales_data= self._data[(self._data['order_date'] >= start_date) & (self._data['order_date'] <= end_date)]
        # Query the data to get revenue over time
        # Use pandasql to execute the SQL query on the DataFrame
        query = f"""
            SELECT DATE(order_date) as date, SUM(price * quantity) as revenue
            FROM sales_data
            WHERE (categories = 'All Categories' OR categories = '{category}')
            GROUP BY DATE(order_date)
            ORDER BY date;
        """
        query_formatted = query.format(category=category)        
        plot_data = sqldf(query_formatted, locals())
        return plot_data
    def get_revenue_by_category(self, start_date, end_date, category) -> pd.DataFrame |None:
        # Query the data to get revenue by category
        sales_data= self._data[(self._data['order_date'] >= start_date) & (self._data['order_date'] <= end_date)]
        query = f"""
            SELECT categories, SUM(price * quantity) as revenue
            FROM sales_data
            WHERE (categories = 'All Categories' OR categories = '{category}')
            GROUP BY categories
            HAVING SUM(price * quantity) > 0            
            ORDER BY revenue DESC;
        """
        query = query.format(category=category)
        revenue_by_category = sqldf(query, locals())
        return revenue_by_category
    def get_top_products(self, start_date, end_date, category) -> pd.DataFrame | None:
        sales_data= self._data[(self._data['order_date'] >= start_date) & (self._data['order_date'] <= end_date)]
        # Query the data to get top products
        query = f"""
            SELECT product_names, SUM(price * quantity) as revenue
            FROM sales_data
            WHERE (categories = 'All Categories' OR categories = '{category}')
            GROUP BY product_names
            HAVING SUM(price * quantity) > 0
            ORDER BY revenue DESC
            LIMIT 10;
        """
        query = query.format(category=category)
        top_products = sqldf(query, locals())
        return top_products
    def plot_data(self, _data, x_col, y_col, title, xlabel, ylabel, orientation='v'):
        fig, ax = plt.subplots(figsize=(10, 6))
        if _data is not None and not getattr(_data, "empty", False):
            if orientation == 'v':
                ax.bar(_data[x_col], _data[y_col])
            else:
                ax.barh(_data[x_col], _data[y_col])
            ax.set_title(title)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            plt.xticks(rotation=45)
        else:
            ax.text(0.5, 0.5, "No data available", ha='center', va='center')
        return fig

    
    # def generate_data(nrows: int, filename: str) -> pl.DataFrame:

    #     # Generate 100,000 rows of data with random order_date and save to CSV
    #     data = ds.generate(nrows, filename)
    #     return data
    # Approach 1: Query the data using Polars SDataFrame SQL API
    # Load the data into a Polars DataFrame
    #ddf = self._data.sql("SELECT MIN(order_date) as Min_Date, MAX(order_date) as Max_Date FROM self")


    # Approach 2: Query the data using Polars SQLContext
    # Load the data into a Polars SQLContext
    # Assuming the CSV file is already generated and available at the specified path
        #sales_dataContext = pl.SQLContext(sales_data=_data)
    # Query the data to get the date range
        #dates = sales_dataContext.execute("SELECT MIN(order_date) as Min_Date, MAX(order_date) as Max_Date FROM sales_data")
    # Collect the results
        #print(dates.collect())
    print("the app has finished running")

