import streamlit as st
from admin import display_admin_page
from getStarted import display_get_started
from payment import display_payment_page
from signin import display_sign_in
from signUp import display_sign_up
from order import display_order_page
from homepage import display_homepage

# Initialize session state
if "page" not in st.session_state:
    st.session_state["page"] = "Get Started"

if "user_type" not in st.session_state:
    st.session_state["user_type"] = None  # Initialize user type as None

# Navigation
if st.session_state["page"] == "Get Started":
    display_get_started()
elif st.session_state["page"] == "Sign In":
    display_sign_in()
elif st.session_state["page"] == "Sign Up":
    display_sign_up()
elif st.session_state["page"] == "Homepage":
    display_homepage()
elif st.session_state["page"] == "Order":
    if "username" in st.session_state:
        display_order_page(st.session_state["username"])
    else:
        st.error("Please sign in first!")
        st.session_state["page"] = "Sign In"
elif st.session_state["page"] == "Admin":
    if st.session_state["user_type"] == "admin":
        display_admin_page()


elif st.session_state.page == "payment" and 'order' in st.session_state and st.session_state.order is not None:

    display_payment_page(
        username=st.session_state.order['Username'],
        order_details=st.session_state.order,
        total_price=float(st.session_state.order['Price ($)']),
        branch=st.session_state.order['Branch'],
        payment_method=st.session_state.order['Method'],
        booking_number=st.session_state.order['Booking Number'],
        prep_time=st.session_state.order['Preparation Time (min)']
    )
   
