import pandas as pd
import sqlite3
from app.data.db import connect_database


def insert_incident(date, title, severity, status, description, reported_by):
    """
    Insert a new cyber incident. Maps the 'title' argument to the 'incident_type' column.
    
    Args:
        date (str): Incident date (YYYY-MM-DD).
        title (str): Title or type of the incident (mapped to incident_type).
        severity (str): Severity level.
        status (str): Current status.
        description (str): Full incident description.
        reported_by (str): Username of the reporter.
    
    Returns:
        int/None: The ID of the new incident or None on failure.
        
        """
    conn = connect_database()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO cyber_incidents 
            (Date, Title, severity, status, Description, reported_by)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (date, title, severity, status, description, reported_by))
        conn.commit()
        incident_id = cursor.lastrowid
        return incident_id
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        conn.close()

def get_all_incidents():
    """Get all incidents as DataFrame."""
    conn = connect_database()
    try:
         # Reads the entire result set into a pandas DataFrame.
        df = pd.read_sql_query("SELECT * FROM cyber_incidents ORDER BY id DESC", conn)
        return df
    finally:
        conn.close()

def update_incident_status(incident_id, new_status):
    """Update incident status by ID"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE cyber_incidents SET status = ? WHERE id = ?",
        (new_status, incident_id)
    )
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0

def delete_incident(incident_id):
    """Delete incident by ID."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM cyber_incidents WHERE id = ?",
        (incident_id,)
    )
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0

def get_incidents_by_type_count():
    """ 
    Get incident counts grouped by type (incident_type column) 
    Returns data as a DataFrame for visualization
    
    """
    conn = connect_database()
    try:
        df = pd.read_sql_query("""
            SELECT Type as incident_type, COUNT(*) as count
            FROM cyber_incidents
            GROUP BY Type
            ORDER BY count DESC
        """, conn)
        return df
    finally:
        conn.close()

def get_high_severity_by_status(conn):
    """
    Get high severity incidents by status. 
    Requires an existing database connection object (conn) to be passed in
    
    """
    query = """ 
    SELECT status, COUNT(*) as count
    FROM cyber_incidents
    WHERE LOWER(severity) = 'high'
    GROUP BY status
    ORDER BY count DESC
    """
    #Uses the connection passed as an argument
    df = pd.read_sql_query(query, conn)
    return df