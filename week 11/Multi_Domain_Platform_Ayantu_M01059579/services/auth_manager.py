# services/auth_manager.py
from typing import Optional
from models.user import User
from services.database_manager import DatabaseManager
import bcrypt
import hashlib

class SimpleHasher:
    def hash_password(plain: str) -> str:
        return hashlib.sha256(plain.encode("utf-8")).hexdigest()

    def check_password(plain: str, hashed: str) -> bool:
        return SimpleHasher.hash_password(plain) == hashed

class AuthManager:
    def __init__(self, db: DatabaseManager):
        self._db = db

    def login_user(self, username: str, password: str) -> Optional[User]:
        row = self._db.fetch_one(
            "SELECT username, password_hash, role FROM users WHERE username = ?",
            (username,)
        )
        
        if row is None:
            return None
        
        username_db, password_hash_db, role_db = row
        
        if password_hash_db.startswith('$2'):
            password_bytes = password.encode('utf-8')
            hash_bytes = password_hash_db.encode('utf-8')
            
            if bcrypt.checkpw(password_bytes, hash_bytes):
                return User(username_db, password_hash_db, role_db)
            else:
                return None
        else:
            if SimpleHasher.check_password(password, password_hash_db):
                return User(username_db, password_hash_db, role_db)
            else:
                return None

    def register_user(self, username: str, password: str, role: str = "user") -> bool:
        existing = self._db.fetch_one("SELECT id FROM users WHERE username = ?", (username,))
        if existing is not None:
            return False
  
        password_bytes = password.encode('utf-8')
        password_hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')
        
        self._db.execute_query(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role)
        )
   
        check_user = self._db.fetch_one("SELECT id FROM users WHERE username = ?", (username,))
        if check_user:
            return True
        else:
            return False