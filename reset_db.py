import os
import sys
import shutil
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from studentdbms.app_fixed import app, db

def reset_database():
    db_file = os.path.join(os.path.dirname(__file__), 'studentdb.db')
    temp_file = os.path.join(os.path.dirname(__file__), 'studentdb_temp.db')
    
    # Create a temporary copy of the database
    if os.path.exists(db_file):
        try:
            shutil.copy2(db_file, temp_file)
            print(f"Created temporary copy: {temp_file}")
        except Exception as e:
            print(f"Failed to create temporary copy: {e}")
            return False
    
    # Create new database
    with app.app_context():
        db.create_all()
        print("Successfully created new database with all tables")
    
    return True

if __name__ == '__main__':
    if reset_database():
        print("Database reset completed successfully")
    else:
        print("Database reset failed - please try again or restart your system")
