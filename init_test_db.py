from app_fixed import app
from extensions import db
from models import User
from werkzeug.security import generate_password_hash

def initialize_database():
    """Initialize database and create test user"""
    with app.app_context():
        try:
            print("Creating database tables...")
            db.create_all()
            
            # Create admin user if doesn't exist
            if not db.session.query(User).filter_by(username='admin').first():
                admin = User(
                    username='admin',
                    password_hash=generate_password_hash('admin123')
                )
                db.session.add(admin)
                db.session.commit()
                print("✅ Created admin user (username: admin, password: admin123)")
            else:
                print("ℹ️ Admin user already exists")
                
        except Exception as e:
            print(f"❌ Error initializing database: {str(e)}")
            db.session.rollback()
        finally:
            db.session.close()

if __name__ == '__main__':
    print("Starting database initialization...")
    initialize_database()
    print("Initialization complete")