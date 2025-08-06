from app import create_app
from models import EmotionLog, db

app = create_app()

with app.app_context():
    count = EmotionLog.query.count()
    print(f'Emotion logs count: {count}')
    
    if count > 0:
        logs = EmotionLog.query.all()
        print(f'First log: {logs[0].timestamp}, Focus: {logs[0].focus_score}, Frustration: {logs[0].frustration_score}')
    else:
        print('No emotion logs found in the database.')