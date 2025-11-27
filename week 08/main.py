import pandas as pd
import sqlite3
from pathlib import Path
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Import from your corrected db.py
from app.data.db import (
    connect_database,
    DB_PATH, 
    CYBER_INCIDENTS_CSV,
    DATASETS_METADATA_CSV,
    IT_TICKETS_CSV
)

# Import schema and services
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user, migrate_users_from_file

# Import data functions
from app.data.incidents import insert_incident, update_incident_status, delete_incident
from app.data.datasets import insert_dataset
from app.data.tickets import insert_ticket



def diagnose_csv_structure():
    """Check the structure of all CSV files"""
    print("\n" + "="*60)
    print("CSV STRUCTURE DIAGNOSIS")
    print("="*60)
    
    csv_files = {
        "CYBER_INCIDENTS": CYBER_INCIDENTS_CSV,  
        "DATASETS_METADATA": DATASETS_METADATA_CSV, 
        "IT_TICKETS": IT_TICKETS_CSV
    }
    
    for name, path in csv_files.items():
        print(f"\n{name}: {path}")
        if path.exists():
            df = pd.read_csv(path)
            print(f"  Columns: {list(df.columns)}")
            print(f"  Shape: {df.shape}")
        else:
            print("  ❌ File not found")

def load_csv_to_table(conn, csv_path: Path, table_name: str):
    """
    Load a CSV file into a database table using pandas.
    """
    csv_file = Path(csv_path)
    if not csv_file.exists():
        # IMPORTANT: Print the variable name, not the path, when the path is wrong
        print(f"❌ CSV file not found (Check mapping in load_all_csv_data): {csv_path}")
        return 0
    
    try:
        df = pd.read_csv(csv_path)
        df.columns = df.columns.str.strip()

        df.columns = [col.strip().replace(' ', '_') for col in df.columns]

        print(f" 🎉 Loading {len(df)} rows from {csv_path.name}")
        print(f"  CSV columns: {list(df.columns)}")
        
        # Check table structure
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        table_columns = [column[1] for column in cursor.fetchall()]
        print(f"  Table columns: {table_columns}")
    
        df.to_sql(
            name=table_name, 
            con=conn, 
            if_exists='append', 
            index=False
        )
    
        print(f"✅ Loaded {len(df)} rows into '{table_name}' from {csv_path.name}")
        return len(df)
    except Exception as e:
        print(f"❌ Error loading {csv_path.name}: {e}")
        return 0

def load_all_csv_data(conn):
    """ coordinates the loading of all domain csv files"""
    total_rows = 0

    # FIX: Use the imported Path variables (not strings) as keys
    csv_to_table = {
        CYBER_INCIDENTS_CSV: "cyber_incidents",
        DATASETS_METADATA_CSV: "datasets_metadata",
        IT_TICKETS_CSV: "it_tickets"
    }
    
    for csv_path, table_name in csv_to_table.items():
        rows = load_csv_to_table(conn, csv_path, table_name)
        total_rows += rows
    return total_rows
    

def setup_database_complete():
    """
    Complete database setup:
    1. Connect to database
    2. Create all tables
    3. Migrate users from users.txt
    4. Load CSV data for all domains
    5. Verify setup
    """
    print("\n" + "="*60)
    print("STARTING COMPLETE DATABASE SETUP")
    print("="*60)
    

    diagnose_csv_structure()
    
    # Step 1: Connect
    print("\n[1/5] Connecting to database...")
    conn = connect_database()
    print("Connected")
    
    # Step 2: Create tables
    print("\n[2/5] Creating database tables...")
    create_all_tables(conn)
    
    # Step 3: Migrate users
    print("\n[3/5] Migrating users from users.txt...")
    user_count = migrate_users_from_file("/Users/ayu/CST1510_CW2_M01059579/week 08/DATA/users.txt")
    print(f" Migrated {user_count} users")
    
    # Step 4: Load CSV data
    print("\n[4/5] Loading CSV data...")
    total_rows = load_all_csv_data(conn)
    
    # Step 5: Verify
    print("\n[5/5] Verifying database setup...")
    cursor = conn.cursor()
    
    # Count rows in each table
    tables = ['users', 'cyber_incidents', 'datasets_metadata', 'it_tickets']
    print("\n Database Summary:")
    print(f"{'Table':<25} {'Row Count':<15}")
    print("-" * 40)
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:<25} {count:<15}")
    
    conn.close()
    
    print("\n" + "="*60)
    print(" DATABASE SETUP COMPLETE!")
    print("="*60)
    print(f"\n Database location:", DB_PATH.resolve())
    print("\nYou're ready for Week 9 (Streamlit web interface)!")


