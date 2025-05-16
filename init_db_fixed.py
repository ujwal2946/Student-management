import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Set up the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studentdb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define models (same as in app_fixed.py)
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # Add other columns as needed

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add other columns as needed

def init_db():
    with app.app_context():
        db.create_all()
        print("Database tables created successfully")

if __name__ == '__main__':
    init_db()
