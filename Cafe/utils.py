import os
import pandas as pd

inventory_file = 'inventory.csv'

# Load inventory
if os.path.isfile(inventory_file):
    inventory = pd.read_csv(inventory_file).to_dict('records')[0]
else:
    inventory = {
        'coffee_beans': 50,
        'milk': 40,
        'sugar': 5,
        'cups': 5
    }

max_stock = {
    'coffee_beans': 1000,
    'milk': 500,
    'sugar': 200,
    'cups': 50
}

# Save inventory
def save_inventory(inventory_data):
    pd.DataFrame([inventory_data]).to_csv(inventory_file, index=False)

# Check low inventory
def check_low_inventory():
    return {item: amount for item, amount in inventory.items() if amount < 0.2 * max_stock[item]}
