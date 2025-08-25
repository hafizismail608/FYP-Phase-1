import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, Lecture, LectureLike, LectureShare

def upgrade():
    """Add lecture-related tables to the database"""
    # Create the upload directories if they don't exist
    video_upload_dir = os.path.join('static', 'uploads', 'videos')
    thumbnail_upload_dir = os.path.join('static', 'uploads', 'thumbnails')
    subtitle_upload_dir = os.path.join('static', 'uploads', 'subtitles')
    
    for directory in [video_upload_dir, thumbnail_upload_dir, subtitle_upload_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    # Create a Flask app and push an application context
    app = create_app()
    
    with app.app_context():
        # Create the tables
        db.create_all()
        print("Lecture tables created successfully.")

def downgrade():
    """Remove lecture-related tables from the database"""
    # Create a Flask app and push an application context
    app = create_app()
    
    with app.app_context():
        # This is a destructive operation and should be used with caution
        Lecture.__table__.drop(db.engine)
        LectureLike.__table__.drop(db.engine)
        LectureShare.__table__.drop(db.engine)
        print("Lecture tables removed.")

if __name__ == "__main__":
    # When run directly, perform the upgrade
    upgrade()