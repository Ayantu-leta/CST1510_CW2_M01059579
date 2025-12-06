import streamlit as st
import pandas as pd
import numpy as np
from openai import OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title=" 📊_Data Science", layout="wide")

#blocking the page if the user is not logged in
if not st.session_state.logged_in:
    st.error("You must be logged in to view this page.")
    if st.button("Go to login page"):
        st.switch_page("Home.py")
    st.stop()


st.title("Data Science Dashboard")
st.success(f"Hello, **{st.session_state.username}**!")

#three metric cards
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Accuracy", "94.2%")

with col2:
    st.metric("Precision", "87%")

with col3:
    st.metric("Recall", "89.5%")

#training history data for the line chart
history = pd.DataFrame({
    "epoch": [1, 2, 3, 4, 5],
    "accuracy": [0.65, 0.78, 0.85, 0.89, 0.94],
    "loss": [0.45, 0.32, 0.24, 0.18, 0.15]
})
#line chart showing training progress
st.subheader("Model Training Progress")
st.line_chart(history, x = "epoch", y = ["loss", "accuracy"])

st.divider()

if st.button("Back to Dashboard"):
    st.switch_page("pages/1_Dashboard.py")