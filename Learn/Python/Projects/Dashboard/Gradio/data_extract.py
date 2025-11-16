import datetime
import tempfile
from cachetools import cached, TTLCache
import pandas as pd
from matplotlib import pyplot as plt
import startup

cache = TTLCache(maxsize=128, ttl=300)

@cached(cache)
def get_unique_categories():
    if startup.csv_data is None:
        return []
    cats = sorted(startup.csv_data['categories'].dropna().unique().tolist())
    cats = [cat.capitalize() for cat in cats]
    return cats

def get_date_range():
    if startup.csv_data is None or startup.csv_data.empty:
        return None, None
    return startup.csv_data['order_date'].min(), startup.csv_data['order_date'].max()

def filter_data(start_date, end_date, category):
    if isinstance(start_date, str):
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    if isinstance(end_date, str):
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

    df = startup.csv_data.loc[
        (startup.csv_data['order_date'] >= pd.to_datetime(start_date)) &
        (startup.csv_data['order_date'] <= pd.to_datetime(end_date))
        ].copy()

    if category != "All Categories":
        df = df.loc[df['categories'].str.capitalize() == category].copy()

    return df

def get_dashboard_stats(start_date, end_date, category):
    df = filter_data(start_date, end_date, category)
    if df.empty:
        return (0, 0, 0, "N/A")

    df['revenue'] = df['price'] * df['quantity']
    total_revenue = df['revenue'].sum()
    total_orders = df['order_id'].nunique()
    avg_order_value = total_revenue / total_orders if total_orders else 0

    cat_revenues = df.groupby('categories')['revenue'].sum().sort_values(ascending=False)
    top_category = cat_revenues.index[0] if not cat_revenues.empty else "N/A"

    return (total_revenue, total_orders, avg_order_value, top_category.capitalize())

def get_data_for_table(start_date, end_date, category):
    df = filter_data(start_date, end_date, category)
    if df.empty:
        return pd.DataFrame()

    df = df.sort_values(by=["order_id", "order_date"], ascending=[True, False]).copy()

    columns_order = [
        "order_id", "order_date", "customer_id", "customer_name",
        "product_id", "product_names", "categories", "quantity",
        "price", "total"
    ]
    columns_order = [col for col in columns_order if col in df.columns]
    df = df[columns_order].copy()

    df['revenue'] = df['price'] * df['quantity']
    return df

def get_plot_data(start_date, end_date, category):
    df = filter_data(start_date, end_date, category)
    if df.empty:
        return pd.DataFrame()
    df['revenue'] = df['price'] * df['quantity']
    plot_data = df.groupby(df['order_date'].dt.date)['revenue'].sum().reset_index()
    plot_data.rename(columns={'order_date': 'date'}, inplace=True)
    return plot_data

def get_revenue_by_category(start_date, end_date, category):
    df = filter_data(start_date, end_date, category)
    if df.empty:
        return pd.DataFrame()
    df['revenue'] = df['price'] * df['quantity']
    cat_data = df.groupby('categories')['revenue'].sum().reset_index()
    cat_data = cat_data.sort_values(by='revenue', ascending=False)
    return cat_data

def get_top_products(start_date, end_date, category):
    df = filter_data(start_date, end_date, category)
    if df.empty:
        return pd.DataFrame()
    df['revenue'] = df['price'] * df['quantity']
    prod_data = df.groupby('product_names')['revenue'].sum().reset_index()
    prod_data = prod_data.sort_values(by='revenue', ascending=False).head(10)
    return prod_data

def create_matplotlib_figure(data, x_col, y_col, title, xlabel, ylabel, orientation='v'):
    plt.figure(figsize=(10, 6))
    if data.empty:
        plt.text(0.5, 0.5, 'No data available', ha='center', va='center')
    else:
        if orientation == 'v':
            plt.bar(data[x_col], data[y_col])
            plt.xticks(rotation=45, ha='right')
        else:
            plt.barh(data[x_col], data[y_col])
            plt.gca().invert_yaxis() 

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
        plt.savefig(tmpfile.name)
    plt.close()
    return tmpfile.name