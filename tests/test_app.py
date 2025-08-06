import pytest
from flask import url_for
from flask_login import current_user

# Basic route tests
def test_home_page(client):
    """Test that the home page loads successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'TransLearn LMS' in response.data

def test_login_page(client):
    """Test that the login page loads successfully."""
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_register_page(client):
    """Test that the registration page loads successfully."""
    response = client.get('/auth/register')
    assert response.status_code == 200
    assert b'Register' in response.data

# Authentication tests
def test_login_success(client, test_user):
    """Test successful user login."""
    response = client.post(
        '/auth/login',
        data={
            'email': 'test@example.com',
            'password': 'password123',
            'remember': False
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'Welcome' in response.data

def test_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    response = client.post(
        '/auth/login',
        data={
            'email': 'wrong@example.com',
            'password': 'wrongpassword',
            'remember': False
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'Invalid email or password' in response.data

def test_logout(client, test_user):
    """Test user logout functionality."""
    # First login
    client.post(
        '/auth/login',
        data={
            'email': 'test@example.com',
            'password': 'password123',
            'remember': False
        }
    )
    
    # Then logout
    response = client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'You have been logged out' in response.data

# Admin access tests
def test_admin_access(client, test_admin):
    """Test admin access to admin dashboard."""
    # Login as admin
    client.post(
        '/auth/login',
        data={
            'email': 'admin@example.com',
            'password': 'admin123',
            'remember': False
        }
    )
    
    # Access admin dashboard
    response = client.get('/admin/dashboard', follow_redirects=True)
    assert response.status_code == 200
    assert b'Admin Dashboard' in response.data

def test_non_admin_access_denied(client, test_user):
    """Test that non-admin users cannot access admin dashboard."""
    # Login as regular user
    client.post(
        '/auth/login',
        data={
            'email': 'test@example.com',
            'password': 'password123',
            'remember': False
        }
    )
    
    # Try to access admin dashboard
    response = client.get('/admin/dashboard', follow_redirects=True)
    assert response.status_code == 403  # Forbidden
    assert b'Access Denied' in response.data