#!/usr/bin/env python3
"""
Migration script to add dubbed_video_path column to lectures table
"""

import sqlite3
import os
from datetime import datetime

def add_dubbed_video_path_column():
    """
    Add dubbed_video_path column to the lectures table
    """
    # Get the database path
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'lms.db')
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return False
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if the column already exists
        cursor.execute("PRAGMA table_info(lecture)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'dubbed_video_path' in columns:
            print("Column 'dubbed_video_path' already exists in lectures table")
            return True
        
        # Add the new column
        cursor.execute("""
            ALTER TABLE lecture 
            ADD COLUMN dubbed_video_path VARCHAR(500)
        """)
        
        # Commit the changes
        conn.commit()
        print("Successfully added 'dubbed_video_path' column to lectures table")
        
        return True
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    print(f"Starting migration at {datetime.now()}")
    success = add_dubbed_video_path_column()
    if success:
        print("Migration completed successfully")
    else:
        print("Migration failed")