import streamlit as st
import pandas as pd

st.set_page_config(page_title=" 📝_Data Management", layout="wide")

#blocking the page if the user is not logged in
if not st.session_state.logged_in:
    st.error("You must be logged in to view this page.")
    if st.button("Go to login page"):
        st.switch_page("Home.py")
    st.stop()

st.title("📝 Data Management")
st.success(f"Hello, **{st.session_state.username}**!")

#create a list to store records if it does not exist
if "records" not in st.session_state:
    st.session_state.records = []

#form to add a new record
with st.form("add_record"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    role = st.selectbox("Role", ["User", "Admin"])
    
    if st.form_submit_button("Add Record"):
        record = {"name": name, "email": email, "role": role}
        st.session_state.records.append(record)
        st.success("Record added!")

# Show records 
if st.session_state.records:
    st.subheader("All Records")
    df = pd.DataFrame(st.session_state.records)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No records found")

st.divider()

#updating a record
st.subheader("Update Record")
if st.session_state.records:
    #get list of names for selection
    names = [r["name"] for r in st.session_state.records]
    selected = st.selectbox("Select record to update", names)
    
    #find the selected record index
    idx = names.index(selected)
    record = st.session_state.records[idx]
    
    #updating form
    with st.form("update_form"):
     #pre-fill with existing values
        new_email = st.text_input("Email", record["email"])
        new_role = st.selectbox("Role", ["User", "Admin"], 
                              index=0 if record["role"]=="User" else 1)
        
        if st.form_submit_button("Update"):
            st.session_state.records[idx]["email"] = new_email
            st.session_state.records[idx]["role"] = new_role
            st.success("Record updated!")
else:
    st.info("No records to update")

st.divider()

#deleteing a record
st.subheader("Delete Record")
if st.session_state.records:
    names = [r["name"] for r in st.session_state.records]
    to_delete = st.selectbox("Select record to delete", names)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.warning(f"Delete {to_delete}?")
    
    with col2:
        if st.button("Delete", type="primary"):
            idx = names.index(to_delete)
            st.session_state.records.pop(idx)
            st.success("Record deleted!")
            st.rerun()
else:
    st.info("No records to delete")

st.divider()
if st.button("Back to Dashboard"):
    st.switch_page("pages/1_Dashboard.py")

