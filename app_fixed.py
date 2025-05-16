from flask import Flask
import os
from dotenv import load_dotenv
from extensions import db, mail, csrf, login_manager

def create_app():
    load_dotenv()
    app = Flask(__name__)
    
    # Configuration
    app.config.update(
        SECRET_KEY=os.getenv('SECRET_KEY') or 'dev-secret-key',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 'studentdb.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        WTF_CSRF_ENABLED=True,
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USERNAME='student29system@gmail.com',
        MAIL_PASSWORD='pabs mbvm cemo ktuy',
        MAIL_DEFAULT_SENDER='student29system@gmail.com'
    )

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    with app.app_context():
        from models import User, Student, Attendance, Grade
        db.create_all()

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        from routes import init_routes
        init_routes(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5005, host='0.0.0.0')
