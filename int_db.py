from app_fixed import app, db
from models import User
from werkzeug.security import generate_password_hash

def initialize():
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Create admin user
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin')
            admin.password_hash = generate_password_hash('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created")
        else:
            print("ℹ️ Admin user already exists")

if __name__ == '__main__':
    initialize()