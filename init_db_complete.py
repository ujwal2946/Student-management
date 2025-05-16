from app_fixed import create_app
from extensions import db
from models import User
from werkzeug.security import generate_password_hash

def initialize_database():
    app = create_app()
    with app.app_context():
        # Create all database tables
        db.create_all()
        
        # Create admin user if doesn't exist
        if not User.query.filter_by(username='UKVM').first():
            admin = User(
                username='UKVM',
                password_hash=generate_password_hash('501')
            )
            db.session.add(admin)
            db.session.commit()
            print("Database initialized successfully")
            print("Admin user created: UKVM/501")
        else:
            print("Database already initialized")
            print("Admin user exists: UKVM/501")

if __name__ == '__main__':
    initialize_database()