def run_comprehensive_tests():
    """
    Run comprehensive tests on your database.
    """
    print("\n" + "="*60)
    print("🧪 RUNNING COMPREHENSIVE TESTS")
    print("="*60)
    
    conn = connect_database()
    
    # Test 1: Authentication
    print("\n[TEST 1] Authentication")
    success, msg = register_user("test_user", "TestPass123!", "user")
    print(f"  Register: {'✅' if success else '❌'} {msg}")
    
    success, msg = login_user("test_user", "TestPass123!")
    print(f"  Login:    {'✅' if success else '❌'} {msg}")
    
    # Test 2: CRUD Operations
    print("\n[TEST 2] CRUD Operations")
    
    # Create
    try:
        test_id = insert_incident(
            "2024-11-05",
            "Test Incident",
            "Low",
            "Open",
            "This is a test incident",
            "tester"
        )
        
        if test_id:
            print(f"  Create: ✅ Incident #{test_id} created")
            
            update_incident_status(test_id, "Resolved")
            print(f"  Update: Status updated")
            
            delete_incident(test_id)
            print(f"  Delete: Incident deleted")
        else:
            print(f"  Create: ❌ Failed to create incident")
        
    except Exception as e:
        print(f"  CRUD Operations: ❌ Failed - {e}")
    
    # Test 3: Additional Inserts - FIXED DATASET CALL
    print("\n[TEST 3] Additional Inserts")
    try:
        # Use the correct number of parameters for your function
        dataset_id = insert_dataset("Test Dataset", "Research Data", "Internal Source")
        if dataset_id:
            print(f"  Dataset: ✅ Inserted dataset #{dataset_id}")
        else:
            print(f"  Dataset: ❌ Failed to insert dataset")
    except Exception as e:
        print(f"  Dataset: ❌ Failed - {e}")
    
    print("  Ticket: ⏸️  Skipped")
    
    # Test 4: Check Data
    print("\n[TEST 4] Data Verification")
    cursor = conn.cursor()
    tables = ['cyber_incidents', 'datasets_metadata', 'it_tickets']
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  {table}: {count} rows")
    
    conn.close()
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)

def reset_database():
    """Completely reset the database for fresh start"""
    print("\n🔄 RESETTING DATABASE...")
    
    # Completely remove the database file to ensure clean start
    if DB_PATH.exists():
        DB_PATH.unlink()
        print("✅ Database file deleted completely")
    
    # Recreate connection like to create new file 
    conn = connect_database()
    conn.close()
    print("✅ Database reset complete!")

def check_csv_paths():
    """Check where the CSV files are supposed to be"""
    print("\n🔍 CHECKING CSV PATHS")
    print("=" * 50)
    

    # Define a dictionary of file descriptions and their paths
    files = {
        "Cyber Incidents": CYBER_INCIDENTS_CSV,
        "Datasets Metadata": DATASETS_METADATA_CSV,
        "IT Tickets": IT_TICKETS_CSV
    }
    
    for name, path in files.items():
        exists = "✅ EXISTS" if path.exists() else "❌ MISSING"
        print(f"{name}: {exists}")   # Print the file name and its existence status
        print(f"   Looking in: {path}")
        print()

def debug_current_schema():
    """Check what schema is actually being used"""
    print("\n🔍 CHECKING CURRENT SCHEMA.PY")
    print("=" * 50)
    
    # Construct the Path object for the schema.py file relative to the current script
    schema_file = Path(__file__).parent / "app" / "data" / "schema.py"
    print(f"Schema file: {schema_file}")
    print(f"Exists: {schema_file.exists()}")
    
    if schema_file.exists():
        with open(schema_file, 'r') as f:
            content = f.read()

            # Check if it has the correct table definitions
            if "Title TEXT" in content and "Date TEXT" in content:
                print("✅ Schema appears to have correct column names")
            else:
                print("❌ Schema has wrong column names")
                
            # Show a snippet of the cyber_incidents table
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'cyber_incidents' in line.lower():
                    print(f"\nCyber incidents table snippet:")
                    for j in range(i, min(i+10, len(lines))):
                        print(f"  {lines[j]}")
                    break


# The structure should execute setup first and then run tests using the database 
if __name__ == "__main__":
    debug_current_schema()
    check_csv_paths()
    reset_database()
    setup_database_complete()
    run_comprehensive_tests()
  

  