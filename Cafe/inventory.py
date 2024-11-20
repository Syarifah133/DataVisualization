import os
import pandas as pd
import streamlit as st
from datetime import datetime
from utils import save_inventory, check_low_inventory, max_stock, inventory_file, inventory

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

    # Display inventory with progress bars
    for item, amount in inventory.items():
        max_amount = max_stock[item]
        stock_ratio = min(amount / max_amount, 1.0)
        status = "Low Stock" if stock_ratio <= 0.2 else "Medium Stock" if stock_ratio <= 0.5 else "High Stock"
        st.write(f"**{item.capitalize()}** ({status}): {amount}/{max_amount}")
        st.progress(stock_ratio)

    # Low inventory alerts
    st.subheader("Restock Alerts")
    low_items = check_low_inventory()

    if low_items:
        st.write("Items that need restocking:")
        for item in low_items:
            st.markdown(f"- **{item.capitalize()}**")
    else:
        st.write("All items are well-stocked.")

    # Auto-generated restock list
    st.subheader("Auto-Generated Restock List")
    low_stock_items = {item: inventory[item] for item in inventory if inventory[item] <= 0.2 * max_stock[item]}
    
    if low_stock_items:
        st.write("The following items need restocking:")
        for item, quantity in low_stock_items.items():
            st.write(f"- **{item.capitalize()}**: {quantity}/{max_stock[item]}")
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
