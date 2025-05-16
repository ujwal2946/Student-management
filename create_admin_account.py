import sys
from pathlib import Path
from werkzeug.security import generate_password_hash

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

from studentdbms.app_fixed import app, db
from studentdbms.models import User

def create_admin():
    with app.app_context():
        # Check if admin exists
        if User.query.filter_by(username='UKVM').first():
            print("UKVM user already exists")
            return
            
        # Create admin user
        admin = User(
            username='UKVM',
            password_hash=generate_password_hash('501'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Successfully created UKVM admin account")

if __name__ == '__main__':
    create_admin()
