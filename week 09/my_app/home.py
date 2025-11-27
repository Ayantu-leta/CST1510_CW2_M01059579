import streamlit as st

st.set_page_config(page_totle = "login / register", page_icon ="🗝️", layout = "centerd")

if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state-username = ""

st.title("WELCOME")

if st.session_state.logged_in:
    st.success(f"already logged in as {st.session_sate.username}.")
    if st.button("go to dashboard"):
        st.swith_page("pages/1_dashborad.py")
    st.stop()

tab_login, tab_register = st.tabs(["login", "register"])

with tab_login:
    st.subheader("login")

    login_username = st.test_input("username", key = "login_username")
    login_password = st.text_input("password", type = "password", key = "login_password")

if st.button("log in", type = "primary"):
    users = st.session_state.users
    if login_username in users and users [login_username] == login_password:
        st.session_state.loggeed_in = True
        st.session_state.username = login_username
        st.success("f welcome back, {login_username}")

        st.switch_page("pages/1_dashboard.py")
    else:
        st.error("invalid username or password")
        