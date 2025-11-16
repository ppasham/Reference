# Browse : http://127.0.0.1:7860/
import warnings
import taipy.gui as gui
import taipy.gui.builder as tgb

from Taipy.data_extract import categories, raw_data, start_date, end_date, selected_category, total_revenue, \
    total_orders, avg_order_value, top_category, selected_tab, revenue_data, category_data, top_products_data


warnings.filterwarnings("ignore", category=FutureWarning, module="seaborn")

#section 3
with tgb.Page() as page:
    print("Building the page...started.")
    tgb.text("# Sales Performance Dashboard", mode="md")
    # Filters section
    with tgb.part(class_name="card"):
        print("Building the page part...filters.")
        with tgb.layout(columns="1 1 2"):  # Arrange elements in 3 columns
            with tgb.part():
                tgb.text("Filter From:")
                tgb.date(start_date)
            with tgb.part():
                tgb.text("To:")
                tgb.date(end_date)
            with tgb.part():
                tgb.text("Filter by Category:")
                tgb.selector(
                    value=selected_category,
                    lov=categories,
                    dropdown=True,
                    width="300px"
                )

    # Metrics section
    tgb.text("## Key Metrics", mode="md")
    with tgb.layout(columns="1 1 1 1"):
        print("Building the page part...metrics.")
        with tgb.part(class_name="metric-card"):
            tgb.text("### Total Revenue", mode="md")
            tgb.text(f"{total_revenue}")
        with tgb.part(class_name="metric-card"):
            tgb.text("### Total Orders", mode="md")
            tgb.text(f"{total_orders}")
        with tgb.part(class_name="metric-card"):
            tgb.text("### Average Order Value", mode="md")
            tgb.text(f"{avg_order_value}")
        with tgb.part(class_name="metric-card"):
            tgb.text("### Top Category", mode="md")
            tgb.text(f"{top_category}")

    tgb.text("## Visualizations", mode="md")
    # Selector for visualizations with reduced width
    DROPDOWN_OPTIONS = {"Revenue Over Time": 0, "Revenue by Category": 1, "Top Products": 3}
    DROPDOWN_WIDTH = "360px"  # Semantic
    print(f"Building the Visualizations for {DROPDOWN_OPTIONS}")
    with tgb.part(style="width: 50px;"):  # Reduce width of the dropdown
        tgb.selector(
            value=f"{selected_tab}",
            lov=DROPDOWN_OPTIONS,
            dropdown=True,
            width=DROPDOWN_WIDTH,  # Reduce width of the dropdown
        )

    # Conditional rendering of charts based on selected_tab
    with tgb.part(render=selected_tab == 'Revenue Over Time'):
        print("Building the page part...revenue_data.")
        tgb.chart(
            data=f"{revenue_data}",
            x="order_date",
            y="revenue",
            type="line",
            title="Revenue Over Time",
        )

    with tgb.part(render=selected_tab == 'Revenue by Category'):
        print("Building the page part...category_data.")
        tgb.chart(
            data=f"{category_data}",
            x="categories",
            y="revenue",
            type="bar",
            title="Revenue by Category",
        )

    with tgb.part(render=selected_tab == 'Top Products'):
        print("Building the page part...top_products_data.")
        tgb.chart(
            data=f"{top_products_data}",
            x="product_names",
            y="revenue",
            type="bar",
            title="Top Products",
        )

    # Raw Data Table
    print("Building the page part...raw_data.")
    tgb.text("## Raw Data", mode="md")
    tgb.table(data=raw_data)

#if __name__ == "__main__":
    try:
        gui.Gui(page).run(
            title="Sales Dashboard",
            dark_mode=False,
            debug=True,
            port="auto",
            allow_unsafe_werkzeug=True,
            async_mode="threading"
        )
    except Exception as e:
        print(e)
