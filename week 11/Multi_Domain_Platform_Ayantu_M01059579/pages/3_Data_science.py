import streamlit as st
from services.database_manager import DatabaseManager
from models.dataset import Dataset
import pandas as pd

st.set_page_config(page_title="Data Science", page_icon="📊")

#blocking the page if the user is not logged in 
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page.")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()

#connecting to the database
db = DatabaseManager("database/platform.db")

st.title("📊 Data Science Dashboard")
st.success(f"Hello {st.session_state.current_user}!")

#three button operations
st.subheader("Operations")
col1, col2, col3 = st.columns(3)

with col1:
    crud_btn = st.button("📝 CRUD", use_container_width=True)
with col2:
    analytics_btn = st.button("📈 Analytics", use_container_width=True)
with col3:
    ai_btn = st.button("🤖 AI Assistant", use_container_width=True)

#open AI page when clicked
if ai_btn:
    st.session_state.selected_domain = "Data Science"
    st.switch_page("pages/5_AI_Assistant.py")

#initialize section
if 'show_section' not in st.session_state:
    st.session_state.show_section = "crud"

#switch to CRUD section
if crud_btn:
    st.session_state.show_section = "crud"
    st.rerun()

#switch to analytics section
if analytics_btn:
    st.session_state.show_section = "analytics"
    st.rerun()

# CRUD section
if st.session_state.show_section == "crud":
    st.subheader("📝 Manage Datasets")
    
    #fetches all datasets from database
    rows = db.fetch_all("SELECT id, name, size_bytes, rows, source FROM datasets")
    
    datasets = []
    for row in rows:
        dataset = Dataset(
            dataset_id=row[0],
            name=row[1],
            size_bytes=row[2],
            rows=row[3],
            source=row[4]
        )
        datasets.append(dataset)
    
    #display each datasets with details and delete button
    for dataset in datasets:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.write(f"Name: {dataset.get_name()}")
            st.write(f"Source: {dataset.get_source()}")
        with col2:
            size_mb = dataset.calculate_size_mb()
            st.write(f"Size: {size_mb:.2f} MB")
            st.write(f"Rows: {dataset.get_rows():,}")
        
        if st.button(f"Delete {dataset.get_name()}", key=f"del_{dataset._Dataset__id}"):
            db.execute_query("DELETE FROM datasets WHERE id = ?", (dataset._Dataset__id,))
            st.success("Dataset deleted!")
            st.rerun()
        
        st.divider()
    
    #add new dataset
    st.subheader("Add New Dataset")
    with st.form("new_dataset"):
        name = st.text_input("Dataset Name")
        source = st.text_input("Source")
        size_bytes = st.number_input("Size (bytes)", min_value=0)
        rows = st.number_input("Number of rows", min_value=0)
        
        if st.form_submit_button("Add Dataset"):
            if name and source:
                db.execute_query(
                    "INSERT INTO datasets (name, size_bytes, rows, source) VALUES (?, ?, ?, ?)",
                    (name, size_bytes, rows, source)
                )
                st.success("Dataset added!")
                st.rerun()
            else:
                st.error("Please fill required fields")

#analytics section
elif st.session_state.show_section == "analytics":
    st.subheader("📈 Data Analytics")
    
    #get data
    data = db.fetch_all("SELECT name, size_bytes, rows FROM datasets")
    
    if data:
        #creating DataFrame
        df = pd.DataFrame(data, columns=["Dataset", "Size_Bytes", "Rows"])
        df["Size_MB"] = df["Size_Bytes"] / (1024 * 1024)
        
        #chart selection
        chart_type = st.selectbox("Select Chart Type", 
                                 ["Bar Chart", "Pie Chart", "Line Chart"])
        
        chart_data = st.selectbox("Show", ["Size (MB)", "Rows Count"])
        
        if chart_data == "Size (MB)":
            chart_df = df[["Dataset", "Size_MB"]].set_index("Dataset")
            chart_title = "Dataset Sizes (MB)"
        else:
            chart_df = df[["Dataset", "Rows"]].set_index("Dataset")
            chart_title = "Dataset Rows Count"
        
        if chart_type == "Bar Chart":
            st.bar_chart(chart_df)
        
        elif chart_type == "Pie Chart":
            st.write(f" {chart_title}")
            for index, row in df.iterrows():
                if chart_data == "Size (MB)":
                    st.write(f"{row['Dataset']}: {row['Size_MB']:.2f} MB")
                else:
                    st.write(f"{row['Dataset']}: {row['Rows']:,} rows")
        
        elif chart_type == "Line Chart":
            # Create sample timeline
            dates = pd.date_range(start='2024-01-01', periods=5, freq='D')
            sizes = [500, 550, 600, 650, 700]
            timeline_df = pd.DataFrame({'Date': dates, 'Size_MB': sizes})
            st.line_chart(timeline_df.set_index('Date'))
        
        #show data table
        st.write(" Data Summary")
        st.write(df[["Dataset", "Size_MB", "Rows"]])
    else:
        st.info("No data available for analytics")

#navigation
st.divider()
if st.button("🏠 Back to Home"):
    st.switch_page("Home.py")