import streamlit as st
import pandas as pd
import random
import datetime
import os
from history import display_order_history
from homepage import display_homepage

# def display_order_page(username):
#     # Sidebar Navigation
#     st.sidebar.title("Navigation")
#     page = st.sidebar.radio("Go to", ["Order", "History", "Homepage"])

#     # Navigate based on sidebar selection
#     if page == "Order":
#         # Display Order Page
#         st.title(f"Welcome, {username}!")
#         st.header("Menu")
#         menu = {
#             'Americano': 2.5,
#             'Cappuccino': 3.0,
#             'Latte': 3.5,
#             'Caramel Macchiato': 4.0
#         }
#         st.write(pd.DataFrame(list(menu.items()), columns=['Coffee Type', 'Price ($)']))

#         # Function to save orders to CSV
#         def save_order_to_csv(order):
#             if not os.path.isfile('orders.csv'):
#                 df = pd.DataFrame([order])
#                 df.to_csv('orders.csv', index=False)
#             else:
#                 df = pd.DataFrame([order])
#                 df.to_csv('orders.csv', mode='a', header=False, index=False)

#         # Order placement form
#         with st.form(key='order_form'):
#             coffee_type = st.selectbox("Select Coffee", list(menu.keys()))
#             size = st.radio("Select Size", ['Small', 'Medium', 'Large'])
#             ice = st.radio("Choice of Ice", ['Hot','Less','Normal'])
#             sugar = st.radio("Choice of Sugar", ['No','Less','Normal'])
#             add_ons = st.multiselect("Add-ons", ['Milk', 'Whipped Cream', 'Shot'])
#             submit_order = st.form_submit_button("Place Order")

#             if submit_order:
#                 booking_number = str(random.randint(1000, 9999))
#                 prep_time = random.randint(5, 15)
#                 order_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#                 order = {
#                     'Username': username,
#                     'Coffee Type': coffee_type,
#                     'Size': size,
#                     'Ice': ice,
#                     'Sugar': sugar,
#                     'Add-ons': ', '.join(add_ons),
#                     'Booking Number': booking_number,
#                     'Preparation Time (min)': prep_time,
#                     'Order Time': order_time
#                 }

#                 save_order_to_csv(order)
#                 st.success(f"Order placed! Your booking number is {booking_number}. Estimated preparation time is {prep_time} minutes.")
#     elif page == "History":
#         # Display Order History Page
#         display_order_history()
#     elif page == "Homepage":
#         # Display Homepage
#         display_homepage()

def display_order_page(username):
    # Sidebar Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Order", "History", "Homepage"])

    # Navigate based on sidebar selection
    if page == "Order":
        # Display Order Page
        st.title(f"Welcome, {username}!")
        st.header("Menu")
        menu = {
            'Americano': 2.5,
            'Cappuccino': 3.0,
            'Latte': 3.5,
            'Caramel Macchiato': 4.0
        }
        st.write(pd.DataFrame(list(menu.items()), columns=['Coffee Type', 'Price ($)']))

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
                prep_time = random.randint(5, 15)
                order_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                order = {
                    'Username': username,
                    'Coffee Type': coffee_type,
                    'Size': size,
                    'Ice': ice,
                    'Sugar': sugar,
                    'Add-ons': ', '.join(add_ons),
                    'Price ($)': price,  # Include the price in the order
                    'Booking Number': booking_number,
                    'Preparation Time (min)': prep_time,
                    'Order Time': order_time
                }

                save_order_to_csv(order)
                st.success(f"Order placed! Your booking number is {booking_number}. Estimated preparation time is {prep_time} minutes.")
    elif page == "History":
        # Display Order History Page
        display_order_history()
    elif page == "Homepage":
        # Display Homepage
        display_homepage()
