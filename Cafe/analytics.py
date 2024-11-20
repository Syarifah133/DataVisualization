import os
import pandas as pd
import streamlit as st

# Define the path to your orders and inventory files
orders_file = 'orders.csv'
inventory_file = 'inventory.csv'  # Make sure your inventory data is stored in a CSV or other format

# Example of maximum stock levels for inventory items (can be adjusted based on your requirements)
max_stock = {
    'coffee beans': 100,
    'milk': 50,
    'sugar': 30,
    'cups': 200
}

# Assuming inventory data is stored in a dictionary
# This should be replaced with actual inventory data reading logic
inventory = {
    'coffee beans': 60,
    'milk': 20,
    'sugar': 15,
    'cups': 150
}

# Load orders from the CSV file
def load_orders():
    if os.path.isfile(orders_file):
        return pd.read_csv(orders_file, parse_dates=['Order Time'])
    return pd.DataFrame()  # Empty dataframe if no orders found

# Check inventory health for low stock items
def check_low_inventory():
    low_inventory_items = []
    for item, amount in inventory.items():
        stock_ratio = amount / max_stock[item]
        if stock_ratio <= 0.2:  # If stock is below 20% of max stock
            low_inventory_items.append(item)
    return low_inventory_items

def display_analytics_dashboard():
    st.title("Analytics Dashboard")

    # Load the order data
    orders_df = load_orders()
    
    if orders_df.empty:
        st.info("No sales data found. Please add orders to view analytics.")
        return

    # Sales Trend (Daily)
    st.subheader("Sales Trend (Daily)")
    orders_df['Date'] = orders_df['Order Time'].dt.date
    sales_by_date = orders_df.groupby('Date').agg(Quantity=('Price', 'count'), Revenue=('Price', 'sum'))
    st.line_chart(sales_by_date)

    # Revenue Trend (Weekly)
    st.subheader("Revenue Trend (Weekly)")
    orders_df['Week'] = orders_df['Order Time'].dt.to_period('W')
    revenue_by_week = orders_df.groupby('Week').agg(Revenue=('Price', 'sum'))
    st.line_chart(revenue_by_week)

    # Real-Time Monitoring: Current Orders and Sales
    st.subheader("Current Orders & Sales")
    current_sales = orders_df.tail(10)  # Show last 10 orders
    st.dataframe(current_sales[['Order Time', 'Coffee Type', 'Price']])

    # Real-Time Sales Summary
    total_sales = orders_df['Price'].sum()
    total_orders = len(orders_df)
    st.markdown(f"**Total Sales Revenue:** ${total_sales:.2f}")
    st.markdown(f"**Total Orders Processed:** {total_orders}")

    # Inventory Health Check: Low Stock Items
    st.subheader("Inventory Health Check")
    low_inventory_items = check_low_inventory()
    
    if low_inventory_items:
        st.warning(f"The following items are running low and need restocking: {', '.join(low_inventory_items)}")
    else:
        st.success("All inventory levels are healthy.")

    # Show Current Inventory Levels
    st.subheader("Current Inventory Levels")
    for item, amount in inventory.items():
        max_amount = max_stock[item]
        stock_ratio = min(amount / max_amount, 1.0)
        status = "Low Stock" if stock_ratio <= 0.2 else "Medium Stock" if stock_ratio <= 0.5 else "High Stock"
        st.write(f"**{item.capitalize()}**: {amount}/{max_amount} ({status})")
        st.progress(stock_ratio)

