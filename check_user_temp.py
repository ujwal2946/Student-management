import sys
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent))

from studentdbms.app_fixed import app, db, User

with app.app_context():
    user = User.query.filter_by(username='UKVM').first()
    print(f"User found: {user}")
    if user:
        print(f"Password hash: {user.password_hash}")
