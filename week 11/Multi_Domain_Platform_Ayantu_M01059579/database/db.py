# database/db.py
import sqlite3
import os
import bcrypt

def create_tables():
    """Create all necessary tables for the platform."""

    os.makedirs("database", exist_ok=True)

    with sqlite3.connect("database/platform.db") as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS security_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_type TEXT NOT NULL,
            severity TEXT CHECK(severity IN ('low', 'medium', 'high', 'critical')),
            status TEXT DEFAULT 'open',
            description TEXT,
            reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS datasets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            size_bytes INTEGER,
            rows INTEGER,
            source TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        cursor.execute("DROP TABLE IF EXISTS it_tickets")
        cursor.execute('''
        CREATE TABLE it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            priority TEXT CHECK(priority IN ('low', 'medium', 'high', 'urgent')),
            status TEXT DEFAULT 'open',
            assigned_user_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (assigned_user_id) REFERENCES users(id)
        )
        ''')
        #inserting sample data
        ali_hash = bcrypt.hashpw(b"ali123", bcrypt.gensalt()).decode('utf-8')
        helen_hash = bcrypt.hashpw(b"helen123", bcrypt.gensalt()).decode('utf-8')
        bob_hash = bcrypt.hashpw(b"bob123", bcrypt.gensalt()).decode('utf-8')
        maria_hash = bcrypt.hashpw(b"maria123", bcrypt.gensalt()).decode('utf-8')
        
        cursor.executemany('''
        INSERT OR IGNORE INTO users (username, password_hash, role) 
        VALUES (?, ?, ?)
        ''', [
            ('ali', ali_hash, 'admin'),
            ('helen', helen_hash, 'user'),
            ('bob', bob_hash, 'user'),
            ('maria', maria_hash, 'user')
        ])

        cursor.executemany('''
        INSERT OR IGNORE INTO security_incidents (incident_type, severity, status, description)
        VALUES (?, ?, ?, ?)
        ''', [
            ('Malware Infection', 'high', 'open', 'Ransomware detected on endpoint device'),
            ('Phishing Attempt', 'medium', 'investigating', 'Suspicious email campaign targeting employees'),
            ('Unauthorized Access', 'critical', 'resolved', 'External IP attempted SSH brute force'),
            ('Data Leak', 'high', 'open', 'Sensitive documents found on public server')
        ])

        cursor.executemany('''
        INSERT OR IGNORE INTO datasets (name, size_bytes, rows, source)
        VALUES (?, ?, ?, ?)
        ''', [
            ('Customer Analytics', 104857600, 500000, 'Sales Database'),
            ('Network Logs', 52428800, 1000000, 'Firewall'),
            ('Employee Performance', 20971520, 10000, 'HR System')
        ])

        conn.commit()
