from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

# Create minimal Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'test-secret-key'

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)

# Define minimal User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

def setup_test_environment():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create test user if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Created test admin user")
        else:
            print("ℹ️ Test user already exists")

if __name__ == '__main__':
    print("Setting up test environment...")
    setup_test_environment()
    print("✅ Test environment ready")
    print("You can now run the main application")
