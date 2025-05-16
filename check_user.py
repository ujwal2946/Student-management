from app_fixed import create_app, db, User

app = create_app()
with app.app_context():
    user = User.query.filter_by(username='UKVM').first()
    print(f"User found: {user}")
    if user:
        print(f"Password hash: {user.password_hash}")
