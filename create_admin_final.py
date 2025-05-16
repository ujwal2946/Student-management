import os
import sys
from pathlib import Path
from datetime import datetime
from werkzeug.security import generate_password_hash
from sqlalchemy import text

# Add project paths
project_root = str(Path(__file__).resolve().parent)
studentdbms_path = os.path.join(project_root, 'studentdbms')
sys.path.extend([project_root, studentdbms_path])

from extensions import db
from app_fixed import app

def create_admin():
    with app.app_context():
        # Check if admin exists
        result = db.session.execute(
            text("SELECT id FROM users WHERE username = 'UKVM'")
        ).fetchone()
        
        if result:
            print("Admin user already exists")
            return

        # Create admin user
        password_hash = generate_password_hash('501')
        current_time = datetime.utcnow()
        
        db.session.execute(
            text("""
                INSERT INTO users (username, password_hash, created_at) 
                VALUES (:username, :password_hash, :created_at)
            """),
            {
                'username': 'UKVM',
                'password_hash': password_hash,
                'created_at': current_time
            }
        )
        db.session.commit()
        print("Admin user created successfully")

if __name__ == '__main__':
    create_admin()
