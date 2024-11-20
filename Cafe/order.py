import streamlit as st
import pandas as pd
import random
import datetime
import os
from history import display_order_history  # Import the history function
from homepage import display_homepage  # Import the homepage function

# Function to display the order page
def display_order_page(username):
    # Sidebar Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Order", "History", "Homepage"])

    # Initialize a variable for the selected branch
    selected_branch = None

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
        branches = ['Seri Iskandar', 'Ipoh', 'Manjung']  # List of branches
        selected_branch = st.selectbox("Select Branch", branches)
        st.write(f"**Selected Branch:** {selected_branch}")

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
            submit_order = st.form_submit_button("Place Order")

            if submit_order:
                price = menu[coffee_type]  # Fetch the price of the selected coffee type
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
                    'Price ($)': price,  # Including price in the order
                    'Booking Number': booking_number,
                    'Preparation Time (min)': prep_time,
                    'Order Time': order_time,
                    'Branch': selected_branch,  # Including the selected branch
                    'Status': 'Preparing'  # Initial status set to "Preparing"
                }

                # Save the order to CSV
                save_order_to_csv(order)
                
                # Show success message to the user
                st.success(f"Order placed! Your booking number is {booking_number}. Estimated preparation time is {prep_time} minutes.")
    
    elif page == "History":
        # Display Order History Page (Functionality to show past orders)
        display_order_history()  # Pass the username and selected branch to the history page

    elif page == "Homepage":
        # Display Homepage (Simple display)
        display_homepage()
