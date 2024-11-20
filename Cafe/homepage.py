import streamlit as st
import pandas as pd
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

# Function to load active coupons
def load_active_coupons():
    coupons_df = pd.read_csv('coupons.csv') if os.path.exists('coupons.csv') else pd.DataFrame(columns=["Coupon Code", "Discount (%)", "Expiration Date", "Active"])
    return coupons_df[coupons_df['Active'] == True]  # Return only active coupons

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

    # Show active coupons with a beautiful design
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("🌟 Active Coupons Available for You!")

    active_coupons = load_active_coupons()
    if not active_coupons.empty:
        for _, row in active_coupons.iterrows():
            coupon_code = row['Coupon Code']
            discount = row['Discount (%)']
            expiration_date = row['Expiration Date']

            # Beautiful box for each coupon
            st.markdown(f"""
            <div style="background-color: #e0f7fa; padding: 20px; margin-bottom: 15px; border-radius: 10px; border-left: 5px solid #009688;">
                <h4 style="color: #00796b; font-size: 22px;">🎟️ <strong>{coupon_code}</strong></h4>
                <p style="font-size: 18px; color: #00796b;">**Discount**: {discount}% Off</p>
                <p style="font-size: 16px; color: #444;">**Expires On**: {expiration_date}</p>
                <div style="font-size: 18px; color: #388e3c;">
                    <strong>Active</strong> ✔️
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No active coupons available right now.")

    # Logout Button
    st.markdown("<hr>", unsafe_allow_html=True)
    if st.button("Log Out"):
        st.session_state.clear()  # Clear session state
        st.session_state["page"] = "Sign In"  # Redirect to Sign In
        st.success("You have logged out. Redirecting to Sign In...")
