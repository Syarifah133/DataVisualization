import streamlit as st
import pandas as pd
from datetime import date

coupon_file = 'coupons.csv'
user_file = 'users.csv'  # Path to your users file

# Function to load existing coupons
def load_coupons():
    if not pd.io.common.file_exists(coupon_file):
        return pd.DataFrame(columns=["Coupon Code", "Discount (%)", "Expiration Date", "Active", "Username"])
    return pd.read_csv(coupon_file)

# Function to save coupons to a CSV file
def save_coupons(coupons_df):
    coupons_df.to_csv(coupon_file, index=False)

# Function to create a new coupon for all users with username="all"
def create_coupon_for_all_users(coupon_code, discount, expiration_date, username="all"):
    coupons_df = load_coupons()
    
    # Check if coupon already exists
    if coupon_code in coupons_df['Coupon Code'].values:
        st.error("Coupon code already exists!")
        return
    
    # Create a new coupon entry with "all" as the username
    new_coupon = pd.DataFrame({
        "Coupon Code": [coupon_code],
        "Discount (%)": [discount],
        "Expiration Date": [expiration_date],
        "Active": [True],
        "Username": [username]  # Assign the coupon to the "all" username
    })
    
    # Add the new coupon to the dataframe
    coupons_df = pd.concat([coupons_df, new_coupon], ignore_index=True)
    save_coupons(coupons_df)
    st.success(f"Coupon '{coupon_code}' created for all users successfully!")

# Function to deactivate a coupon
def deactivate_coupon(coupon_code):
    coupons_df = load_coupons()
    if coupon_code in coupons_df['Coupon Code'].values:
        coupons_df.loc[coupons_df['Coupon Code'] == coupon_code, 'Active'] = False
        save_coupons(coupons_df)
        st.success(f"Coupon '{coupon_code}' deactivated successfully!")
        st.experimental_rerun()  # Rerun the app to update coupon status
    else:
        st.error("Coupon code not found!")

# Function to display and manage coupons
def display_promotions_page():
    st.title("Promotions & Discounts")
    
    # Show the existing coupons
    coupons_df = load_coupons()
    st.subheader("Existing Coupons")
    st.dataframe(coupons_df)
    
    # Create a new coupon
    st.subheader("Create New Coupon")
    
    # Add unique keys for the input fields to prevent DuplicateWidgetID error
    coupon_code = st.text_input("Coupon Code", key="coupon_code_input")  # Unique key
    discount = st.number_input("Discount (%)", min_value=1, max_value=100, value=10, key="discount_input")  # Unique key
    expiration_date = st.date_input("Expiration Date", key="expiration_date_input")  # Unique key
    
    if st.button("Create Coupon", key="create_coupon_button"):  # Unique key
        if coupon_code:
            create_coupon_for_all_users(coupon_code, discount, expiration_date)
        else:
            st.error("Please enter a coupon code.")
    
    # Deactivate a coupon
    st.subheader("Deactivate Coupon")
    deactivate_code = st.text_input("Coupon Code to Deactivate", key="deactivate_code_input")  # Unique key
    
    if st.button("Deactivate Coupon", key="deactivate_coupon_button"):  # Unique key
        if deactivate_code:
            deactivate_coupon(deactivate_code)
        else:
            st.error("Please enter a coupon code to deactivate.")
