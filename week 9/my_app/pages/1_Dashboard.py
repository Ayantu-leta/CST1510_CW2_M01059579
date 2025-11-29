import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
from pathlib import Path
import sys

#connect to your SQLite database file
db_path = "/Users/ayu/CST1510_CW2_M01059579/week 8/DATA/intelligence_platform.db"
conn = sqlite3.connect(db_path)

#read the entire cyber_incidents table into a DataFrame
incidents_df = pd.read_sql_query("SELECT * FROM cyber_incidents", conn)
conn.close()

st.set_page_config(page_title=" ⛓️‍💥_Dashboard", layout="wide")


#blocking the page if the user is not logged in
if not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to login page"):
        st.switch_page("Home.py")
    st.stop()


st.title("Dashboard")
st.success(f"Hello, **{st.session_state.username}**! You are logged in.")

#show how many rows were loaded from the database
st.success(f"✅ Loaded {len(incidents_df)} records from Week 8 database")
st.caption(f"Welcome to your personalized dashboard, {st.session_state.username}! ")

with st.sidebar:
    st.header("Filters")
#slider to select how many rows to display
    n_points = st.slider("Number of data points", 10, 200, 50)


data = incidents_df.head(n_points)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Line chart")

#select numeric columns in the data
    numeric_cols = data.select_dtypes(include=[np.number]).columns

 #if there is any one numeric column it will plot the first one
    if len(numeric_cols) > 0:
        st.line_chart(data[numeric_cols[0]])

#if no numeric column exists it will plot the first column anyway
    else:
        st.line_chart(data.iloc[:, 0])

with col2:
    st.subheader("Bar chart")

 #select columns with text or object data
    categorical_cols = data.select_dtypes(include=['object']).columns

#if there is any one categorical column it will count its values
    if len(categorical_cols) > 0:
        value_counts = data[categorical_cols[0]].value_counts().head(10)
        st.bar_chart(value_counts)
    else:
        st.bar_chart(data.iloc[:, 1])

with st.expander("See raw data"):
    st.dataframe(data)

st.divider()

st.subheader("Go to Domain Pages")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔒Cybersecurity"):
        st.switch_page("pages/2_Cybersecurity.py")

with col2:
    if st.button("📊Data Science"):
        st.switch_page("pages/3_Datascience.py")

with col3:
    if st.button("📝 Data Management"):  
        st.switch_page("pages/4_CRUD.py")  

st.divider()
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.info("You have been logged out.")
    st.switch_page("Home.py")