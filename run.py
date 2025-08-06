import os
from dotenv import load_dotenv
from app import create_app
from fix_database import main as fix_database

# Load environment variables from .env file
load_dotenv()

# Create app instance
app = create_app()

def main():
    """Entry point for the application"""
    # Fix database schema and ensure super admin exists
    fix_database()
    
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.environ.get('FLASK_ENV') == 'development'
    )

if __name__ == '__main__':
    main()