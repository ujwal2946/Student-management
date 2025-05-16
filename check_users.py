from app_fixed import create_app
from models import User

app = create_app()

with app.app_context():
    users = User.query.all()
    if not users:
        print("No users found in database")
    else:
        print(f"Found {len(users)} user(s):")
        for user in users:
            print(f"- ID: {user.id}, Username: {user.username}")
