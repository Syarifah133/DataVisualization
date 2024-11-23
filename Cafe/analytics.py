import os
import pandas as pd
import streamlit as st
from datetime import datetime

# Define the path to your orders and inventory files
inventory_file = 'inventory.csv'  # Make sure your inventory data is stored in a CSV or other format
orders_file='orders.csv'
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

    # Radio button for page selection
    page_option = st.radio("Choose Report Type", ['Sales Trends', 'Inventory Health', 'Order Management'])

    # Load the order data
    orders_df = load_orders()
    
    if orders_df.empty:
        st.info("No sales data found. Please add orders to view analytics.")
        return

    # Display the appropriate section based on page option
    if page_option == 'Sales Trends':
        st.subheader("Sales Trend (Daily)")
        orders_df['Date'] = orders_df['Order Time'].dt.date
        sales_by_date = orders_df.groupby('Date').agg(Quantity=('Price', 'count'), Revenue=('Price', 'sum'))
        st.dataframe(sales_by_date)
        st.line_chart(sales_by_date)

        st.subheader("Revenue Trend (Weekly)")
        orders_df['Week'] = orders_df['Order Time'].dt.to_period('W')
        revenue_by_week = orders_df.groupby('Week').agg(Revenue=('Price', 'sum'))
        st.dataframe(revenue_by_week)
        st.line_chart(revenue_by_week)

        # **Revenue Trend (Monthly)**
        st.subheader("Revenue Trend (Monthly)")
        orders_df['Month'] = orders_df['Order Time'].dt.to_period('M')
        revenue_by_month = orders_df.groupby('Month').agg(Revenue=('Price', 'sum'))
        st.dataframe(revenue_by_month)
        st.line_chart(revenue_by_month)
        

    elif page_option == 'Inventory Health':
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

    elif page_option == 'Order Management':
        st.subheader("Real-Time Orders & Sales")
        
        # Filter Orders based on user input
        order_status = st.selectbox("Select Order Status", ['Preparing', 'Ready for Pickup', 'Done'])
        filtered_orders = orders_df[orders_df['Status'] == order_status]

        if filtered_orders.empty:
            st.info(f"No orders found with status: {order_status}")
        else:
            st.dataframe(filtered_orders[['Order Time', 'Coffee Type', 'Price', 'Status']])

        # Update Order Status
        st.subheader("Update Order Status")
        order_id = st.number_input("Enter Order ID to Update", min_value=1)
        if order_id:
            new_status = st.selectbox("Select New Order Status", ['Preparing', 'Ready for Pickup', 'Done'])
            if st.button("Update Status"):
                orders_df.loc[orders_df['Booking Number'] == order_id, 'Status'] = new_status
                orders_df.to_csv(orders_file, index=False)
                st.success(f"Order #{order_id} status updated to {new_status}.")

# Run the function to display the dashboard
