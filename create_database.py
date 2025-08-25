#!/usr/bin/env python3
"""
Script to create the database and all tables
"""
from app import create_app
from models import db

def main():
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✓ Database and all tables created successfully")
        
        # Check if site.db file exists
        import os
        db_path = os.path.join(os.path.dirname(__file__), 'site.db')
        if os.path.exists(db_path):
            print(f"✓ Database file created at: {db_path}")
        else:
            print("Database file not found in expected location")

if __name__ == '__main__':
    main()