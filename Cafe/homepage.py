import streamlit as st
import pandas as pd
import os
import random
from history import display_order_history
from order import display_order_page
from payment import display_payment_page

def logout():
    st.session_state.clear()  # Clears all session state variables (e.g., user_type, username)
    st.session_state["page"] = "Sign In"  # Redirect the user to the Sign In page
    st.rerun()

# Function to load loyalty data
def load_loyalty_data():
    if os.path.isfile('loyalty_points.csv'):
        return pd.read_csv('loyalty_points.csv')
    return pd.DataFrame(columns=['Username', 'Total Price', 'Redeem', 'Loyalty', 'Last Voucher'])


# Function to update loyalty data based on orders
def update_loyalty_points():
    loyalty_df = load_loyalty_data()

    # Load orders and calculate total spent by the user
    if os.path.isfile('orders.csv'):
        orders_df = pd.read_csv('orders.csv')
        total_spent = orders_df[orders_df['Username'] == st.session_state['username']]['Price'].sum()
    else:
        total_spent = 0

    # Check if the user exists in the loyalty data
    user_record = loyalty_df[loyalty_df['Username'] == st.session_state['username']]
    if not user_record.empty:
        # Update existing user's total price and loyalty points
        redeemed_points = user_record['Redeem'].iloc[0]
        loyalty_df.loc[loyalty_df['Username'] == st.session_state['username'], 'Total Price'] = total_spent
        loyalty_df.loc[loyalty_df['Username'] == st.session_state['username'], 'Loyalty'] = total_spent - redeemed_points
    else:
        # Create a new record for the user
        new_record = {
            'Username': st.session_state['username'],
            'Total Price': total_spent,
            'Redeem': 0,
            'Loyalty': total_spent,
            'Last Voucher': None
        }
        loyalty_df = pd.concat([loyalty_df, pd.DataFrame([new_record])], ignore_index=True)

    # Update session state
    st.session_state["loyalty_points"] = loyalty_df[loyalty_df['Username'] == st.session_state['username']]['Loyalty'].iloc[0]

    # Save the updated loyalty data
    loyalty_df.to_csv('loyalty_points.csv', index=False)


# Function to redeem a voucher
def redeem_voucher():
    if "loyalty_points" not in st.session_state:
        st.session_state["loyalty_points"] = 0

    # Voucher options based on loyalty points
    voucher_options = {
        "5% Off (10 Points)": {"discount": 5, "required_points": 10},
        "10% Off (100 Points)": {"discount": 10, "required_points": 100},
        "15% Off (150 Points)": {"discount": 15, "required_points": 150}
    }

    # Check for available vouchers
    available_vouchers = {
        k: v for k, v in voucher_options.items() if st.session_state["loyalty_points"] >= v["required_points"]
    }

    if available_vouchers:
        selected_voucher = st.selectbox("Select a voucher to redeem", options=list(available_vouchers.keys()))

        if st.button("Redeem Voucher"):
            voucher_details = available_vouchers[selected_voucher]
            required_points = voucher_details["required_points"]

            # Deduct points and update data
            st.session_state["loyalty_points"] -= required_points
            loyalty_df = load_loyalty_data()

            # Update user's record
            user_record = loyalty_df[loyalty_df['Username'] == st.session_state['username']]
            if not user_record.empty:
                current_redeem = user_record['Redeem'].iloc[0]
                new_redeem = current_redeem + required_points

                loyalty_df.loc[loyalty_df['Username'] == st.session_state['username'], 'Redeem'] = new_redeem
                loyalty_df.loc[loyalty_df['Username'] == st.session_state['username'], 'Loyalty'] = \
                    loyalty_df.loc[loyalty_df['Username'] == st.session_state['username'], 'Total Price'] - new_redeem
                loyalty_df.loc[loyalty_df['Username'] == st.session_state['username'], 'Last Voucher'] = selected_voucher
            else:
                # Create a new record if user not found
                new_record = {
                    'Username': st.session_state['username'],
                    'Total Price': 0,
                    'Redeem': required_points,
                    'Loyalty': st.session_state["loyalty_points"],
                    'Last Voucher': selected_voucher
                }
                loyalty_df = pd.concat([loyalty_df, pd.DataFrame([new_record])], ignore_index=True)

            # Save the updated loyalty data
            loyalty_df.to_csv('loyalty_points.csv', index=False)

            # Update session state for new loyalty points
            st.session_state["loyalty_points"] = loyalty_df[loyalty_df['Username'] == st.session_state['username']]['Loyalty'].iloc[0]

            # Success message for voucher redemption
            st.success(f"You have successfully redeemed a {voucher_details['discount']}% off voucher!")
            st.write(f"🎟️ Your voucher code is: `{selected_voucher.split()[0].upper()}-{random.randint(1000, 9999)}`")
            st.markdown(f"🎉 **Your new loyalty balance:** {st.session_state['loyalty_points']} points")
    else:
        st.info("You don't have enough points to redeem any vouchers at the moment.")


# Function to display the homepage
def display_homepage():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Go to", ["Homepage", "Order", "History"])

    if 'username' not in st.session_state:
        st.error("You need to sign in to access the homepage!")
        return

    username = st.session_state["username"]

    if page == "Homepage":
        st.subheader(f"Welcome back, {username}!")

        # Update loyalty points based on previous orders
        update_loyalty_points()

        # Display loyalty points
        st.markdown(f"""
        <div style="background-color: #f0f8ff; padding: 10px; border-radius: 5px;">
            <h3 style="color: #4CAF50;">🎉 You have <strong>{int(st.session_state['loyalty_points'])}</strong> loyalty points</h3>
            <p style="font-size: 18px;">Keep earning points with each purchase to redeem awesome rewards!</p>
        </div>
        """, unsafe_allow_html=True)

        # Redeem a voucher section
        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("🎁 Redeem a Voucher")

        # Redeem voucher functionality
        redeem_voucher()

    elif page == "Order":
        display_order_page(username)

    elif page == "History":
        display_order_history()

    if st.sidebar.button('Logout'):
        logout()  # Call the logout function when the button is clicked