import streamlit as st
import pandas as pd
import os
import random
import datetime

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

    # Redeem voucher section
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("🎁 Redeem a Voucher")

    voucher_options = {
        "5% Off (10 Points)": {"discount": 5, "required_points": 10},
        "10% Off (100 Points)": {"discount": 10, "required_points": 100},
        "15% Off (150 Points)": {"discount": 15, "required_points": 150}
    }

    available_vouchers = {
        k: v for k, v in voucher_options.items() if st.session_state["loyalty_points"] >= v["required_points"]
    }

    if available_vouchers:
        selected_voucher = st.selectbox(
            "Select a voucher to redeem",
            options=list(available_vouchers.keys())
        )

        if st.button("Redeem Voucher"):
            voucher_details = available_vouchers[selected_voucher]
            st.session_state["loyalty_points"] -= voucher_details["required_points"]

            # Save the redeemed voucher as an active coupon
            # Save the redeemed voucher as an active coupon
            new_coupon = {
                "Coupon Code": f"{selected_voucher.split()[0].upper()}-{random.randint(1000, 9999)}",
                "Discount (%)": voucher_details["discount"],
                "Expiration Date": (datetime.datetime.now() + datetime.timedelta(days=30)).strftime('%Y-%m-%d'),
                "Active": True
            }

            # Update coupons.csv
            coupons_df = pd.read_csv('coupons.csv') if os.path.isfile('coupons.csv') else pd.DataFrame(columns=new_coupon.keys())
            new_coupon_df = pd.DataFrame([new_coupon])  # Convert the new coupon to a DataFrame
            coupons_df = pd.concat([coupons_df, new_coupon_df], ignore_index=True)  # Add the new coupon
            coupons_df.to_csv('coupons.csv', index=False)  # Save the updated DataFrame back to the CSV


            st.success(f"You have successfully redeemed a {voucher_details['discount']}% off voucher!")
            st.write(f"🎟️ Your voucher code is: `{new_coupon['Coupon Code']}`")
    else:
        st.info("You don't have enough points to redeem any vouchers at the moment.")

    # Show active coupons
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


    
