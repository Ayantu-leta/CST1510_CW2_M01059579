import streamlit as st
import pandas as pd
import numpy as np
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="🔒Cybersecurity", layout="wide")

#blocking the page if the user is not logged in   
if not st.session_state.logged_in:
    st.error("You must be logged in to view this page.")
    if st.button("Go to login page"):
        st.switch_page("Home.py")
    st.stop()

st.title("Cybersecurity Dashboard")
st.success(f"Hello, **{st.session_state.username}**!")

#three metric cards
col1, col2, col3 = st.columns(3)

#each metric shows a value and a change number
with col1:
    st.metric("Threats Detected","247", delta= "+12")

with col2:
    st.metric("Incidents", "3", delta="+1")

with col3:
    st.metric("Vulnerabilities", "8", delta= "-3")

#simple threat data for the bar chart
threat_data = pd.DataFrame({
    "Malware": [45, 32, 28, 51, 39],
    "Phishing": [23, 45, 32, 28, 37],
    "DDoS": [12, 8, 15, 9, 11]

})
#it will display the chart
st.subheader("Threat Distribution")
st.bar_chart(threat_data)

st.divider()



if st.button("Back to Dashboard"):
    st.switch_page("pages/1_Dashboard.py")


    