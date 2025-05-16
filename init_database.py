import os
import sys
from pathlib import Path

# Add both project root and studentdbms directory to Python path
project_root = str(Path(__file__).resolve().parent)
studentdbms_path = os.path.join(project_root, 'studentdbms')
sys.path.extend([project_root, studentdbms_path])

from extensions import db
from app_fixed import app

with app.app_context():
    db.create_all()
    print("Database tables created successfully")
