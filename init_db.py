import sys
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent))

from studentdbms.app_fixed import app, db, User

with app.app_context():
    # Create all database tables
    db.create_all()
    
    # Create admin user if it doesn't exist
    if not User.query.filter_by(username='UKVM').first():
        admin = User(username='UKVM')
        admin.set_password('501')
        db.session.add(admin)
        db.session.commit()
        print("Created admin user UKVM with password '501'")
    else:
        print("Admin user already exists")
