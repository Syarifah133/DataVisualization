import os
import pandas as pd
import streamlit as st
from utils import save_inventory, check_low_inventory, max_stock, inventory_file, inventory

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

    # Restocking Section
    st.subheader("Restock Items")
    updated_inventory = inventory.copy()
    for item in inventory.keys():
        restock_amount = st.number_input(f"Restock {item}", min_value=0, step=10, key=f"restock_{item}")
        if restock_amount:
            updated_inventory[item] += restock_amount

    if st.button("Update Inventory"):
        inventory.update(updated_inventory)
        save_inventory(inventory)
        st.success("Inventory updated successfully.")
        st.rerun()
