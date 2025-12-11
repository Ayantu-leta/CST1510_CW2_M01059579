import streamlit as st
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager
from database.db import create_tables

#this sets the page title and centers the layout on the screen
st.set_page_config(page_title="Home", layout="centered")

#initialize
create_tables()
db = DatabaseManager("database/platform.db")
auth = AuthManager(db)

st.title("🏠 Multi Domain Platform")

#checking if already logged in
if "logged_in" in st.session_state and st.session_state.logged_in:
    st.success(f"Welcome {st.session_state.current_user}!")
    
    # Show domain buttons
    st.subheader("Select Domain")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🛡️ Cybersecurity", use_container_width=True):
            st.switch_page("pages/2_Cybersecurity.py")
    with col2:
        if st.button("📊 Data Science", use_container_width=True):
            st.switch_page("pages/3_Data_science.py")
    with col3:
        if st.button("🖥️ IT Operations", use_container_width=True):
            st.switch_page("pages/4_IT_Operations.py")
    
    col4, col5 = st.columns(2)
    with col4:
        if st.button("🤖 AI Assistant", use_container_width=True):
            st.switch_page("pages/5_AI_Assistant.py")
    with col5:
        if st.button("Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    
    st.stop()

#create two tabs on the screen
tab_login, tab_register = st.tabs(["Login", "Register"])

#login tab
with tab_login:
    st.subheader("Login to Your Account")
    
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")
    
    #when the user clicks this button, the login process starts
    if st.button("Login", type="primary", key="login_btn"):
        if login_username and login_password:
            user = auth.login_user(login_username, login_password)
            if user:
                st.session_state.current_user = user.get_username()
                st.session_state.current_role = user.get_role()
                st.session_state.logged_in = True
                st.success(f"Welcome {user.get_username()}!")
                st.rerun()
            else:
                st.error("Wrong username or password")
        else:
            st.error("Enter username and password")

#registration tab
with tab_register:
    st.subheader("Create New Account")
    #user enters details to create a new account
    reg_username = st.text_input("Choose Username", key="reg_username")
    reg_password = st.text_input("Choose Password", type="password", key="reg_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
    
    #password requirements
    st.caption("Password must be at least 8 characters long")
    
    if st.button("Register", type="secondary", key="register_btn"):
        if not reg_username or not reg_password:
            st.error("Please fill in all fields")
        elif len(reg_password) < 8:
            st.error("Password must be at least 8 characters long")
        elif reg_password != confirm_password:
            st.error("Passwords do not match")
        else:
            if auth.register_user(reg_username, reg_password):
                st.success("✅ Account created! You can now login.")
            else:
                st.error("Username already exists. Please choose another.")

