from app import create_app
from models import EmotionLog, User, db
from datetime import datetime, timedelta
import random
import json

app = create_app()

def generate_sample_logs(user_id, num_logs=10):
    """Generate sample emotion logs for a user"""
    with app.app_context():
        # Check if user exists
        user = User.query.get(user_id)
        if not user:
            print(f"User with ID {user_id} not found.")
            return False
        
        # Generate logs with timestamps going back from now
        now = datetime.utcnow()
        
        for i in range(num_logs):
            # Create timestamp going back in time
            timestamp = now - timedelta(minutes=i*5)  # 5 minute intervals
            
            # Generate random focus and frustration scores
            focus_score = round(random.uniform(0.3, 0.9), 2)
            frustration_score = round(random.uniform(0.2, 0.8), 2)
            
            # Generate sample source data
            source_data = {
                'face': {
                    'emotions': {
                        'happy': round(random.uniform(0.1, 0.5), 2),
                        'sad': round(random.uniform(0.0, 0.3), 2),
                        'angry': round(random.uniform(0.0, 0.2), 2),
                        'surprised': round(random.uniform(0.0, 0.2), 2),
                        'disgusted': round(random.uniform(0.0, 0.1), 2),
                        'neutral': round(random.uniform(0.2, 0.6), 2)
                    },
                    'attention': round(random.uniform(0.3, 0.9), 2)
                },
                'voice': {
                    'volume': round(random.uniform(0.3, 0.8), 2),
                    'tone': round(random.uniform(0.2, 0.7), 2)
                },
                'keyboard': {
                    'typing_speed': round(random.uniform(0.4, 0.9), 2),
                    'error_rate': round(random.uniform(0.1, 0.5), 2)
                },
                'mouse': {
                    'movement': round(random.uniform(0.3, 0.8), 2),
                    'clicks': round(random.uniform(0.2, 0.7), 2)
                }
            }
            
            # Create and save the log
            log = EmotionLog(
                student_id=user_id,
                timestamp=timestamp,
                focus_score=focus_score,
                frustration_score=frustration_score,
                source_data_summary=str(source_data)
            )
            
            db.session.add(log)
        
        # Commit all logs at once
        db.session.commit()
        print(f"Generated {num_logs} sample emotion logs for user {user_id}")
        return True

if __name__ == "__main__":
    # Get user ID from input
    try:
        user_id = int(input("Enter user ID to generate logs for: "))
        num_logs = int(input("Enter number of logs to generate (default 10): ") or "10")
        
        success = generate_sample_logs(user_id, num_logs)
        
        if success:
            print("Sample logs generated successfully!")
        else:
            print("Failed to generate sample logs.")
    except ValueError:
        print("Please enter valid numeric values.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")