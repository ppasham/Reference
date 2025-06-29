'''
    You can run this command in your terminal to start the Streamlit app.
        C:Usersthoma> python -m streamlit run app.py

    You can now view your Streamlit app in your browser.
    Local URL: http://localhost:8501
    Network URL: http://192.168.0.59:8501
'''


import streamlit as st
from app_code import appFacade
import datetime as dt

DEBUG = False
# Streamlit App
st.title("Sales Performance Dashboard")
st.markdown("""
    This dashboard provides insights into sales performance, including revenue trends, category performance, and top products.
    Use the filters below to customize your view.
""")

# Filters
with st.container(), appFacade(sales_records=100_000, filename="C:\\temp\\sales_data.csv") as facade:
    col1, col2, col3 = st.columns([1, 1, 2])
    date_range = facade.get_date_range()
    if date_range is not None and not date_range.empty:        
        start_date:str = (date_range['Min_Date'].astype('datetime64[us]').item()).strftime('%Y-%m-%d')
        end_date:str = (date_range['Max_Date'].astype('datetime64[us]').item()).strftime('%Y-%m-%d')    
    else:
        start_date = "2010-01-01"
        end_date = "2023-12-31"
    if DEBUG:
        print(f"Start Date: {start_date}, End Date: {end_date}")
    categories = facade.get_unique_categories()
    category = col3.selectbox("Category", categories)

# Custom CSS for metrics
st.markdown("""
    <style>
    .metric-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 20px;
    }
    .metric-container {
        flex: 1;
        padding: 10px;
        text-align: center;
        background-color: #f0f2f6;
        border-radius: 5px;
        margin: 0 5px;
    }
    .metric-label {
        font-size: 14px;
        color: #555;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 18px;
        font-weight: bold;
        color: #0e1117;
    }
    </style>
""", unsafe_allow_html=True)

# Metrics
st.header("Key Metrics")
stats = facade.get_dashboard_stats(start_date, end_date, category)
print(f"Stats: {stats}")
if stats is not None and not getattr(stats, "empty", False):
    total_revenue, total_orders, avg_order_value, top_category = stats["total_revenue"].item(), stats["total_orders"].item(), stats["avg_order_value"].item(), stats["top_category"].item()
else:
    total_revenue, total_orders, avg_order_value, top_category = 0.00, 0.00, 0, "N/A"

# Custom metrics display
metrics_html = f"""
<div class="metric-row">
    <div class="metric-container">
        <div class="metric-label">Total Revenue</div>
        <div class="metric-value">${total_revenue:.2f}</div>
    </div>
    <div class="metric-container">
        <div class="metric-label">Total Orders</div>
        <div class="metric-value">{total_orders:,.0f}</div>
    </div>
    <div class="metric-container">
        <div class="metric-label">Average Order Value</div>
        <div class="metric-value">${avg_order_value:,.2f}</div>
    </div>
    <div class="metric-container">
        <div class="metric-label">Top Category</div>
        <div class="metric-value">{top_category}</div>
    </div>
</div>
"""
st.markdown(metrics_html, unsafe_allow_html=True)

# Visualization Tabs
st.header("Visualizations")
tabs = st.tabs(["Revenue Over Time", "Revenue by Category", "Top Products"])

# Revenue Over Time Tab
with tabs[0]:
    st.subheader("Revenue Over Time")
    revenue_data = facade.get_plot_data(start_date, end_date, category)
    st.pyplot(facade.plot_data(revenue_data, 'date', 'revenue', "Revenue Over Time", "Date", "Revenue"))

# Revenue by Category Tab
with tabs[1]:
    st.subheader("Revenue by Category")
    category_data = facade.get_revenue_by_category(start_date, end_date, category)
    st.pyplot(facade.plot_data(category_data, 'categories', 'revenue', "Revenue by Category", "Category", "Revenue"))

# Top Products Tab
with tabs[2]:
    st.subheader("Top Products")
    top_products_data = facade.get_top_products(start_date, end_date, category)
    st.pyplot(facade.plot_data(top_products_data, 'product_names', 'revenue', "Top Products", "Revenue", "Product Name", orientation='h'))

st.header("Raw Data")

raw_data = facade.get_data(
    start_date=start_date,
    end_date=end_date,
    category=category)

# Remove the index by resetting it and dropping the old index
if raw_data is not None:
    raw_data = raw_data.reset_index(drop=True)
    st.dataframe(raw_data, hide_index=True)
else:
    st.write("No data available for the selected filters.")

# Add spacing
st.write("")

