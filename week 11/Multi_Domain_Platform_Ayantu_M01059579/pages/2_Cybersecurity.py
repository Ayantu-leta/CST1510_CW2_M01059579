import streamlit as st
from services.database_manager import DatabaseManager
from models.security_incident import SecurityIncident
import pandas as pd

st.set_page_config(page_title="Cybersecurity", page_icon="🛡️")

#blocking the page if the user is not logged in  
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page.")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()

db = DatabaseManager("database/platform.db")

st.title("🛡️ Cybersecurity Dashboard")
st.success(f"Hello {st.session_state.current_user}!")

st.subheader("Operations")
col1, col2, col3 = st.columns(3)

with col1:
    crud_btn = st.button("📝 CRUD", use_container_width=True)
with col2:
    analytics_btn = st.button("📈 Analytics", use_container_width=True)
with col3:
    ai_btn = st.button("🤖 AI Assistant", use_container_width=True)

#AI assistant button logic
if ai_btn:
    st.session_state.selected_domain = "Cybersecurity"
    st.switch_page("pages/5_AI_Assistant.py")

#initialize section in session
if 'show_section' not in st.session_state:
    st.session_state.show_section = "crud"

if crud_btn:
    st.session_state.show_section = "crud"
    st.rerun()

if analytics_btn:
    st.session_state.show_section = "analytics"
    st.rerun()

if st.session_state.show_section == "crud":
    st.subheader("📝 Manage Security Incidents")

    rows = db.fetch_all("SELECT id, incident_type, severity, status, description FROM security_incidents")
    
    #creating security incident objects
    incidents = []
    for row in rows:
        incident = SecurityIncident(
            incident_id=row[0],
            incident_type=row[1],
            severity=row[2],
            status=row[3],
            description=row[4]
        )
        incidents.append(incident)
    
        #display each incident
    for incident in incidents:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.write(f"ID: {incident.get_id()}")
            st.write(f"Severity: {incident.get_severity()}")
            st.write(f"Status: {incident.get_status()}")
        with col2:
            st.write(f"Type: {incident.get_incident_type()}")
            st.write(f"Description: {incident.get_description()}")
 
        new_status = st.selectbox("Change Status", 
                                  ["open", "investigating", "resolved", "closed"],
                                  key=f"status_{incident.get_id()}")
        
        col3, col4 = st.columns(2)
         #updating status button
        with col3:
            if st.button("Update Status", key=f"update_{incident.get_id()}"):
                db.execute_query("UPDATE security_incidents SET status = ? WHERE id = ?", 
                               (new_status, incident.get_id()))
                st.success("Status updated!")
                st.rerun()
     #deleting incident button
        with col4:
            if st.button("Delete", key=f"delete_{incident.get_id()}"):
                db.execute_query("DELETE FROM security_incidents WHERE id = ?", 
                               (incident.get_id(),))
                st.success("Incident deleted!")
                st.rerun()
        
        st.divider()
   #adding new incident form
    st.subheader(" Add New Incident")
    with st.form("new_incident"):
        incident_type = st.text_input("Incident Type")
        severity = st.selectbox("Severity", ["low", "medium", "high", "critical"])
        description = st.text_area("Description")
        
        if st.form_submit_button("Add Incident"):
            if incident_type and description:
                db.execute_query(
                    "INSERT INTO security_incidents (incident_type, severity, description) VALUES (?, ?, ?)",
                    (incident_type, severity, description)
                )
                st.success("Incident added!")
                st.rerun()
            else:
                st.error("Please fill required fields")

#analytics section
elif st.session_state.show_section == "analytics":
    st.subheader("📈 Cybersecurity Analytics")

    data = db.fetch_all("SELECT severity, COUNT(*) as count FROM security_incidents GROUP BY severity")
    
    if data:
        df = pd.DataFrame(data, columns=["Severity", "Count"])

        chart_type = st.selectbox("Select Chart Type", 
                                 ["Bar Chart", "Pie Chart", "Line Chart"])
        
        if chart_type == "Bar Chart":
            st.bar_chart(df.set_index("Severity"))
        
        elif chart_type == "Pie Chart":
            st.write("Incident Distribution")
            for index, row in df.iterrows():
                st.write(f"{row['Severity']}: {row['Count']} incidents")
        
        elif chart_type == "Line Chart":
            dates = pd.date_range(start='2024-01-01', periods=7, freq='D')
            values = [2, 1, 3, 2, 1, 0, 1]
            timeline_df = pd.DataFrame({'Date': dates, 'Incidents': values})
            st.line_chart(timeline_df.set_index('Date'))
        
        #show data table
        st.write(" Data Summary")
        st.write(df)
    else:
        st.info("No data available for analytics")

#navigation
st.divider()
if st.button("🏠 Back to Home"):
    st.switch_page("Home.py")