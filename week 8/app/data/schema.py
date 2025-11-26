def create_users_table(conn):
    """
    Create the users table if it doesn't exist.
    
    Args:
        conn: Database connection object
    """
    cursor = conn.cursor()
    # SQL statement to create users table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    cursor.execute(create_table_sql)
    conn.commit()
    print("✅ Users table created successfully!")

def create_cyber_incidents_table(conn):
    """
    Create the cyber_incidents table using CSV file names
    These column names like Title, Affiliations and the rest match the headers 
 
    """
    # TODO: Get a cursor from the connection
    cursor = conn.cursor()

    # TODO: Write CREATE TABLE IF NOT EXISTS SQL statement
    # Follow the pattern from create_users_table()
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS cyber_incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Title TEXT,
        Date TEXT,
        Affiliations TEXT,
        Description TEXT,
        Response TEXT,
        Victims TEXT,
        Sponsor TEXT,
        Type TEXT,
        Category TEXT,
        Sources_1 TEXT,
        Sources_2 TEXT,
        Sources_3 TEXT,
        severity TEXT,
        status TEXT,
        reported_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (reported_by) REFERENCES users(username)
    )
    """
     # TODO: Execute the SQL statement
    cursor.execute(create_table_sql)

     # TODO: Commit the changes
    conn.commit()

    # TODO: Print success message
    print("✅ Cyber incidents table created successfully!")

def create_datasets_metadata_table(conn):
    """
    Create the datasets_metadata table using custom CSV file names.
    These column names like votes, owner match the headers 
 
    """

     # TODO: Implement following the users table pattern
    cursor = conn.cursor()
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS datasets_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Kernel TEXT NOT NULL,
        Votes INTEGER,
        Owner INTEGER,
        dataset TEXT,
        Version_History TEXT,
        Tags TEXT,
        Output TEXT,
        Code_Type INTEGER,
        Language TEXT,
        Comments TEXT,
        Views TEXT,
        Forks INTEGER
        
    )
    """
    cursor.execute(create_table_sql)
    conn.commit()
    print("✅ Datasets metadata table created successfully!")

def create_it_tickets_table(conn):
    """
    Create the it_tickets table using custom CSV file names.
    These column names like Customer_Input, Possible_Resolutions1
    match the headers in your CSV file.
    """
    cursor = conn.cursor()
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS it_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Customer_Input TEXT,
        Category TEXT,
        Ticket_Type TEXT,
        Possible_Resolutions1 TEXT,
        Customer_Input_2 TEXT,
        Category_2 TEXT,
        Ticket_Type_2 TEXT,
        Possible_Resolution TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    cursor.execute(create_table_sql)
    conn.commit()
    print("✅ IT tickets table created successfully!")

def create_all_tables(conn):
    """
    Drops existing tables and recreates the entire schema.
    
    Args:
        conn: Database connection object
    """
    cursor = conn.cursor()
    tables = ['users', 'cyber_incidents', 'datasets_metadata', 'it_tickets']
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")
    conn.commit()
    print("✅ Dropped all existing tables")
    
    # Create all tables with current schemas
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)
    print("✅ All tables created successfully!")