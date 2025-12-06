import streamlit as st
import pandas as pd

st.set_page_config(page_title=" ⚙️_IT Operations", layout="wide")

#blocking the page if the user is not logged in 
if not st.session_state.logged_in:
    st.error("You must be logged in to view this page.")
    if st.button("Go to login page"):
        st.switch_page("Home.py")
    st.stop()

st.title("IT Operations Dashboard")
st.success(f"Hello, **{st.session_state.username}**!")

#three metric cards
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("CPU Usage", "67%", delta="+5%")

with col2:
    st.metric("Memory Usage", "8.2 GB",delta= "+0.3 GB")

with col3:
    st.metric("Uptime", "99.8%", delta="+0.1%")

#creating sample system data to visualization the dataframe contains data 
system_data = pd.DataFrame({
    "hour": [0, 6, 12, 18, 23],
    "CPU": [45, 52, 78, 82, 67],
    "Memory": [62, 68, 85, 91, 82]
})

st.subheader("System Resources")
st.line_chart(system_data.set_index("hour"))    # st.line_chart creates a line chart from the dataframe

st.divider()
if st.button("Back to Dashboard"):
    st.switch_page("pages/1_Dashboard.py")