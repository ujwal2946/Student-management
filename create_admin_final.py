import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = 'studentdbms/studentdb.db'

def create_admin():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if admin exists
    cursor.execute("SELECT * FROM user WHERE username='UKVM'")
    if cursor.fetchone():
        print("UKVM user already exists")
        return
    
    # Create UKVM user
    password_hash = generate_password_hash('501')
    cursor.execute(
        "INSERT INTO user (username, password_hash) VALUES (?, ?)",
        ('UKVM', password_hash)
        )
    conn.commit()
    print("UKVM user created successfully")
    conn.close()

if __name__ == '__main__':
    create_admin()
