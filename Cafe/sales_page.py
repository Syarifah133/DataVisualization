import os
import pandas as pd
import streamlit as st

orders_file = 'orders.csv'


def display_sales_reporting():  

    st.title("Sales Reporting")
    if not os.path.isfile(orders_file):
        st.info("No sales data found. Please add orders to view reports.")
        return

    # Load Orders Data
    orders_df = pd.read_csv(orders_file, parse_dates=['Order Time'])

    # Daily, Weekly, Monthly Reports
    st.subheader("Total Sales Report")
    orders_df['Date'] = orders_df['Order Time'].dt.date
    sales_by_date = orders_df.groupby('Date').agg(
        Quantity=('Price', 'count'), Revenue=('Price', 'sum')
    )
    st.line_chart(sales_by_date)

    # Coffee Type Breakdown
    st.subheader("Sales Breakdown by Coffee Type")
    coffee_breakdown = orders_df.groupby('Coffee Type').agg(
        Quantity=('Price', 'count'), Revenue=('Price', 'sum')
    ).sort_values('Quantity', ascending=False)
    st.bar_chart(coffee_breakdown['Quantity'])
    st.dataframe(coffee_breakdown)
