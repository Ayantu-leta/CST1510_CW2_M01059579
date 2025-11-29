import streamlit as st

#this sets the page title and centers the layout on the screen
st.set_page_config(page_title="Login / Register", layout="centered")

#create a place to store users only if it is not already created
if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

st.title("Welcome")

#if a user is already logged in show this message and stop the page
if st.session_state.logged_in:
    st.success(f"Already logged in as {st.session_state.username}.")

#button to move to the dashboard page
    if st.button("Go to dashboard"):
        st.switch_page("pages/1_Dashboard.py")
    st.stop()

#create two tabs on the screen
tab_login, tab_register = st.tabs(["Login", "Register"])

with tab_login:
    st.subheader("Login")
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

 #when the user clicks this button, the login process starts
    if st.button("Log in", type="primary"):
        users = st.session_state.users
        if login_username in users and users[login_username] == login_password:
            st.session_state.logged_in = True
            st.session_state.username = login_username
            st.success(f"Welcome back, {login_username}!")
            st.switch_page("pages/1_Dashboard.py")
        else:
            st.error("Invalid username or password")

with tab_register:
    st.subheader("Register")
#user enters details to create a new account
    new_username = st.text_input("Choose a username", key="register_username")
    new_password = st.text_input("Choose a password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm")
    
    if st.button("Create account"):
        if not new_username or not new_password:
            st.warning("Please fill in all fields.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        elif new_username in st.session_state.users:
            st.error("Username already exists. Choose another one.")
        else:
            st.session_state.users[new_username] = new_password
            st.success("Account created! You can now log in from the Login tab.")
            st.info("Tip: go to the Login tab and sign in with your new account.")