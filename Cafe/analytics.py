import os
import pandas as pd
import streamlit as st
from datetime import datetime

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

# Custom function to render a progress bar with color
def colored_progress_bar(ratio, color):
    """ Renders a colored progress bar using HTML and CSS """
    st.markdown(
        f"""
        <div style="background-color: #f0f0f0; border-radius: 5px; width: 100%; height: 20px;">
            <div style="background-color: {color}; width: {ratio * 100}%; height: 100%; border-radius: 5px;"></div>
        </div>
        """,
        unsafe_allow_html=True
    )

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
    with st.expander("Current Orders & Sales", expanded=True):
        st.subheader("Orders in 'Preparing' Status")

        # Filter the orders that are in "Preparing" status
        preparing_orders = orders_df[orders_df['Status'] == 'Preparing']
        
        if preparing_orders.empty:
            st.info("No orders are currently in 'Preparing' status.")
        else:
            st.dataframe(preparing_orders[['Order Time', 'Coffee Type', 'Price', 'Status']])

    # Real-Time Sales Summary
    st.markdown("### Real-Time Sales Summary")
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
    with st.expander("Current Inventory Levels", expanded=True):
        st.subheader("Inventory Levels")

        for item, amount in inventory.items():
            max_amount = max_stock[item]
            stock_ratio = min(amount / max_amount, 1.0)
            status = "Low Stock" if stock_ratio <= 0.2 else "Medium Stock" if stock_ratio <= 0.5 else "High Stock"
            
            # Color logic for progress bar
            color = 'red' if stock_ratio <= 0.2 else 'orange' if stock_ratio <= 0.5 else 'green'
            st.write(f"**{item.capitalize()}**: {amount}/{max_amount} ({status})")
            
            # Displaying the colored progress bar
            colored_progress_bar(stock_ratio, color)

    # Display the order status options
    st.subheader("Update Order Status")
    order_id = st.number_input("Enter Order ID to Update", min_value=1)
    if order_id:
        new_status = st.selectbox("Select New Order Status", ['Preparing', 'Ready for Pickup', 'Done'])
        if st.button("Update Status"):
            orders_df.loc[orders_df['Booking Number'] == order_id, 'Status'] = new_status
            orders_df.to_csv(orders_file, index=False)
            st.success(f"Order #{order_id} status updated to {new_status}.")
