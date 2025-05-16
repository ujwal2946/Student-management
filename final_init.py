import os
import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = 'studentdbms/studentdb.db'

def initialize_database():
    # Remove existing database if exists
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    
    # Create connection
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create all tables with proper schema
    tables = [
        """CREATE TABLE user (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )""",
        """CREATE TABLE student (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            dob TEXT NOT NULL,
            parent_email TEXT NOT NULL,
            address TEXT,
            enroll_date TEXT
        )""",
        """CREATE TABLE attendance (
            id INTEGER PRIMARY KEY,
            student_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            status INTEGER DEFAULT 1,
            remarks TEXT,
            FOREIGN KEY(student_id) REFERENCES student(id)
        )""",
        """CREATE TABLE grade (
            id INTEGER PRIMARY KEY,
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            score REAL NOT NULL,
            semester TEXT,
            date_recorded TEXT,
            FOREIGN KEY(student_id) REFERENCES student(id)
        )"""
    ]
    
    for table in tables:
        cursor.execute(table)
    
    # Create UKVM user with password 501
    cursor.execute(
        "INSERT INTO user (username, password_hash) VALUES (?, ?)",
        ('UKVM', generate_password_hash('501'))
    )
    
    conn.commit()
    conn.close()
    print("Database initialized with UKVM user and all tables")

if __name__ == '__main__':
    initialize_database()
