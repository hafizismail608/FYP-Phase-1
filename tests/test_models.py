import pytest
from models import User, Course, Enrollment, StudentProfile, InstructorProfile
from werkzeug.security import check_password_hash

# User model tests
def test_user_creation(session):
    """Test creating a new user."""
    user = User(
        email='newuser@example.com',
        password='securepassword',
        first_name='New',
        last_name='User',
        role='student'
    )
    session.add(user)
    session.commit()
    
    retrieved_user = session.query(User).filter_by(email='newuser@example.com').first()
    assert retrieved_user is not None
    assert retrieved_user.email == 'newuser@example.com'
    assert retrieved_user.first_name == 'New'
    assert retrieved_user.last_name == 'User'
    assert retrieved_user.role == 'student'
    assert check_password_hash(retrieved_user.password, 'securepassword')

def test_user_password_hashing(session):
    """Test that passwords are properly hashed."""
    user = User(
        email='passwordtest@example.com',
        password='testpassword',
        first_name='Password',
        last_name='Test',
        role='student'
    )
    session.add(user)
    session.commit()
    
    retrieved_user = session.query(User).filter_by(email='passwordtest@example.com').first()
    assert retrieved_user.password != 'testpassword'  # Password should be hashed
    assert check_password_hash(retrieved_user.password, 'testpassword')  # Hash should verify
    assert not check_password_hash(retrieved_user.password, 'wrongpassword')  # Wrong password should fail

# Course model tests
def test_course_creation(session):
    """Test creating a new course."""
    # Create an instructor first
    instructor = User(
        email='instructor@example.com',
        password='instructor123',
        first_name='Test',
        last_name='Instructor',
        role='instructor'
    )
    session.add(instructor)
    session.commit()
    
    # Create a course
    course = Course(
        title='Test Course',
        description='A test course for unit testing',
        instructor_id=instructor.id
    )
    session.add(course)
    session.commit()
    
    retrieved_course = session.query(Course).filter_by(title='Test Course').first()
    assert retrieved_course is not None
    assert retrieved_course.title == 'Test Course'
    assert retrieved_course.description == 'A test course for unit testing'
    assert retrieved_course.instructor_id == instructor.id

# Enrollment model tests
def test_enrollment(session):
    """Test enrolling a student in a course."""
    # Create a student
    student = User(
        email='student@example.com',
        password='student123',
        first_name='Test',
        last_name='Student',
        role='student'
    )
    session.add(student)
    
    # Create an instructor
    instructor = User(
        email='instructor2@example.com',
        password='instructor123',
        first_name='Test',
        last_name='Instructor',
        role='instructor'
    )
    session.add(instructor)
    session.commit()
    
    # Create a course
    course = Course(
        title='Enrollment Test Course',
        description='A course for testing enrollment',
        instructor_id=instructor.id
    )
    session.add(course)
    session.commit()
    
    # Enroll the student in the course
    enrollment = Enrollment(
        student_id=student.id,
        course_id=course.id
    )
    session.add(enrollment)
    session.commit()
    
    # Verify enrollment
    retrieved_enrollment = session.query(Enrollment).filter_by(
        student_id=student.id,
        course_id=course.id
    ).first()
    
    assert retrieved_enrollment is not None
    assert retrieved_enrollment.student_id == student.id
    assert retrieved_enrollment.course_id == course.id

# Profile model tests
def test_student_profile(session):
    """Test creating a student profile."""
    # Create a student
    student = User(
        email='profilestudent@example.com',
        password='student123',
        first_name='Profile',
        last_name='Student',
        role='student'
    )
    session.add(student)
    session.commit()
    
    # Create a student profile
    profile = StudentProfile(
        user_id=student.id,
        bio='Test student bio',
        phone='123-456-7890',
        student_id='S12345',
        parent_email='parent@example.com',
        parent_phone='987-654-3210'
    )
    session.add(profile)
    session.commit()
    
    # Verify profile
    retrieved_profile = session.query(StudentProfile).filter_by(user_id=student.id).first()
    assert retrieved_profile is not None
    assert retrieved_profile.bio == 'Test student bio'
    assert retrieved_profile.phone == '123-456-7890'
    assert retrieved_profile.student_id == 'S12345'
    assert retrieved_profile.parent_email == 'parent@example.com'
    assert retrieved_profile.parent_phone == '987-654-3210'

def test_instructor_profile(session):
    """Test creating an instructor profile."""
    # Create an instructor
    instructor = User(
        email='profileinstructor@example.com',
        password='instructor123',
        first_name='Profile',
        last_name='Instructor',
        role='instructor'
    )
    session.add(instructor)
    session.commit()
    
    # Create an instructor profile
    profile = InstructorProfile(
        user_id=instructor.id,
        bio='Test instructor bio',
        phone='123-456-7890',
        specialization='Computer Science',
        education='PhD in Computer Science'
    )
    session.add(profile)
    session.commit()
    
    # Verify profile
    retrieved_profile = session.query(InstructorProfile).filter_by(user_id=instructor.id).first()
    assert retrieved_profile is not None
    assert retrieved_profile.bio == 'Test instructor bio'
    assert retrieved_profile.phone == '123-456-7890'
    assert retrieved_profile.specialization == 'Computer Science'
    assert retrieved_profile.education == 'PhD in Computer Science'