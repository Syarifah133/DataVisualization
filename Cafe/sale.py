import streamlit as st

def display_sales_page(username):
    st.title("Sales Dashboard")
    st.subheader(f"Welcome, Admin {username}!")

    # Example content for Sales Page
    st.write("This is the admin sales dashboard. You can view sales data here.")
    st.write("Feature ideas: Total sales, daily revenue, product performance, etc.")
