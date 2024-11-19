import streamlit as st
import pandas as pd
import os
import datetime

def display_order_history():
    st.title("Order History")
    
    # Load orders.csv
    if os.path.isfile("orders.csv"):
        orders_df = pd.read_csv("orders.csv")
    else:
        st.warning("No order history found.")
        return

    # Load feedback.csv
    feedback_df = pd.read_csv("feedback.csv") if os.path.isfile("feedback.csv") else pd.DataFrame()

    username = st.session_state.get("username", "Guest")
    user_orders = orders_df[orders_df["Username"] == username]

    if user_orders.empty:
        st.warning("No orders found for your account.")
        return

    for _, order in user_orders.iterrows():
        st.subheader(f"Order #{order['Booking Number']}")
        st.write(f"**Coffee Type**: {order['Coffee Type']} - **Price**: ${order['Price']}")
        st.write(f"**Size**: {order['Size']} | **Ice**: {order['Ice']} | **Sugar**: {order['Sugar']}")
        if order['Add-ons']:
            st.write(f"**Add-ons**: {order['Add-ons']}")
        st.write(f"**Order Time**: {order['Order Time']}")

        # Check if feedback already exists
        existing_feedback = feedback_df[
            (feedback_df["Username"] == username) & 
            (feedback_df["Booking Number"] == order["Booking Number"])
        ]

        if not existing_feedback.empty:
            # st.info("You have already rated this order.")
            st.write(f"**Rating**: {'⭐' * int(existing_feedback.iloc[0]['Rating'])}")
            st.info(f"**Comments**: {existing_feedback.iloc[0]['Feedback']}")
        else:
            # Rating using star buttons
            st.write("Rate this order:")
            stars = st.radio(
                "Select Rating", [1, 2, 3, 4, 5], format_func=lambda x: "⭐" * x, key=f"rating_{order['Booking Number']}"
            )
            feedback = st.text_area("Leave a comment:", key=f"comments_{order['Booking Number']}")
            submit_feedback = st.button(f"Submit Feedback for Order #{order['Booking Number']}", key=f"submit_{order['Booking Number']}")

            if submit_feedback:
                # Save feedback to CSV
                feedback = {
                    "Username": username,
                    "Booking Number": order["Booking Number"],
                    "Coffee Type": order["Coffee Type"],
                    "Rating": stars,
                    "Comments": feedback,
                    "Feedback Time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }

                feedback_df = pd.DataFrame([feedback])
                if not os.path.isfile("feedback.csv"):
                    feedback_df.to_csv("feedback.csv", index=False)
                else:
                    feedback_df.to_csv("feedback.csv", mode="a", header=False, index=False)

                st.success("Thank you for your feedback!")


