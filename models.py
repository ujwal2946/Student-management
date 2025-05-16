from extensions import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False
        
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False, default='Male')  # Added gender field
    parent_email = db.Column(db.String(100), nullable=False)
    class_ = db.Column(db.String(10), nullable=True)  # Stores class like 10-A, 11-B etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    VALID_CLASSES = ['10-A', '10-B', '10-C', '11-A', '11-B', '11-C']
    
    @property
    def display_id(self):
        """Returns sequential position based on creation date"""
        students = Student.query.order_by(Student.created_at).all()
        return students.index(self) + 1
        
class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    student = db.relationship('Student', backref=db.backref('attendance_records', cascade='all, delete-orphan'))
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Boolean, default=False)  # False=Absent, True=Present
    notified = db.Column(db.Boolean, default=False)
    
class Grade(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    student = db.relationship('Student', backref=db.backref('grades', cascade='all, delete-orphan'))
    subject = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Float, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
