import pytest
from forms import LoginForm, StudentRegistrationForm, InstructorRegistrationForm
from wtforms.validators import ValidationError

# Login form tests
def test_login_form_valid():
    """Test login form with valid data."""
    form = LoginForm()
    form.email.data = 'test@example.com'
    form.password.data = 'password123'
    form.remember.data = True
    
    assert form.validate() is True

def test_login_form_invalid_email():
    """Test login form with invalid email."""
    form = LoginForm()
    form.email.data = 'not-an-email'
    form.password.data = 'password123'
    
    assert form.validate() is False
    assert 'Invalid email address.' in form.email.errors

def test_login_form_missing_password():
    """Test login form with missing password."""
    form = LoginForm()
    form.email.data = 'test@example.com'
    form.password.data = ''
    
    assert form.validate() is False
    assert 'This field is required.' in form.password.errors

# Student registration form tests
def test_student_registration_form_valid():
    """Test student registration form with valid data."""
    form = StudentRegistrationForm()
    form.email.data = 'student@example.com'
    form.password.data = 'Password123!'
    form.confirm_password.data = 'Password123!'
    form.first_name.data = 'Test'
    form.last_name.data = 'Student'
    form.accept_terms.data = True
    
    assert form.validate() is True

def test_student_registration_form_password_mismatch():
    """Test student registration form with mismatched passwords."""
    form = StudentRegistrationForm()
    form.email.data = 'student@example.com'
    form.password.data = 'Password123!'
    form.confirm_password.data = 'DifferentPassword123!'
    form.first_name.data = 'Test'
    form.last_name.data = 'Student'
    form.accept_terms.data = True
    
    assert form.validate() is False
    assert 'Passwords must match.' in form.confirm_password.errors

def test_student_registration_form_weak_password():
    """Test student registration form with weak password."""
    form = StudentRegistrationForm()
    form.email.data = 'student@example.com'
    form.password.data = 'weak'
    form.confirm_password.data = 'weak'
    form.first_name.data = 'Test'
    form.last_name.data = 'Student'
    form.accept_terms.data = True
    
    assert form.validate() is False
    # Check for password strength error message
    assert any('at least 8 characters' in error for error in form.password.errors)

def test_student_registration_form_terms_not_accepted():
    """Test student registration form without accepting terms."""
    form = StudentRegistrationForm()
    form.email.data = 'student@example.com'
    form.password.data = 'Password123!'
    form.confirm_password.data = 'Password123!'
    form.first_name.data = 'Test'
    form.last_name.data = 'Student'
    form.accept_terms.data = False
    
    assert form.validate() is False
    assert 'You must accept the terms and conditions to register.' in form.accept_terms.errors

# Instructor registration form tests
def test_instructor_registration_form_valid():
    """Test instructor registration form with valid data."""
    form = InstructorRegistrationForm()
    form.email.data = 'instructor@example.com'
    form.password.data = 'Password123!'
    form.confirm_password.data = 'Password123!'
    form.first_name.data = 'Test'
    form.last_name.data = 'Instructor'
    form.specialization.data = 'Computer Science'
    form.accept_terms.data = True
    
    assert form.validate() is True

def test_instructor_registration_form_missing_specialization():
    """Test instructor registration form with missing specialization."""
    form = InstructorRegistrationForm()
    form.email.data = 'instructor@example.com'
    form.password.data = 'Password123!'
    form.confirm_password.data = 'Password123!'
    form.first_name.data = 'Test'
    form.last_name.data = 'Instructor'
    form.specialization.data = ''
    form.accept_terms.data = True
    
    assert form.validate() is False
    assert 'This field is required.' in form.specialization.errors

# Test email normalization
def test_email_normalization():
    """Test that emails are normalized to lowercase."""
    form = LoginForm()
    form.email.data = 'TEST@ExAmPlE.CoM'
    form.password.data = 'password123'
    
    # Call the validation method directly
    form.validate_email(form.email)
    
    # Check that the email was converted to lowercase
    assert form.email.data == 'test@example.com'