#!/usr/bin/env python3
"""
Migration script to add dubbed_video_path column to the lecture table
"""
import sqlite3
import os

def main():
    # Database path
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'site.db')
    
    if not os.path.exists(db_path):
        print(f"Database file not found at {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if the column already exists
        cursor.execute("PRAGMA table_info(lecture)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'dubbed_video_path' in columns:
            print("✓ dubbed_video_path column already exists")
        else:
            # Add the dubbed_video_path column
            cursor.execute("ALTER TABLE lecture ADD COLUMN dubbed_video_path VARCHAR(500)")
            conn.commit()
            print("✓ Added dubbed_video_path column to lecture table")
            
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()
        print("Database connection closed")

if __name__ == '__main__':
    main()