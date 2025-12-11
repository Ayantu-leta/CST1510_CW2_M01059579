import streamlit as st
from services.database_manager import DatabaseManager
from models.it_ticket import ITTicket
import pandas as pd

st.set_page_config(page_title="IT Operations", page_icon="🖥️")

#blocking the page if the user is not logged in 
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page.")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()

db = DatabaseManager("database/platform.db")

st.title("🖥️ IT Operations Dashboard")
st.success(f"Hello {st.session_state.current_user}!")

#three buttons for CRUD, Analytics, AI Assistant
st.subheader("Operations")
col1, col2, col3 = st.columns(3)

with col1:
    crud_btn = st.button("📝 CRUD", use_container_width=True)
with col2:
    analytics_btn = st.button("📈 Analytics", use_container_width=True)
with col3:
    ai_btn = st.button("🤖 AI Assistant", use_container_width=True)

#handle AI button
if ai_btn:
    st.session_state.selected_domain = "IT Operations"
    st.switch_page("pages/5_AI_Assistant.py")

#initialize section
if 'show_section' not in st.session_state:
    st.session_state.show_section = "crud"

#handle button clicks
if crud_btn:
    st.session_state.show_section = "crud"
    st.rerun()

if analytics_btn:
    st.session_state.show_section = "analytics"
    st.rerun()

# CRUD section
if st.session_state.show_section == "crud":
    st.subheader("📝 Manage IT Tickets")
    
    #views tickets
    rows = db.fetch_all("SELECT id, title, priority, status, assigned_user_id FROM it_tickets")
    
    tickets = []
    for row in rows:
        user_row = db.fetch_one("SELECT username FROM users WHERE id = ?", (row[4],))
        assigned_to = user_row[0] if user_row else "Unassigned"
        
        ticket = ITTicket(
            ticket_id=row[0],
            title=row[1],
            priority=row[2],
            status=row[3],
            assigned_to=assigned_to
        )
        tickets.append(ticket)
    
    for ticket in tickets:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.write(f"ID: {ticket._ITTicket__id}")
            st.write(f"Priority: {ticket.get_priority()}")
            st.write(f"Status: {ticket.get_status()}")
        with col2:
            st.write(f"Title: {ticket.get_title()}")
            st.write(f"Assigned to: {ticket.get_assigned_user()}")
        
    #buttons for each ticket
        col3, col4 = st.columns(2)
        with col3:
            if st.button(f"Close Ticket", key=f"close_{ticket._ITTicket__id}"):
                db.execute_query("UPDATE it_tickets SET status = 'closed' WHERE id = ?", 
                               (ticket._ITTicket__id,))
                st.success("Ticket closed!")
                st.rerun()
        with col4:
            if st.button(f"Delete", key=f"delete_{ticket._ITTicket__id}"):
                db.execute_query("DELETE FROM it_tickets WHERE id = ?", 
                               (ticket._ITTicket__id,))
                st.success("Ticket deleted!")
                st.rerun()
        
        st.divider()
    
    st.subheader(" Create New Ticket")
    with st.form("new_ticket"):
        title = st.text_input("Ticket Title")
        priority = st.selectbox("Priority", ["low", "medium", "high", "urgent"])
        
        if st.form_submit_button("Create Ticket"):
            if title:
                db.execute_query(
                    "INSERT INTO it_tickets (title, priority) VALUES (?, ?)",
                    (title, priority)
                )
                st.success("Ticket created!")
                st.rerun()

#analytics section
elif st.session_state.show_section == "analytics":
    st.subheader("📈 IT Analytics")

    data = db.fetch_all("SELECT priority, status, COUNT(*) FROM it_tickets GROUP BY priority, status")
    
    if data:
        df = pd.DataFrame(data, columns=["Priority", "Status", "Count"])
 
        chart_type = st.selectbox("Select Chart Type", 
                                 ["Bar Chart", "Pie Chart", "Line Chart"])
        
        if chart_type == "Bar Chart":
            pivot_df = df.pivot(index="Priority", columns="Status", values="Count").fillna(0)
            st.bar_chart(pivot_df)
        
        elif chart_type == "Pie Chart":
            priority_data = db.fetch_all("SELECT priority, COUNT(*) FROM it_tickets GROUP BY priority")
            priority_df = pd.DataFrame(priority_data, columns=["Priority", "Count"])
            st.write("Ticket Priority Distribution")
            for index, row in priority_df.iterrows():
                st.write(f"{row['Priority']}: {row['Count']} tickets")
        
        elif chart_type == "Line Chart":
            dates = pd.date_range(start='2024-01-01', periods=7, freq='D')
            tickets_daily = [3, 2, 4, 1, 2, 0, 1]
            timeline_df = pd.DataFrame({'Date': dates, 'Tickets': tickets_daily})
            st.line_chart(timeline_df.set_index('Date'))
        
        #show data table
        st.write("Data Summary")
        st.write(df)
    else:
        st.info("No data available for analytics")

#navigation
st.divider()
if st.button("🏠 Back to Home"):
    st.switch_page("Home.py")