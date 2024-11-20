import random
import streamlit as st
import pandas as pd
import datetime
import os
from history import display_order_history
from homepage import display_homepage

# Function to load and filter active coupons
def load_active_coupons(file_path='coupons.csv'):
    if os.path.isfile(file_path):
        coupons_df = pd.read_csv(file_path)
        today = datetime.date.today()
        coupons_df['Expiration Date'] = pd.to_datetime(coupons_df['Expiration Date']).dt.date
        active_coupons = coupons_df[
            (coupons_df['Active'] == True) & 
            (coupons_df['Expiration Date'] >= today)
        ]
        return active_coupons
    else:
        return pd.DataFrame(columns=['Coupon Code', 'Discount (%)', 'Expiration Date', 'Active'])

# Function to mark a coupon as used
def mark_coupon_as_used(coupon_code, file_path='coupons.csv'):
    if os.path.isfile(file_path):
        coupons_df = pd.read_csv(file_path)
        if coupon_code in coupons_df['Coupon Code'].values:
            coupons_df.loc[coupons_df['Coupon Code'] == coupon_code, 'Active'] = False
            coupons_df.to_csv(file_path, index=False)

# Function to display the order page
def display_order_page(username):
    # Sidebar Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Order", "History", "Homepage"])

    # Navigate based on sidebar selection
    if page == "Order":
        # Display Order Page
        st.title(f"Welcome, {username}!")
        st.header("Menu")

        # Coffee menu with prices
        menu = {
            'Americano': 2.5,
            'Cappuccino': 3.0,
            'Latte': 3.5,
            'Caramel Macchiato': 4.0
        }
        st.write(pd.DataFrame(list(menu.items()), columns=['Coffee Type', 'Price ($)']))

        # Branch Selection Dropdown
        branches = ['Seri Iskandar', 'Ipoh', 'Manjung']
        selected_branch = st.selectbox("Select Branch", branches)
        st.write(f"**Selected Branch:** {selected_branch}")

        # Load active coupons
        active_coupons = load_active_coupons()
        if not active_coupons.empty:
            coupon_options = active_coupons['Coupon Code'].tolist()
        else:
            coupon_options = ["No Coupons Available"]

        # Function to save orders to CSV
        def save_order_to_csv(order):
            if not os.path.isfile('orders.csv'):
                df = pd.DataFrame([order])
                df.to_csv('orders.csv', index=False)
            else:
                df = pd.DataFrame([order])
                df.to_csv('orders.csv', mode='a', header=False, index=False)

        # Order placement form
        with st.form(key='order_form'):
            coffee_type = st.selectbox("Select Coffee", list(menu.keys()))
            size = st.radio("Select Size", ['Small', 'Medium', 'Large'])
            ice = st.radio("Choice of Ice", ['Hot', 'Less', 'Normal'])
            sugar = st.radio("Choice of Sugar", ['No', 'Less', 'Normal'])
            add_ons = st.multiselect("Add-ons", ['Milk', 'Whipped Cream', 'Shot'])

            # Coupon selection
            selected_coupon = st.selectbox("Choose Coupon (Optional)", coupon_options)

            submit_order = st.form_submit_button("Place Order")

            if submit_order:
                # Calculate base price
                price = menu[coffee_type]

                # Apply discount if a valid coupon is selected
                if selected_coupon != "No Coupons Available":
                    discount_row = active_coupons[active_coupons['Coupon Code'] == selected_coupon]
                    discount_percentage = discount_row['Discount (%)'].values[0]
                    original_price = price
                    price *= (1 - discount_percentage / 100)
                    st.write(f"Coupon `{selected_coupon}` applied! Discount: {discount_percentage}%")
                    st.write(f"**Original Price:** ${original_price:.2f}")
                    st.write(f"**Price After Discount:** ${price:.2f}")

                    # Mark coupon as used
                    mark_coupon_as_used(selected_coupon)
                else:
                    st.write("No coupon applied.")
                    st.write(f"**Price:** ${price:.2f}")

                # Generate other order details
                booking_number = str(random.randint(1000, 9999))
                prep_time = random.randint(5, 15)  # Random prep time between 5 to 15 minutes
                order_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Creating the order dictionary 
                order = {
                    'Username': username,
                    'Coffee Type': coffee_type,
                    'Size': size,
                    'Ice': ice,
                    'Sugar': sugar,
                    'Add-ons': ', '.join(add_ons),
                    'Price ($)': f"{price:.2f}",  # Including discounted price
                    'Booking Number': booking_number,
                    'Preparation Time (min)': prep_time,
                    'Order Time': order_time,
                    'Branch': selected_branch,
                    'Coupon': selected_coupon,
                    'Status': 'Preparing'
                }

                # Save the order to CSV
                save_order_to_csv(order)

                # Show success message to the user
                st.success(f"Order placed! Your booking number is {booking_number}. Estimated preparation time is {prep_time} minutes.")

    elif page == "History":
        # Display Order History Page
        display_order_history()

    elif page == "Homepage":
        # Display Homepage
        display_homepage()
