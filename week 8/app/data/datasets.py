import pandas as pd
import sqlite3
#import for db.py has been fixed in the app/data/__init__.py 
from app.data.db import connect_database

def insert_dataset(name, category, source):
    """Insert a new dataset- metadata

    The input arguments (name, category, source) are mapped to the 
    database columns (dataset_name, category, source) respectively

    """
    conn = connect_database()
    cursor = conn.cursor()
    try:
        #Updated column names to match the defined datasets_metadata schema
        #(dataset_name, category, source)
        cursor.execute("""
            INSERT INTO datasets_metadata (name, description, main_speaker )
            VALUES (?, ?, ? )
        """, 
        (name, category, source))
        conn.commit()
        dataset_id = cursor.lastrowid
        return dataset_id
    except Exception as e:
        print(f"Database error: {e}")
        return None
    finally:
        conn.close()

def get_all_datasets():
    """Get all datasets as DataFrame """
    conn = connect_database()
    try:
         #pd.read_sql_query retrieves data directly into a DataFrame
        df = pd.read_sql_query("SELECT * FROM datasets_metadata ORDER BY id DESC", conn)
        return df
    finally:
        conn.close()