import os
import sys
import time
import shutil
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from studentdbms.app_fixed import app, db

def force_reset_database():
    db_file = os.path.join(os.path.dirname(__file__), 'studentdb.db')
    backup_file = os.path.join(os.path.dirname(__file__), 'studentdb_backup.db')
    
    # Create backup
    if os.path.exists(db_file):
        try:
            shutil.copy2(db_file, backup_file)
            print(f"Created backup: {backup_file}")
        except Exception as e:
            print(f"Warning: Could not create backup - {e}")

    # Force delete existing database
    if os.path.exists(db_file):
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                os.remove(db_file)
                print(f"Successfully deleted database file")
                break
            except Exception as e:
                if attempt == max_attempts - 1:
                    print(f"Failed to delete database after {max_attempts} attempts")
                    print("Please close all applications and try again")
                    return False
                print(f"Attempt {attempt + 1}: Could not delete database - retrying...")
                time.sleep(1)

    # Create fresh database
    with app.app_context():
        try:
            db.create_all()
            print("Successfully created new database with all tables")
            return True
        except Exception as e:
            print(f"Failed to create new database: {e}")
            return False

if __name__ == '__main__':
    print("=== FORCE DATABASE RESET ===")
    if force_reset_database():
        print("Database reset completed successfully")
    else:
        print("Database reset failed")
