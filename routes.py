from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, date
from flask_mail import Message
from extensions import db, mail
from models import User, Student, Attendance, Grade

def init_routes(app):
    main_bp = Blueprint('main', __name__)

    @main_bp.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')
            
            if not username or not password:
                flash('Username and password are required')
                return render_template('login.html')
                
            user = User.query.filter_by(username=username).first()
            
            if not user:
                flash('Username not found')
                return render_template('login.html')
                
            if user.verify_password(password):
                login_user(user)
                user.last_login = datetime.utcnow()
                db.session.commit()
                return redirect(url_for('main.dashboard'))
            else:
                flash('Incorrect password')
                
        return render_template('login.html')
                
    @main_bp.route('/logout', methods=['POST'])
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out successfully', 'success')
        return redirect(url_for('main.login'))

    @main_bp.route('/dashboard')
    @login_required
    def dashboard():
        student_count = Student.query.count()
        return render_template('minimal_dashboard.html', student_count=student_count)

    @main_bp.route('/students', methods=['GET'])
    @login_required
    def students():
        search_query = request.args.get('search', '').strip()
        if search_query:
            # Search by ID (exact match) or name/parent_email (partial matches)
            students = Student.query.filter(
                db.or_(
                    Student.id == int(search_query) if search_query.isdigit() else None,
                    Student.name.ilike(f'%{search_query}%'),
                    Student.parent_email.ilike(f'%{search_query}%')
                )
            ).order_by(Student.id.asc()).all()
        else:
            students = Student.query.order_by(Student.id.asc()).all()
        return render_template('students.html', students=students, search_query=search_query)
            
    @main_bp.route('/add_student', methods=['GET', 'POST'])
    @login_required
    def add_student():
        if request.method == 'POST':
            try:
                new_student = Student(
                    id=int(request.form['id']),
                    name=request.form['name'],
                    dob=datetime.strptime(request.form['dob'], '%Y-%m-%d').date(),
                    gender=request.form['gender'],
                    parent_email=request.form['parent_email'],
                    class_=request.form.get('class', '')
                )
                db.session.add(new_student)
                db.session.commit()
                flash('Student added successfully', 'success')
                return redirect(url_for('main.students'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error adding student: {str(e)}', 'error')
        return render_template('add_student.html')
        
    @main_bp.route('/edit_student/<int:id>', methods=['GET', 'POST'])
    @login_required
    def edit_student(id):
        student = Student.query.get_or_404(id)
        classes = ["10-A", "10-B", "10-C", "11-A", "11-B", "11-C", "12-A", "12-B", "12-C"]  # Add all classes here
        if request.method == 'POST':
            try:
                # Validate form data first
                if not all(field in request.form for field in ['id', 'name', 'dob', 'gender', 'parent_email']):
                    flash('All fields are required', 'error')
                    return render_template('edit_student.html', student=student, classes=classes)
                    
                # Update student data including ID
                new_id = int(request.form['id'])
                if new_id != student.id:
                    # Check if new ID already exists
                    if Student.query.filter(Student.id == new_id).first():
                        flash('Student ID already exists', 'error')
                        return render_template('edit_student.html', student=student, classes=classes)
                    student.id = new_id
                
                student.name = request.form['name'].strip()
                student.dob = datetime.strptime(request.form['dob'], '%Y-%m-%d').date()
                student.gender = request.form['gender']
                student.parent_email = request.form['parent_email'].strip()
                student.class_ = request.form.get('class', '')
                # Verify changes before committing
                if not student.name or not student.parent_email:
                    flash('Name and parent email cannot be empty', 'error')
                    return render_template('edit_student.html', student=student, classes=classes)
                    
                db.session.commit()
                flash('Student updated successfully', 'success')
                return redirect(url_for('main.students'))
            except ValueError:
                db.session.rollback()
                flash('Invalid date format. Please use YYYY-MM-DD', 'error')
            except Exception as e:
                db.session.rollback()
                flash(f'Error updating student: {str(e)}', 'error')
        return render_template('edit_student.html', student=student, classes=classes)

    @main_bp.route('/attendance')
    @login_required
    def attendance():
        attendance_records = db.session.query(Attendance, Student).join(Student).order_by(Attendance.date.desc()).all()
        return render_template('attendance.html', attendance=attendance_records)
    
    @main_bp.route('/mark_attendance', methods=['GET', 'POST'])
    @login_required
    def mark_attendance():
        if request.method == 'POST':
            try:
                student = Student.query.get(request.form['student_id'])
                status = 'Present' if request.form['status'] == 'present' else 'Absent'
                new_attendance = Attendance(
                    student_id=request.form['student_id'],
                    date=datetime.strptime(request.form['date'], '%Y-%m-%d').date(),
                    status=status == 'Present'
                )
                db.session.add(new_attendance)
                db.session.commit()
                
                # Send notification to parent only if absent
                if status == 'Absent':
                    try:
                        msg = Message(
                            subject=f"Absence Notification for {student.name}",
                            recipients=[student.parent_email],
                            body=f"""Your child {student.name} was marked absent on:
Date: {request.form['date']}
Please contact the school if this is unexpected."""
                        )
                        mail.send(msg)
                    except Exception as e:
                        print(f"Failed to send email: {str(e)}")
                    
                flash('Attendance marked successfully', 'success')
                return redirect(url_for('main.attendance'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error marking attendance: {str(e)}', 'error')
        
        students = Student.query.order_by(Student.name).all()
        return render_template('mark_attendance.html', students=students)

    @main_bp.route('/grades')
    @login_required
    def grades():
        grades = db.session.query(Grade, Student).join(Student).order_by(Grade.subject).all()
        return render_template('grades.html', grades=grades)
    
    @main_bp.route('/add_grade', methods=['GET', 'POST'])
    @login_required
    def add_grade():
        if request.method == 'POST':
            try:
                new_grade = Grade(
                    student_id=request.form['student_id'],
                    subject=request.form['subject'],
                    score=float(request.form['score'])
                )
                db.session.add(new_grade)
                db.session.commit()
                flash('Grade added successfully', 'success')
                return redirect(url_for('main.grades'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error adding grade: {str(e)}', 'error')
        
        students = Student.query.order_by(Student.name).all()
        return render_template('add_grade.html', students=students)

    @main_bp.route('/edit_grade/<int:id>', methods=['GET', 'POST'])
    @login_required
    def edit_grade(id):
        grade = Grade.query.get_or_404(id)
        if request.method == 'POST':
            try:
                grade.student_id = request.form['student_id']
                grade.subject = request.form['subject']
                grade.score = float(request.form['score'])
                db.session.commit()
                flash('Grade updated successfully', 'success')
                return redirect(url_for('main.grades'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error updating grade: {str(e)}', 'error')
        
        students = Student.query.order_by(Student.name).all()
        return render_template('edit_grade.html', 
                            grade=grade,
                            students=students)
    @main_bp.route('/delete_grade/<int:id>', methods=['POST'])
    @login_required
    def delete_grade(id):
        grade = Grade.query.get_or_404(id)
        db.session.delete(grade)
        db.session.commit()
        flash('Grade deleted successfully', 'success')
        return redirect(url_for('main.grades'))
    @main_bp.route('/delete_student/<int:id>', methods=['POST'])
    @login_required
    def delete_student(id):
        student = Student.query.get_or_404(id)
        db.session.delete(student)
        db.session.commit()
        flash('Student deleted successfully', 'success')
        return redirect(url_for('main.students'))

    @main_bp.route('/edit_attendance/<int:id>', methods=['GET', 'POST'])
    @login_required
    def edit_attendance(id):
        attendance = Attendance.query.get_or_404(id)
        if request.method == 'POST':
            try:
                student = Student.query.get(attendance.student_id)
                status = 'Present' if request.form['status'] == 'present' else 'Absent'
                attendance.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
                attendance.status = status == 'Present'
                db.session.commit()
                
                # Send notification to parent only if changed to absent
                was_present = attendance.status
                is_absent = status == 'Absent'
                if is_absent and not was_present:
                    try:
                        msg = Message(
                            subject=f"Absence Notification for {student.name}",
                            recipients=[student.parent_email],
                            body=f"""Your child {student.name} was marked absent on:
Date: {request.form['date']}
Please contact the school if this is unexpected."""
                        )
                        mail.send(msg)
                    except Exception as e:
                        print(f"Failed to send email: {str(e)}")
                    
                flash('Attendance updated successfully', 'success')
                return redirect(url_for('main.attendance'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error updating attendance: {str(e)}', 'error')
        
        students = Student.query.order_by(Student.name).all()
        return render_template('edit_attendance.html', 
                            attendance=attendance,
                            students=students)

    @main_bp.route('/delete_attendance/<int:id>', methods=['POST'])
    @login_required
    def delete_attendance(id):
        attendance = Attendance.query.get_or_404(id)
        db.session.delete(attendance)
        db.session.commit()
        flash('Attendance record deleted successfully', 'success')
        return redirect(url_for('main.attendance'))
            
    @main_bp.route('/')
    def home():
        return redirect(url_for('main.login'))
        
    app.register_blueprint(main_bp)
