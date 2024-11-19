import streamlit as st
from getStarted import display_get_started
from signin import display_sign_in
from signUp import display_sign_up
from order import display_order_page
from sale import display_sales_page

# Initialize session state
if "page" not in st.session_state:
    st.session_state["page"] = "Get Started"

# Navigation
if st.session_state["page"] == "Get Started":
    display_get_started()
elif st.session_state["page"] == "Sign In":
    display_sign_in()
elif st.session_state["page"] == "Sign Up":
    display_sign_up()
elif st.session_state["page"] == "Order":
    if "username" in st.session_state:
        display_order_page(st.session_state["username"])
    else:
        st.error("Please sign in first!")
        st.session_state["page"] = "Sign In"
        
elif st.session_state["page"] == "Sales":
    if "username" in st.session_state:
        display_sales_page(st.session_state["username"])
    else:
        st.error("Please sign in first!")
        st.session_state["page"] = "Sign In"
        
