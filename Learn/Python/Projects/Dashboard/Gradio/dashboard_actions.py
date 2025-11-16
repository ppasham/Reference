import gradio as gr
import datetime
import data_extract as data

def update_dashboard(start_date, end_date, category):
    total_revenue, total_orders, avg_order_value, top_category = data.get_dashboard_stats(start_date, end_date, category)

    # Generate plots
    revenue_data = data.get_plot_data(start_date, end_date, category)
    category_data = data.get_revenue_by_category(start_date, end_date, category)
    top_products_data = data.get_top_products(start_date, end_date, category)

    revenue_over_time_path = data.create_matplotlib_figure(
        revenue_data, 'date', 'revenue',
        "Revenue Over Time", "Date", "Revenue"
    )
    revenue_by_category_path = data.create_matplotlib_figure(
        category_data, 'categories', 'revenue',
        "Revenue by Category", "Category", "Revenue"
    )
    top_products_path = data.create_matplotlib_figure(
        top_products_data, 'product_names', 'revenue',
        "Top Products", "Revenue", "Product Name", orientation='h'
    )

    # Data table
    table_data = data.get_data_for_table(start_date, end_date, category)

    return (
        revenue_over_time_path,
        revenue_by_category_path,
        top_products_path,
        table_data,
        total_revenue,
        total_orders,
        avg_order_value,
        top_category
    )

def create_dashboard():
    min_date, max_date = data.get_date_range()
    if min_date is None or max_date is None:
        min_date = datetime.datetime.now()
        max_date = datetime.datetime.now()

    default_start_date = min_date
    default_end_date = max_date

    with gr.Blocks(css="""
        footer {display: none !important;}
        .tabs {border: none !important;}  
        .gr-plot {border: none !important; box-shadow: none !important;}
    """) as dashboard:
        
        gr.Markdown("# Sales Performance Dashboard")

        # Filters row
        with gr.Row():
            start_date = gr.DateTime(
                label="Start Date",
                value=default_start_date.strftime('%Y-%m-%d'),
                include_time=False,
                type="datetime"
            )
            end_date = gr.DateTime(
                label="End Date",
                value=default_end_date.strftime('%Y-%m-%d'),
                include_time=False,
                type="datetime"
            )
            category_filter = gr.Dropdown(
                choices=["All Categories"] + data.get_unique_categories(),
                label="Category",
                value="All Categories"
            )

        gr.Markdown("# Key Metrics")

        # Stats row
        with gr.Row():
            total_revenue = gr.Number(label="Total Revenue", value=0)
            total_orders = gr.Number(label="Total Orders", value=0)
            avg_order_value = gr.Number(label="Average Order Value", value=0)
            top_category = gr.Textbox(label="Top Category", value="N/A")

        gr.Markdown("# Visualisations")
        # Tabs for Plots
        with gr.Tabs():
            with gr.Tab("Revenue Over Time"):
                revenue_over_time_image = gr.Image(label="Revenue Over Time", container=False)
            with gr.Tab("Revenue by Category"):
                revenue_by_category_image = gr.Image(label="Revenue by Category", container=False)
            with gr.Tab("Top Products"):
                top_products_image = gr.Image(label="Top Products", container=False)

        gr.Markdown("# Raw Data")
        # Data Table (below the plots)
        data_table = gr.DataFrame(
            label="Sales Data",
            type="pandas",
            interactive=False
        )

        # When filters change, update everything
        for f in [start_date, end_date, category_filter]:
            f.change(
                fn=lambda s, e, c: update_dashboard(s, e, c),
                inputs=[start_date, end_date, category_filter],
                outputs=[
                    revenue_over_time_image, 
                    revenue_by_category_image, 
                    top_products_image,
                    data_table,
                    total_revenue, 
                    total_orders,
                    avg_order_value, 
                    top_category
                ]
            )

        # Initial load
        dashboard.load(
            fn=lambda: update_dashboard(default_start_date, default_end_date, "All Categories"),
            outputs=[
                revenue_over_time_image, 
                revenue_by_category_image, 
                top_products_image,
                data_table,
                total_revenue, 
                total_orders,
                avg_order_value, 
                top_category
            ]
        )

    return dashboard