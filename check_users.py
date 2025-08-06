from app import create_app
from models import User, db

app = create_app()

with app.app_context():
    users = User.query.all()
    print(f"Total users: {len(users)}")
    
    if users:
        print("\nUser list:")
        for user in users:
            print(f"ID: {user.id}, Email: {user.email}, Role: {user.role}")
    else:
        print("No users found in the database.")