import streamlit as st
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager
from database.db import create_tables

st.set_page_config(page_title="Login", page_icon="🔐")

#initialize
create_tables()
db = DatabaseManager("database/platform.db")
auth = AuthManager(db)

st.title("🔐 Login")

#checking if already logged in
if "logged_in" in st.session_state and st.session_state.logged_in:
    st.success(f"Already logged in as {st.session_state.current_user}")
    if st.button("Go to Home"):
        st.switch_page("Home.py")
    st.stop()

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login", type="primary"):
    if username and password:
        user = auth.login_user(username, password)
        if user:
            st.session_state.current_user = user.get_username()
            st.session_state.current_role = user.get_role()
            st.session_state.logged_in = True
            st.success(f"Welcome {user.get_username()}!")
            st.rerun()
            st.switch_page("Home.py")
        else:
            st.error("Wrong username or password")
    else:
        st.error("Enter username and password")

if st.button("Back to Home"):
    st.switch_page("Home.py")