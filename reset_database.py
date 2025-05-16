from app_fixed import create_app
from extensions import db

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Database reset successfully")
