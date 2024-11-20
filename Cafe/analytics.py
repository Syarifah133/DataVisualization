import os
import pandas as pd
import streamlit as st

orders_file = 'orders.csv'

def display_analytics_dashboard():
    st.title("Analytics Dashboard")
    if not os.path.isfile(orders_file):
        st.info("No sales data found. Please add orders to view analytics.")
        return

    orders_df = pd.read_csv(orders_file, parse_dates=['Order Time'])

    # Sales Trend Over Time
    st.subheader("Sales Trend (Daily)")
    orders_df['Date'] = orders_df['Order Time'].dt.date
    sales_by_date = orders_df.groupby('Date').agg(Quantity=('Price', 'count'), Revenue=('Price', 'sum'))
    st.line_chart(sales_by_date)

    # Revenue Trend Over Time
    st.subheader("Revenue Trend (Weekly)")
    orders_df['Week'] = orders_df['Order Time'].dt.to_period('W')
    revenue_by_week = orders_df.groupby('Week').agg(Revenue=('Price', 'sum'))
    st.line_chart(revenue_by_week)
