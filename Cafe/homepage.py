import streamlit as st
import random
import pandas as pd
from datetime import datetime
import os

# Function to calculate and update loyalty points based on order total
def update_loyalty_points():
    if "loyalty_points" not in st.session_state:
        st.session_state["loyalty_points"] = 0  # Initialize loyalty points if not present

    # Load order history from CSV or session (assuming orders.csv has a 'Price' column)
    if os.path.isfile('orders.csv'):
        orders_df = pd.read_csv('orders.csv')
        total_spent = orders_df[orders_df['Username'] == st.session_state['username']]['Price'].sum()
    else:
        total_spent = 0

    # Each $1 spent gives 1 loyalty point
    loyalty_points = int(total_spent)
    st.session_state["loyalty_points"] = loyalty_points

# Function to display the homepage
def display_homepage():
    st.title("Homepage")

    if 'username' not in st.session_state:
        st.error("You need to sign in to access the homepage!")
        return

    username = st.session_state["username"]
    st.subheader(f"Welcome back, {username}!")

    # Update loyalty points based on previous orders
    update_loyalty_points()

    # Beautifully display loyalty points
    st.markdown(f"""
    <div style="background-color: #f0f8ff; padding: 10px; border-radius: 5px;">
        <h3 style="color: #4CAF50;">🎉 You have <strong>{st.session_state['loyalty_points']}</strong> loyalty points</h3>
        <p style="font-size: 18px;">Keep earning points with each purchase to redeem awesome rewards!</p>
    </div>
    """, unsafe_allow_html=True)

    # Daily Special Offers in a Beautiful Box
    offers = [
        "Buy 1 Get 1 Free on Cappuccinos",
        "20% Off All Lattes",
        "Free Extra Shot with Americano",
        "Free Whipped Cream Topping on Caramel Macchiato"
    ]
    daily_offer = offers[datetime.now().weekday() % len(offers)]  # Rotate offers daily

    # Add some spacing and visuals for a nicer design
    st.markdown("<hr>", unsafe_allow_html=True)
    # Beautiful box for Daily Special Offer
    st.markdown(f"""
    <div style="background-color: #ffebcd; padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #ff9800;">
        <h3 style="color: #ff9800; font-size: 24px;">🎉 **Today's Special Offer**</h3>
        <p style="font-size: 20px; color: #555;">{daily_offer}</p>
    </div>
    """, unsafe_allow_html=True)

    # # Logout Button
    st.markdown("<hr>", unsafe_allow_html=True)
    if st.button("Log Out"):
        st.session_state.clear()  # Clear session state
        st.session_state["page"] = "Sign In"  # Redirect to Sign In
        st.success("You have logged out. Redirecting to Sign In...")
