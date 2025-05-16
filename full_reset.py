import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create minimal Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studentdb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define all models matching app_fixed.py
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    parent_email = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(200))
    enroll_date = db.Column(db.Date, default=lambda: date.today())

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Boolean, default=True)
    remarks = db.Column(db.String(200))

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Float, nullable=False)
    semester = db.Column(db.String(20))
    date_recorded = db.Column(db.Date, default=lambda: date.today())

def reset_database():
    with app.app_context():
        db_file = os.path.join(os.path.dirname(__file__), 'studentdb.db')
        if os.path.exists(db_file):
            os.remove(db_file)
        db.create_all()
        print("Database fully reset with all tables")

if __name__ == '__main__':
    from datetime import date
    reset_database()
