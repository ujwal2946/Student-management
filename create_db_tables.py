import sys
sys.path.insert(0, 'c:/Users/chiru/OneDrive/Desktop/projects')

from studentdbms.extensions import db
from studentdbms.app_fixed import app

with app.app_context():
    db.create_all()
    print("Database tables created successfully")
