from app_fixed import app, db
from models import User

def create_test_user():
    with app.app_context():
        try:
            # Create database tables if they don't exist
            db.create_all()
            
            # Check if test user already exists
            if not User.query.filter_by(username='admin').first():
                test_user = User(username='admin')
                test_user.password = 'admin123'  # This will be hashed automatically
                db.session.add(test_user)
                db.session.commit()
                print("Test user created successfully")
            else:
                print("Test user already exists")
        except Exception as e:
            print(f"Error creating test user: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    create_test_user()
