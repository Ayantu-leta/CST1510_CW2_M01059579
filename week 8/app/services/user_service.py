import bcrypt
from pathlib import Path
from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user

def register_user(username, password, role='user'):
    """Register new user with password hashing."""
    # Input validation
    if not username or not password:
        return False, "Username and password are required."
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    
   # Hash password securely using bcrypt and Start a block for hashing and database insertion

    try:
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        password_hash = hashed.decode('utf-8')
        
        # Insert the new users into the database
        success, message = insert_user(username, password_hash, role)
        return success, message
    except Exception as e:
        return False, f"Registration error: {e}"

def login_user(username, password):
    """Authenticate user against database."""
    if not username or not password:
        return False, "Username and password are required."
    
    # Retrieve user record and checks if user was found
    user = get_user_by_username(username)
    if not user:
        return False, "User not found."
    
  # Verify password against the stored hash and user[2] is the stored password hash
    stored_hash = user[2]
    user_role = user[3]  # role is at index 3
    
    # Start a block for password verification and check if the entered password matches the stored hash
    try:
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
            return True, f"Login successful! Role: {user_role}"
        else:
            return False, "Incorrect password."
    except Exception as e:
        return False, f"Authentication error: {e}"

def migrate_users_from_file(filepath="/Users/ayu/CST1510_CW2_M01059579/week 7/users.txt"):
    """
    Migrate users from a text file to the database.
    Expected file format: username,password,role
    """
    file_path = Path(filepath)
    
    if not file_path.exists():
        print(f"❌ Users file not found: {file_path}")
        return 0
    # Start block for file reading and processing Open and read file lines
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        migrated_count = 0
        skipped_count = 0
        
        print(f"📖 Reading users from: {file_path}")
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()

           # Skip empty lines and comments starting with '#'
            if not line or line.startswith('#'):
                continue
           
            parts = line.split(',')   # Split line into parts
            if len(parts) == 3:
                username, password, role = parts
                username = username.strip()
                password = password.strip() 
                role = role.strip()
                
                # Check for existing user to prevent duplicates and If user exists, skip
                existing_user = get_user_by_username(username)
                if existing_user:
                    print(f"⏭️  User {username} already exists, skipping...")
                    skipped_count += 1
                    continue
                
                # Register the new user securely includes hashing
                success, message = register_user(username, password, role)
                if success:
                    migrated_count += 1
                    print(f"✅ [{line_num}] Migrated user: {username} ({role})")
                else:
                    print(f"❌ [{line_num}] Failed to migrate {username}: {message}")
            else:
                print(f"⚠️  [{line_num}] Invalid format: {line}")
        
        # Print a summary of the migration results
        print(f"\n📊 Migration Summary:")
        print(f"   ✅ Successfully migrated: {migrated_count} users")
        print(f"   ⏭️  Skipped (already exist): {skipped_count} users")
        print(f"   📝 Total processed: {len([l for l in lines if l.strip() and not l.strip().startswith('#')])} lines")
        
        return migrated_count
        
    except Exception as e:
        print(f"❌ Error migrating users: {e}")
        return 0

def change_user_password(username, new_password):
    """Change a user's password."""
    
    # Start block for hashing and database update
    # Hash the new password securely with a new salt
    try:
        password_bytes = new_password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        new_password_hash = hashed.decode('utf-8')
        
        # Update the hash in the database
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET password_hash = ? WHERE username = ?",
            (new_password_hash, username)
        )
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        
        if affected > 0:
            return True, "Password updated successfully"
        else:
            return False, "User not found"
          
        # Catch exceptions during password change
    except Exception as e:
        return False, f"Error changing password: {e}"

def list_all_users():
    """List all users in the system (for admin purposes)"""

    # Start block for retrieving data and Connect to DB
    try:
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role, created_at FROM users ORDER BY id")
        users = cursor.fetchall()
        conn.close()
        
        return users
    except Exception as e:
        print(f"Error listing users: {e}")
        return []  # Return empty list on failure