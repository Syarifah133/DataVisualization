import os
import pandas as pd
import streamlit as st
from datetime import datetime
from utils import save_inventory, check_low_inventory, max_stock, inventory

def update_inventory_after_sale(sale_items):
    """
    Update inventory based on items sold.
    sale_items: A dictionary containing items and their quantities sold.
    """
    updated_inventory = inventory.copy()
    
    for item, quantity_sold in sale_items.items():
        if item in updated_inventory:
            updated_inventory[item] = max(updated_inventory[item] - quantity_sold, 0)  # Prevent negative stock
    
    inventory.update(updated_inventory)
    save_inventory(inventory)
    
    st.success("Inventory updated after sale.")

def display_inventory_management():
    """
    Display the Inventory Management page with update functionality and restocking alerts.
    """
    st.title("Inventory Management")
    st.write("### Current Inventory Levels:")

    # Display inventory with progress bars and color coding
    for item, amount in inventory.items():
        max_amount = max_stock[item]
        stock_ratio = min(amount / max_amount, 1.0)
        
        # Determine stock status and progress bar color
        if stock_ratio <= 0.2:
            status = "Low Stock"
            progress_color = "red"
        elif stock_ratio <= 0.5:
            status = "Medium Stock"
            progress_color = "orange"
        else:
            status = "High Stock"
            progress_color = "green"
        
        # Display item with progress bar
        st.markdown(f"<p style='font-weight: bold;'>{item.capitalize()} ({status}): {amount}/{max_amount}</p>", unsafe_allow_html=True)

        # Custom Progress Bar with Color
        progress_html = f"""
        <div style="background-color: #e0e0e0; border-radius: 5px; height: 20px; width: 100%;">
            <div style="background-color: {progress_color}; height: 100%; width: {stock_ratio*100}%; border-radius: 5px;"></div>
        </div>
        """
        st.markdown(progress_html, unsafe_allow_html=True)

    # Low inventory alerts
    st.subheader("Restock Alerts")
    low_items = check_low_inventory()

    if low_items:
        st.write("Items that need restocking:")
        for item in low_items:
            st.markdown(f"- <span style='color:red;'>{item.capitalize()}</span>", unsafe_allow_html=True)
    else:
        st.write("All items are well-stocked.")

    # Auto-generated restock list
    st.subheader("Auto-Generated Restock List")
    low_stock_items = {item: inventory[item] for item in inventory if inventory[item] <= 0.2 * max_stock[item]}
    
    if low_stock_items:
        st.write("The following items need restocking:")
        for item, quantity in low_stock_items.items():
            st.markdown(f"- <span style='color:red;'>{item.capitalize()}: {quantity}/{max_stock[item]}</span>", unsafe_allow_html=True)
    else:
        st.write("No items need restocking at the moment.")

    # Restocking Section (Manual update by Admin)
    st.subheader("Restock Items")
    updated_inventory = inventory.copy()
    for item in inventory.keys():
        restock_amount = st.number_input(f"Restock {item.capitalize()}", min_value=0, step=10, key=f"restock_{item}")
        if restock_amount:
            updated_inventory[item] += restock_amount

    if st.button("Update Inventory"):
        inventory.update(updated_inventory)
        save_inventory(inventory)
        st.success("Inventory updated successfully.")
        st.rerun()

    # Add Sale Integration
    st.subheader("Update Inventory After Sale")
    sale_items = {}
    for item in inventory.keys():
        quantity_sold = st.number_input(f"Quantity Sold of {item.capitalize()}", min_value=0, step=1, key=f"sale_{item}")
        if quantity_sold > 0:
            sale_items[item] = quantity_sold

    if st.button("Update Inventory After Sale"):
        if sale_items:
            update_inventory_after_sale(sale_items)
        else:
            st.error("No sales data entered. Please enter the sales quantities.")
