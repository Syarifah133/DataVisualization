import os
import pandas as pd
import streamlit as st

orders_file = 'orders.csv'

def display_order_history():
    st.title("Order History")
    
    # Load orders.csv if it exists
    if os.path.isfile(orders_file):
        orders_df = pd.read_csv(orders_file)
    else:
        st.info("No orders found.")
        return

    # Display order history in a table
    st.write("### Order History")
    st.dataframe(orders_df)

    # Loop through each order and allow user to change its status
    for index, order in orders_df.iterrows():
        order_id = order['Booking Number']
        current_status = order.get('Status', 'Preparing')  # Default status if missing

        st.subheader(f"Order #{order_id}")
        st.write(f"**Coffee Type**: {order['Coffee Type']}")
        st.write(f"**Username**: {order['Username']}")
        st.write(f"**Branch**: {order['Branch']}")
        st.write(f"**Order Time**: {order['Order Time']}")
        st.write(f"**Current Status**: {current_status}")

        # Dropdown to change the order status
        new_status = st.selectbox(
            f"Update status for Order #{order_id}",
            ['Preparing', 'Ready for Pickup', 'Done'],
            index=['Preparing', 'Ready for Pickup', 'Done'].index(current_status),
            key=f"status_{order_id}"
        )

        # If the user submits the change
        if st.button(f"Update Status for Order #{order_id}", key=f"update_{order_id}"):
            # Update the status in the DataFrame
            orders_df.loc[orders_df['Booking Number'] == order_id, 'Status'] = new_status
            # Save the updated DataFrame back to CSV
            orders_df.to_csv(orders_file, index=False)
            st.success(f"Order #{order_id} status updated to {new_status}.")

