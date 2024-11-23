import streamlit as st

# Function to display notifications in the sidebar
def display_user_notifications(username):
    st.sidebar.subheader(f"🔔 Notifications for {username}")

    # Initialize user-specific notifications if not already done
    if "user_notifications" not in st.session_state:
        st.session_state["user_notifications"] = {}

    # Ensure the current user has an entry in the session state
    if username not in st.session_state["user_notifications"]:
        st.session_state["user_notifications"][username] = []

    # Display notifications
    if st.session_state["user_notifications"][username]:
        for notification in st.session_state["user_notifications"][username]:
            st.sidebar.info(notification)

        # Clear notifications button
        if st.sidebar.button("Clear Notifications"):
            st.session_state["user_notifications"][username] = []
            st.sidebar.success("Notifications cleared.")
    else:
        st.sidebar.info("No notifications at the moment.")

# Function to add notifications to the user
def add_notification(username, notification_msg):
    # Initialize user-specific notifications if not already done
    if "user_notifications" not in st.session_state:
        st.session_state["user_notifications"] = {}

    # Ensure the current user has an entry in the session state
    if username not in st.session_state["user_notifications"]:
        st.session_state["user_notifications"][username] = []  # Initialize the notifications list for the user

    # Add the notification to the corresponding user's notification list
    st.session_state["user_notifications"][username].append(notification_msg)

# Function to display the customer sidebar with navigation and notifications
def display_cust_sidebar(username):
    """
    Display the customer sidebar with navigation and user-specific notifications.

    Args:
        username (str): The username of the current user.
    """
    st.sidebar.title("Navigation")

    # Create a unique key for the selectbox based on username to prevent key conflicts
    page = st.sidebar.selectbox("Go to", ["Homepage", "Order", "History"] )


    # Display the notifications for the specific user
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    display_user_notifications(username)  # Pass the username to display user-specific notifications

    return page
