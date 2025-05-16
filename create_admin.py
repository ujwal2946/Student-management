from flask import Flask
from extensions import db
from models import User
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studentdb_fresh.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def create_admin():
    with app.app_context():
        # Create admin user if doesn't exist
        if not User.query.filter_by(username='UKVM').first():
            admin = User(
                username='UKVM',
                password_hash=generate_password_hash('501')
            )
            db.session.add(admin)
            db.session.commit()
            print("UKVM user created successfully")
        else:
            print("UKVM user already exists")
        
if __name__ == '__main__':
    create_admin()
