import sqlite3
from pprint import pprint

def show_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("\nDATABASE TABLES AND CONTENTS:")
    for table in tables:
        table_name = table[0]
        print(f"\n=== TABLE: {table_name} ===")
        
        # Get table structure
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        print("COLUMNS:")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
        
        # Get table contents
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()
        print("\nDATA:")
        for row in rows:
            pprint(row)
    
    conn.close()

# Connect to the main database file
show_database("studentdbms/studentdb.db")
