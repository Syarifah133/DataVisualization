import csv
import os
from datetime import datetime
import streamlit as st

# Path to the CSV file that stores notifications
NOTIFICATION_FILE = "user_notifications.csv"

# Function to read notifications from CSV
def read_notifications():
    notifications = {}
    if os.path.exists(NOTIFICATION_FILE):
        with open(NOTIFICATION_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                username = row[0]
                notification_msg = row[1]
                if username not in notifications:
                    notifications[username] = []
                notifications[username].append(notification_msg)
    return notifications

# Function to save a notification to CSV
def save_notification(username, notification_msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(NOTIFICATION_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, notification_msg, timestamp])

# Function to clear notifications for a specific user
def clear_notifications(username):
    notifications = read_notifications()  # Read current notifications
    updated_notifications = {key: [] for key in notifications.keys()}  # Initialize empty list for each user

    # Overwrite the CSV with cleared notifications for the user
    with open(NOTIFICATION_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        for user, msgs in notifications.items():
            if user != username:
                for msg in msgs:
                    writer.writerow([user, msg, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    return "Notifications cleared!"

# Function to display notifications in the sidebar for a user
def display_user_notifications(username):
    """
    Display notifications for the user in the sidebar.

    Args:
        username (str): The username of the user.
    """
    st.sidebar.subheader(f"🔔 Notifications for {username}")
    notifications = get_notifications(username)

    if notifications:
        for notification in notifications:
            st.sidebar.info(notification)

        # Clear notifications button
        if st.sidebar.button("Clear Notifications", key=f"clear_{username}"):
            clear_notifications(username)
            st.sidebar.success("Notifications cleared!")
    else:
        st.sidebar.info("No notifications at the moment.")

# Function to retrieve notifications for a user (modified for admin to get only the latest)
def get_notifications(username):
    """
    Retrieve notifications for a specific user from the CSV file.

    Args:
        username (str): The username of the user.

    Returns:
        list: A list of notifications for the user.
    """
    notifications = read_notifications()
    if username == 'admin' and username in notifications:
        # For admin, return only the latest notification
        return [notifications['admin'][-1]]  # Return the latest notification
    return notifications.get(username, [])  # For other users, return all their notifications

# Function to add a notification for a user
def add_notification(username, notification_msg):
    """
    Add a notification for a specific user.

    Args:
        username (str): The username of the user.
        notification_msg (str): The notification message to add.
    """
    notifications = get_notifications(username)
    # If notification is not already present, add it
    if notification_msg not in notifications:
        save_notification(username, notification_msg)  # Save new notification to CSV
    else:
        print(f"Duplicate notification for {username} not added: {notification_msg}")
    save_notification(username, notification_msg)  # Save notification to CSV

# Function to display the customer sidebar with navigation and notifications
def display_cust_sidebar(username):
    """
    Display the customer sidebar with navigation and user-specific notifications.

    Args:
        username (str): The username of the current user.
    """
    st.sidebar.title("Navigation")

    # Create a unique key for the selectbox to prevent conflicts
    page = st.sidebar.selectbox("Go to", ["Homepage", "Order", "History"], key=f"nav_{username}")

    # Display the notifications for the specific user
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    display_user_notifications(username)  # Pass the username to display user-specific notifications

    return page

# Function to display admin notifications and manage them (only latest for admin)
def display_admin_notifications(username):
    """
    Display admin notifications and manage them
    """
    # Display the latest notification for the admin
    st.sidebar.subheader("🔔 Admin Notifications")
    admin_notifications = get_notifications('admin')

    if admin_notifications:
        st.sidebar.info(admin_notifications[0])  # Show only the latest notification

        # Admin can clear notifications
        if st.sidebar.button("Clear Admin Notifications", key=f"clear_admin"):
            clear_notifications('admin')
            st.sidebar.success("Admin Notifications cleared!")
    else:
        st.sidebar.info("No admin notifications.")

# Main function to run the app
def main():
    # Simulate a login or user type assignment
    username = st.text_input("Enter your username:", "admin")  # Simulating user input (admin or any user)
    
    if username == 'admin':
        display_admin_notifications(username)  # Show notifications for admin
        st.write("Admin Dashboard")
    else:
        display_cust_sidebar(username)  # Show sidebar for customers
    
    # Example of adding a new notification
    if st.button("Add Notification for Admin"):
        add_notification('admin', "New notification for admin.")

    if st.button("Add Notification for User"):
        add_notification(username, "New notification for user.")

if __name__ == "__main__":
    main()
