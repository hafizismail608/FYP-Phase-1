#!/usr/bin/env python3
"""
Script to fix database schema and ensure all required columns exist
"""
import sqlite3
import os
from app import create_app, db
from models import User
from werkzeug.security import generate_password_hash

def add_missing_columns():
    # Get the database path
    db_path = os.path.join(os.path.dirname(__file__), 'site.db')
    
    if not os.path.exists(db_path):
        print(f"Database file not found at {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Add columns to user table
        print("Adding columns to user table...")
        try:
            cursor.execute("ALTER TABLE user ADD COLUMN is_protected BOOLEAN DEFAULT 0")
            print("✓ Added is_protected column")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("✓ is_protected column already exists")
            else:
                print(f"Error adding is_protected: {e}")
        
        try:
            cursor.execute("ALTER TABLE user ADD COLUMN last_login DATETIME")
            print("✓ Added last_login column")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("✓ last_login column already exists")
            else:
                print(f"Error adding last_login: {e}")
        
        try:
            cursor.execute("ALTER TABLE user ADD COLUMN login_count INTEGER DEFAULT 0")
            print("✓ Added login_count column")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("✓ login_count column already exists")
            else:
                print(f"Error adding login_count: {e}")
        
        # Ensure super_admin role exists in the user table
        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user'")
            if cursor.fetchone():
                # Check if the role column accepts 'super_admin'
                cursor.execute("PRAGMA table_info(user)")
                columns = cursor.fetchall()
                role_column = next((col for col in columns if col[1] == 'role'), None)
                
                if role_column:
                    # Create or update the super admin user
                    cursor.execute("SELECT id, email, role, is_protected FROM user WHERE email = ?", ("admin@translearn.com",))
                    admin_user = cursor.fetchone()
                    
                    if admin_user:
                        # Update existing admin to super_admin if needed
                        if admin_user[2] != 'super_admin' or admin_user[3] != 1:
                            cursor.execute("UPDATE user SET role = 'super_admin', is_protected = 1 WHERE email = ?", ("admin@translearn.com",))
                            print("✓ Updated existing admin to super_admin with protected status")
                    else:
                        # Create the super admin user
                        password_hash = generate_password_hash("admin@123")
                        cursor.execute(
                            "INSERT INTO user (email, password_hash, role, is_active, is_protected) VALUES (?, ?, ?, ?, ?)",
                            ("admin@translearn.com", password_hash, "super_admin", 1, 1)
                        )
                        print("✓ Created super_admin user with email: admin@translearn.com")
        except Exception as e:
            print(f"Error ensuring super_admin user: {e}")
        
        # Add columns to student_profile table
        print("Adding columns to student_profile table...")
        columns_to_add = [
            ("phone", "VARCHAR(20)"),
            ("bio", "TEXT"),
            ("student_id", "VARCHAR(50)"),
            ("parent_email", "VARCHAR(120)"),
            ("parent_phone", "VARCHAR(20)")
        ]
        
        for col_name, col_type in columns_to_add:
            try:
                # Check if the table exists first
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='student_profile'")
                if not cursor.fetchone():
                    print("Creating student_profile table...")
                    cursor.execute("""
                        CREATE TABLE student_profile (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER,
                            FOREIGN KEY (user_id) REFERENCES user (id)
                        )
                    """)
                    print("✓ Created student_profile table")
            
                cursor.execute(f"ALTER TABLE student_profile ADD COLUMN {col_name} {col_type}")
                print(f"✓ Added {col_name} column")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e):
                    print(f"✓ {col_name} column already exists")
                else:
                    print(f"Error adding {col_name}: {e}")
        
        # Add columns to instructor_profile table
        print("Adding columns to instructor_profile table...")
        columns_to_add = [
            ("phone", "VARCHAR(20)"),
            ("department", "VARCHAR(100)"),
            ("office_location", "VARCHAR(100)"),
            ("office_hours", "VARCHAR(100)"),
            ("specialization", "VARCHAR(200)")
        ]
        
        for col_name, col_type in columns_to_add:
            try:
                # Check if the table exists first
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='instructor_profile'")
                if not cursor.fetchone():
                    print("Creating instructor_profile table...")
                    cursor.execute("""
                        CREATE TABLE instructor_profile (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER,
                            FOREIGN KEY (user_id) REFERENCES user (id)
                        )
                    """)
                    print("✓ Created instructor_profile table")
                
                cursor.execute(f"ALTER TABLE instructor_profile ADD COLUMN {col_name} {col_type}")
                print(f"✓ Added {col_name} column")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e):
                    print(f"✓ {col_name} column already exists")
                else:
                    print(f"Error adding {col_name}: {e}")
        
        # Add columns to course table
        print("Adding columns to course table...")
        columns_to_add = [
            ("code", "VARCHAR(20)"),
            ("category", "VARCHAR(50)"),
            ("level", "VARCHAR(20)"),
            ("max_students", "INTEGER DEFAULT 50"),
            ("start_date", "DATE"),
            ("end_date", "DATE"),
            ("meeting_days", "VARCHAR(100)"),
            ("meeting_time", "TIME"),
            ("syllabus", "TEXT"),
            ("prerequisites", "TEXT"),
            ("learning_outcomes", "TEXT"),
            ("is_active", "BOOLEAN DEFAULT 1"),
            ("allow_enrollment", "BOOLEAN DEFAULT 1"),
            ("enable_quizzes", "BOOLEAN DEFAULT 1"),
            ("enable_assignments", "BOOLEAN DEFAULT 1")
        ]
        
        for col_name, col_type in columns_to_add:
            try:
                # Check if the table exists first
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='course'")
                if not cursor.fetchone():
                    print("Creating course table...")
                    cursor.execute("""
                        CREATE TABLE course (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title VARCHAR(100),
                            description TEXT,
                            instructor_id INTEGER,
                            FOREIGN KEY (instructor_id) REFERENCES user (id)
                        )
                    """)
                    print("✓ Created course table")
                
                cursor.execute(f"ALTER TABLE course ADD COLUMN {col_name} {col_type}")
                print(f"✓ Added {col_name} column")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e):
                    print(f"✓ {col_name} column already exists")
                else:
                    print(f"Error adding {col_name}: {e}")
        
        # Add columns to assignment table
        print("Adding columns to assignment table...")
        try:
            cursor.execute("ALTER TABLE assignment ADD COLUMN is_active BOOLEAN DEFAULT 1")
            print("✓ Added is_active column to assignment")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("✓ is_active column already exists in assignment")
            else:
                print(f"Error adding is_active to assignment: {e}")
        
        # Add columns to quiz table
        print("Adding columns to quiz table...")
        try:
            cursor.execute("ALTER TABLE quiz ADD COLUMN is_active BOOLEAN DEFAULT 1")
            print("✓ Added is_active column to quiz")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("✓ is_active column already exists in quiz")
            else:
                print(f"Error adding is_active to quiz: {e}")
        
        # Create assignment_submission table if it doesn't exist
        print("Creating assignment_submission table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assignment_submission (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                assignment_id INTEGER,
                student_id INTEGER,
                submitted_at DATETIME,
                file_path VARCHAR(500),
                comments TEXT,
                grade FLOAT,
                feedback TEXT,
                FOREIGN KEY (assignment_id) REFERENCES assignment (id),
                FOREIGN KEY (student_id) REFERENCES user (id)
            )
        """)
        print("✓ Created assignment_submission table")
        
        # Create material table if it doesn't exist
        print("Creating material table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS material (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id INTEGER,
                title VARCHAR(100),
                description TEXT,
                file_path VARCHAR(500),
                file_type VARCHAR(50),
                uploaded_at DATETIME,
                FOREIGN KEY (course_id) REFERENCES course (id)
            )
        """)
        print("✓ Created material table")
        
        # Commit all changes
        conn.commit()
        print("All database changes committed successfully")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
        print("Changes rolled back due to error")
    finally:
        conn.close()
        print("Database connection closed")


