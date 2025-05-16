import os
import sqlite3
from datetime import date

DB_PATH = os.path.join(os.path.dirname(__file__), 'studentdb.db')

def reset_database():
    # Remove existing database file
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    
    # Create new database with schema
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create tables with all required columns
    cursor.execute("""
    CREATE TABLE student (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        dob DATE NOT NULL,
        parent_email TEXT NOT NULL,
        address TEXT,
        enroll_date DATE
    )
    """)
    
    cursor.execute("""
    CREATE TABLE attendance (
        id INTEGER PRIMARY KEY,
        student_id INTEGER NOT NULL,
        date DATE NOT NULL,
        status BOOLEAN DEFAULT 1,
        remarks TEXT,
        FOREIGN KEY(student_id) REFERENCES student(id)
    )
    """)
    
    conn.commit()
    conn.close()
    print("Database reset successfully with all required columns")

if __name__ == '__main__':
    reset_database()
