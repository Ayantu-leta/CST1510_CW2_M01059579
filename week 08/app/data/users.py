import sqlite3
from app.data.db import connect_database

def get_user_by_username(username):

    """ Retrieve user by username """

    conn = connect_database()
    cursor = conn.cursor()

    # Execute a parameterized query to securely find the user
    # using '?' as a placeholder to prevent SQL injection
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()   # Fetch the single user record 
    conn.close()
    return user

def insert_user(username, password_hash, role='user'):

    """Insert new user into database"""

    conn = connect_database()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role)
        )
        conn.commit() # to Save the new record
        return True, f"User '{username}' created successfully"
    
    except sqlite3.IntegrityError:
        # This error is caught if the database has a UNIQUE constraint on 'username' 
        # like if a user with that username already exists
        return False, f"Username '{username}' already exists"
    except sqlite3.Error as e:
        # Catch any other database related errors
        return False, f"Database error: {e}"
    finally:
        conn.close()

def get_all_users():

    """ Get all users from database """

    conn = connect_database()
    cursor = conn.cursor()

    # Select key user details sensitive password hash
    cursor.execute("SELECT id, username, role FROM users ORDER BY id")
    users = cursor.fetchall()
    conn.close()
    return users

def delete_user(username):

    """ Delete user by username """

    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()

    #  it will returns True if one or more rows were deleted False otherwise
    return affected > 0