# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 14:02:27 2025

Note:
multiline strings use backslash at the end of a line to indicate \
that the string continues on the next line. \

    @author: prashanth pasham
"""
# print('this is a constants file')
Q_DATE_RANGE = "SELECT MIN(order_date), MAX(order_date) FROM df"
Q_UNIQUE_CATEGORIES = """SELECT DISTINCT categories \
                        FROM public.sales_data ORDER BY categories;"""
Q_DASHBOARD_STATS = """
        WITH category_totals AS (
            SELECT \
                categories,
                SUM(price * quantity) as category_revenue
            FROM public.sales_data
            WHERE order_date BETWEEN %s AND %s
            AND (%s = 'All Categories' OR categories = %s)
            GROUP BY categories
        ),
        top_category AS (
            SELECT categories
            FROM category_totals
            ORDER BY category_revenue DESC
            LIMIT 1
        ),
        overall_stats AS (
            SELECT \
                SUM(price * quantity) as total_revenue,
                COUNT(DISTINCT order_id) as total_orders,
                SUM(price * quantity) / COUNT(DISTINCT order_id) \
                as avg_order_value
            FROM public.sales_data
            WHERE order_date BETWEEN %s AND %s
            AND (%s = 'All Categories' OR categories = %s)
        )
        SELECT \
            total_revenue,
            total_orders,
            avg_order_value,
            (SELECT categories FROM top_category) as top_category
        FROM overall_stats
    """
Q_PLOT_DATA_BY_DATE_CATEGORY = """
                SELECT DATE(order_date) as date,
                       SUM(price * quantity) as revenue
                FROM public.sales_data
                WHERE order_date BETWEEN %s AND %s
                  AND (%s = 'All Categories' OR categories = %s)
                GROUP BY DATE(order_date)
                ORDER BY date
            """
Q_REVENUE_BY_CATEGORY = """
                SELECT categories,
                       SUM(price * quantity) as revenue
                FROM public.sales_data
                WHERE order_date BETWEEN %s AND %s
                  AND (%s = 'All Categories' OR categories = %s)
                GROUP BY categories
                ORDER BY revenue DESC
            """
Q_TOP_PRODUCTS = """
                SELECT product_names,
                       SUM(price * quantity) as revenue
                FROM public.sales_data
                WHERE order_date BETWEEN %s AND %s
                  AND (%s = 'All Categories' OR categories = %s)
                GROUP BY product_names
                ORDER BY revenue DESC
                LIMIT 10
            """
Q_RAW_DATA = """
                SELECT 
                    order_id, order_date, customer_id, customer_name, 
                    product_id, product_names, categories, quantity, price, 
                    (price * quantity) as revenue
                FROM public.sales_data
                WHERE order_date BETWEEN %s AND %s
                  AND (%s = 'All Categories' OR categories = %s)
                ORDER BY order_date, order_id
            """
