import pandas as pd
import sqlite3
from app.data.db import connect_database

def insert_ticket(priority, status, category, subject, description, created_date, resolved_date=None, assigned_to=None):
    """
    Insert a new IT ticket by mapping arguments to CSV-derived schema columns
    
    Args:
        category (str): Ticket category (maps to Category)
        status (str): Ticket status (maps to Ticket_Type)
        subject (str): Brief input/subject (maps to Customer_Input)
        description (str): Detailed text (maps to Possible_Resolution)
        created_date (str): Date of creation (maps to created_at)

    Returns:
        tuple: (success_bool, message, ticket_db_id/None)
    """
    conn = connect_database()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO it_tickets 
            (Category, Ticket_Type, Customer_Input, Possible_Resolution, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (category, status, subject, description, created_date))
        conn.commit()
        ticket_db_id = cursor.lastrowid
        return True, f"Ticket #{ticket_db_id} created successfully", ticket_db_id
    except Exception as e:
        #rollback to clean up transaction state on error
        return False, f"Database error: {e}", None
    finally:
        conn.close()

def get_all_tickets():
    """Get all tickets as DataFrame ordered by creation date"""
    conn = connect_database()
    try:
        df = pd.read_sql_query(
            "SELECT * FROM it_tickets ORDER BY created_at DESC",
            conn
        )
        return df
    finally:
        conn.close()

def get_ticket_by_id(ticket_id):
    """Get specific ticket by ID."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM it_tickets WHERE id = ?",
        (ticket_id,)
    )
    ticket = cursor.fetchone()
    conn.close()
    return ticket

def update_ticket_status(ticket_id, new_status):
    """Update ticket status."""
    conn = connect_database()
    cursor = conn.cursor()
    # Updates the Ticket_Type column based on the new_status value
    cursor.execute(
        "UPDATE it_tickets SET Ticket_Type = ? WHERE id = ?",
        (new_status, ticket_id)
    )
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0

def delete_ticket(ticket_id):
    """Delete ticket by ID."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM it_tickets WHERE id = ?",
        (ticket_id,)
    )
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0

def get_tickets_by_status():
    """Get ticket counts by status."""
    conn = connect_database()
    try:
        df = pd.read_sql_query("""
            SELECT Ticket_Type as status, COUNT(*) as count
            FROM it_tickets
            GROUP BY Ticket_Type
            ORDER BY count DESC
        """, conn)
        return df
    finally:
        conn.close()