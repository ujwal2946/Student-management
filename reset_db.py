from studentdbms.app_fixed import app, db

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Database tables reset successfully")
