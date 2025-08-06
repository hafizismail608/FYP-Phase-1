import pytest
from app import create_app, db as _db
from models import User
from config import TestConfig

@pytest.fixture(scope='session')
def app():
    """Create and configure a Flask app for testing."""
    app = create_app(TestConfig)
    
    # Create a test database and tables
    with app.app_context():
        _db.create_all()
        
    yield app
    
    # Clean up after the test
    with app.app_context():
        _db.session.remove()
        _db.drop_all()

@pytest.fixture(scope='session')
def db(app):
    """Session-wide test database."""
    with app.app_context():
        yield _db

@pytest.fixture(scope='function')
def session(db):
    """Creates a new database session for each test function."""
    connection = db.engine.connect()
    transaction = connection.begin()
    
    session = db.create_scoped_session()
    db.session = session
    
    yield session
    
    transaction.rollback()
    connection.close()
    session.remove()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()

@pytest.fixture
def test_user(session):
    """Create a test user."""
    user = User(
        email='test@example.com',
        password='password123',
        first_name='Test',
        last_name='User',
        role='student'
    )
    session.add(user)
    session.commit()
    
    return user

@pytest.fixture
def test_admin(session):
    """Create a test admin user."""
    admin = User(
        email='admin@example.com',
        password='admin123',
        first_name='Admin',
        last_name='User',
        role='admin'
    )
    session.add(admin)
    session.commit()
    
    return admin