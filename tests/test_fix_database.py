import pytest
import os
import sqlite3
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fix_database import (
    add_missing_columns,
    ensure_super_admin,
    create_table_if_not_exists
)
from models import User, db
from app import create_app
from config import TestConfig

@pytest.fixture
def test_db_path(tmp_path):
    """Create a temporary database file path."""
    db_file = tmp_path / "test.db"
    return str(db_file)

@pytest.fixture
def test_db_connection(test_db_path):
    """Create a test database connection."""
    # Create a new database file
    conn = sqlite3.connect(test_db_path)
    
    # Create a basic user table for testing
    conn.execute('''
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        role TEXT NOT NULL
    )
    ''')
    
    yield conn
    
    # Close the connection after the test
    conn.close()
    
    # Clean up the file
    if os.path.exists(test_db_path):
        os.remove(test_db_path)

def test_add_missing_columns(test_db_connection, test_db_path):
    """Test adding missing columns to the user table."""
    # Initial check - these columns should not exist yet
    cursor = test_db_connection.cursor()
    cursor.execute("PRAGMA table_info(user)")
    columns = [column[1] for column in cursor.fetchall()]
    
    assert 'last_login' not in columns
    assert 'login_count' not in columns
    assert 'is_protected' not in columns
    
    # Run the function to add missing columns
    add_missing_columns(test_db_path)
    
    # Check that columns were added
    cursor.execute("PRAGMA table_info(user)")
    columns = [column[1] for column in cursor.fetchall()]
    
    assert 'last_login' in columns
    assert 'login_count' in columns
    assert 'is_protected' in columns

def test_create_table_if_not_exists(test_db_connection, test_db_path):
    """Test creating a table if it doesn't exist."""
    # Check that the test table doesn't exist yet
    cursor = test_db_connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test_table'")
    assert cursor.fetchone() is None
    
    # Create the table
    create_table_if_not_exists(
        test_db_path,
        'test_table',
        '''
        CREATE TABLE test_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            value TEXT
        )
        '''
    )
    
    # Check that the table was created
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test_table'")
    assert cursor.fetchone() is not None
    
    # Check that calling the function again doesn't cause an error
    create_table_if_not_exists(
        test_db_path,
        'test_table',
        '''
        CREATE TABLE test_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            value TEXT
        )
        '''
    )

def test_ensure_super_admin(app):
    """Test ensuring a super admin exists."""
    with app.app_context():
        # Make sure there's no super_admin user yet
        super_admin = User.query.filter_by(role='super_admin').first()
        if super_admin:
            db.session.delete(super_admin)
            db.session.commit()
        
        # Run the function to ensure super admin
        ensure_super_admin()
        
        # Check that a super admin was created
        super_admin = User.query.filter_by(role='super_admin').first()
        assert super_admin is not None
        assert super_admin.email == 'admin@translearn.com'
        assert super_admin.is_protected is True
        
        # Test that running the function again doesn't create a duplicate
        ensure_super_admin()
        super_admin_count = User.query.filter_by(role='super_admin').count()
        assert super_admin_count == 1