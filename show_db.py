from studentdbms.models import db, User, Student, Attendance, Grade
from studentdbms.extensions import app
from datetime import datetime

def print_table(title, query_result):
    print(f"\n=== {title} ===")
    if not query_result:
        print("No records found")
        return
    for record in query_result:
        print(record.__dict__)

with app.app_context():
    # Connect to database
    db.init_app(app)
    
    # Query all tables
    users = User.query.all()
    students = Student.query.all()
    attendance = Attendance.query.all()
    grades = Grade.query.all()
    
    # Print results
    print_table("USERS", users)
    print_table("STUDENTS", students)
    print_table("ATTENDANCE RECORDS", attendance)
    print_table("GRADES", grades)