def apply_migrations():
    """Apply Flask-Migrate migrations"""
    try:
        from flask_migrate import upgrade
        app = create_app()
        with app.app_context():
            upgrade()
            print("✓ Applied database migrations successfully")
    except Exception as e:
        print(f"Error applying migrations: {e}")


def ensure_super_admin():
    """Ensure super admin exists using SQLAlchemy ORM"""
    try:
        app = create_app()
        with app.app_context():
            # Check if super admin exists
            admin = User.query.filter_by(email="admin@translearn.com").first()
            
            if admin:
                # Update existing admin if needed
                if admin.role != 'super_admin' or not admin.is_protected:
                    admin.role = 'super_admin'
                    admin.is_protected = True
                    db.session.commit()
                    print("✓ Updated existing admin to super_admin with protected status")
                else:
                    print("✓ Super admin already exists with correct settings")
            else:
                # Create new super admin
                password_hash = generate_password_hash("admin@123")
                new_admin = User(
                    email="admin@translearn.com",
                    password_hash=password_hash,
                    role="super_admin",
                    is_active=True,
                    is_protected=True
                )
                db.session.add(new_admin)
                db.session.commit()
                print("✓ Created super_admin user with email: admin@translearn.com")
                
            # Also ensure any user with role 'super_admin' has is_protected set to True
            super_admins = User.query.filter_by(role='super_admin').all()
            for user in super_admins:
                if not user.is_protected:
                    user.is_protected = True
                    db.session.commit()
                    print(f"✓ Updated protection status for super_admin user: {user.email}")
    except Exception as e:
        print(f"Error ensuring super admin: {e}")


def main():
    """Main function to run all database fixes"""
    print("Starting database fixes...")
    
    # First apply migrations if available
    apply_migrations()
    
    # Then add any missing columns manually
    add_missing_columns()
    
    # Finally ensure super admin exists using ORM
    ensure_super_admin()
    
    print("Database fixes completed!")
    print("You can now login with:")
    print("  Email: admin@translearn.com")
    print("  Password: admin@123")
    print("  URL: http://localhost:5000/admin/login")


if __name__ == "__main__":
    main()