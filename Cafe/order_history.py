import os
import pandas as pd
import streamlit as st

orders_file = 'orders.csv'

def display_order_history():
    st.title("Order History")
    if os.path.isfile(orders_file):
        orders_df = pd.read_csv(orders_file)
        st.dataframe(orders_df)
    else:
        st.info("No orders found.")
