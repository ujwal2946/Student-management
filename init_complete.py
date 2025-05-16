import os
import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = 'studentdbms/studentdb.db'

def init_database():
    # Remove existing database if exists
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        
    # Create new database with all tables
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create User table
    cursor.execute("""
    CREATE TABLE user (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
    """)
    
    # Create Student table
    cursor.execute("""
    CREATE TABLE student (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        dob TEXT NOT NULL,
        parent_email TEXT NOT NULL,
        address TEXT,
        enroll_date TEXT
    )
    """)
    
    # Create other tables...
    
    # Create admin user
    password_hash = generate_password_hash('admin123')
    cursor.execute(
        "INSERT INTO user (username, password_hash) VALUES (?, ?)",
        ('admin', password_hash)
    )
    
    conn.commit()
    conn.close()
    print("Database initialized successfully with admin user")

if __name__ == '__main__':
    init_database()
