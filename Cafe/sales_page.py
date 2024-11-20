import os
import pandas as pd
import streamlit as st

orders_file = 'orders.csv'

# Assuming inventory costs (for simplicity, you may want to replace this with a dynamic cost structure)
coffee_costs = {
    'Americano': 2.0,  # Cost per unit for Americano
    'Cappuccino': 2.5,  # Cost per unit for Cappuccino
    'Latte': 2.5,       # Cost per unit for Latte
    'Espresso': 1.5     # Cost per unit for Espresso
}

def display_sales_reporting():  
    st.title("Sales Reporting")
    
    if not os.path.isfile(orders_file):
        st.info("No sales data found. Please add orders to view reports.")
        return

    # Load Orders Data
    orders_df = pd.read_csv(orders_file, parse_dates=['Order Time'])

    # Total Sales Report (Daily, Weekly, Monthly)
    st.subheader("Total Sales Report")
    
    # Adding date-based columns
    orders_df['Date'] = orders_df['Order Time'].dt.date
    orders_df['Week'] = orders_df['Order Time'].dt.to_period('W').dt.start_time
    orders_df['Month'] = orders_df['Order Time'].dt.to_period('M').dt.start_time

    # Group by Date for Daily Sales Report
    daily_sales = orders_df.groupby('Date').agg(
        Quantity=('Price', 'count'),
        Revenue=('Price', 'sum')
    )

    st.write("### Daily Sales")
    st.line_chart(daily_sales)

    # Group by Week for Weekly Sales Report
    weekly_sales = orders_df.groupby('Week').agg(
        Quantity=('Price', 'count'),
        Revenue=('Price', 'sum')
    )
    
    st.write("### Weekly Sales")
    st.line_chart(weekly_sales)

    # Group by Month for Monthly Sales Report
    monthly_sales = orders_df.groupby('Month').agg(
        Quantity=('Price', 'count'),
        Revenue=('Price', 'sum')
    )
    
    st.write("### Monthly Sales")
    st.line_chart(monthly_sales)

    # Coffee Type Breakdown
    st.subheader("Sales Breakdown by Coffee Type")
    coffee_breakdown = orders_df.groupby('Coffee Type').agg(
        Quantity=('Price', 'count'),
        Revenue=('Price', 'sum')
    ).sort_values('Quantity', ascending=False)
    
    st.write("### Coffee Type Breakdown")
    st.bar_chart(coffee_breakdown['Quantity'])
    st.dataframe(coffee_breakdown)

    # Best and Worst Sellers
    st.subheader("Best and Worst Sellers")
    
    # Best Sellers (Highest Quantity Sold)
    best_seller = coffee_breakdown['Quantity'].idxmax()
    best_seller_qty = coffee_breakdown['Quantity'].max()

    # Worst Sellers (Lowest Quantity Sold)
    worst_seller = coffee_breakdown['Quantity'].idxmin()
    worst_seller_qty = coffee_breakdown['Quantity'].min()

    st.write(f"**Best Seller:** {best_seller} with {best_seller_qty} units sold")
    st.write(f"**Worst Seller:** {worst_seller} with {worst_seller_qty} units sold")

    # Total Profit Calculation
    st.subheader("Total Profit Calculation")

    # Assuming revenue - inventory costs gives the profit for each coffee type sold
    orders_df['Cost'] = orders_df['Coffee Type'].map(coffee_costs)
    orders_df['Profit'] = orders_df['Price'] - orders_df['Cost']
    
    daily_profit = orders_df.groupby('Date')['Profit'].sum()
    st.write("### Daily Profit")
    st.line_chart(daily_profit)

    weekly_profit = orders_df.groupby('Week')['Profit'].sum()
    st.write("### Weekly Profit")
    st.line_chart(weekly_profit)

    monthly_profit = orders_df.groupby('Month')['Profit'].sum()
    st.write("### Monthly Profit")
    st.line_chart(monthly_profit)
