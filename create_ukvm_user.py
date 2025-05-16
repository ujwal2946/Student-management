from studentdbms.app_fixed import app, db
from studentdbms.models import User
from werkzeug.security import generate_password_hash

def create_ukvm_user():
    with app.app_context():
        # Check if user exists
        if User.query.filter_by(username='UKVM').first():
            print("UKVM user already exists")
            return
            
        # Create new admin user
        admin = User(
            username='UKVM',
            password_hash=generate_password_hash('501'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Successfully created UKVM admin user")

if __name__ == '__main__':
    create_ukvm_user()
