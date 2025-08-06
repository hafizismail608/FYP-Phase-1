import threading
import time
import random
from datetime import datetime
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from models import Enrollment, EmotionLog, db

# Placeholders for actual imports - in a real implementation, these would be used
# import cv2
# import deepface or fer
# import librosa
# import pynput
# import mouseinfo

db = SQLAlchemy()

class StudentBehaviorMonitor:
    def __init__(self):
        self.running = False
        self.duration = 300  # 5 minutes default duration
        self.logs = []
        self.current_app = None

    def start_monitoring(self, student_id, course_id, app):
        self.running = True
        self.current_app = app
        
        # Store the monitor instance in the app context for access from other routes
        app.behavior_monitor = self
        
        # Start monitoring in a separate thread
        monitor_thread = threading.Thread(target=self._monitoring_loop, args=(student_id, course_id, app))
        monitor_thread.daemon = True  # Thread will exit when main thread exits
        monitor_thread.start()
        
        return True
    
    def _monitoring_loop(self, student_id, course_id, app):
        """The main monitoring loop that runs in a separate thread"""
        with app.app_context():
            try:
                # Initialize monitoring components
                self.initialize_components()
                
                start_time = time.time()
                while self.running and (time.time() - start_time) < self.duration:
                    # Collect data from all sources
                    face_data = self.analyze_face()
                    voice_data = self.analyze_voice()
                    keyboard_data = self.analyze_keyboard()
                    mouse_data = self.analyze_mouse()
                    
                    # Aggregate scores
                    focus_score = self.aggregate_focus_score(face_data, voice_data, keyboard_data, mouse_data)
                    frustration_score = self.aggregate_frustration_score(face_data, voice_data, keyboard_data, mouse_data)
                    
                    # Log the data
                    log_entry = {
                        'timestamp': datetime.utcnow().isoformat(),
                        'focus_score': focus_score,
                        'frustration_score': frustration_score,
                        'source_data_summary': {
                            'face': face_data,
                            'voice': voice_data,
                            'keyboard': keyboard_data,
                            'mouse': mouse_data
                        }
                    }
                    self.logs.append(log_entry)
                    
                    # Log to EmotionLog table
                    elog = EmotionLog(
                        student_id=student_id,
                        course_id=course_id,  # Can be None
                        timestamp=datetime.utcnow(),
                        focus_score=focus_score,
                        frustration_score=frustration_score,
                        source_data_summary=str(log_entry['source_data_summary'])
                    )
                    db.session.add(elog)
                    db.session.commit()
                    
                    # Also update the enrollment record if course_id is provided
                    if course_id:
                        enrollment = Enrollment.query.filter_by(
                            student_id=student_id, 
                            course_id=course_id
                        ).first()
                        
                        if enrollment:
                            enrollment.latest_focus_score = focus_score
                            enrollment.frustration_level = frustration_score
                            enrollment.last_updated = datetime.utcnow()
                            enrollment.is_monitoring = True
                            db.session.commit()
                    
                    time.sleep(2)  # Wait 2 seconds between measurements
                    
            except Exception as e:
                print(f"Error in monitoring: {str(e)}")
            finally:
                self.cleanup()
                self.running = False
                if hasattr(app, 'behavior_monitor'):
                    delattr(app, 'behavior_monitor')

    def stop_monitoring(self):
        self.running = False

    def initialize_components(self):
        # Initialize camera, microphone, and other components
        # In a real implementation, this would initialize hardware components
        # For simulation, we'll just seed the random number generator
        random.seed()  # Use system time as seed

    def cleanup(self):
        # Clean up resources (camera, microphone, etc.)
        pass

    def analyze_face(self):
        # Simulate face analysis since actual implementation would require camera access
        # In a real implementation, this would use OpenCV and DeepFace
        import random
        
        # Generate simulated emotion data
        emotions = {
            'happy': random.uniform(0.3, 0.8),
            'sad': random.uniform(0.0, 0.3),
            'angry': random.uniform(0.0, 0.2),
            'surprised': random.uniform(0.0, 0.2),
            'disgusted': random.uniform(0.0, 0.1),
            'neutral': random.uniform(0.2, 0.6)
        }
        
        # Normalize emotions to sum to 1.0
        total = sum(emotions.values())
        emotions = {k: v/total for k, v in emotions.items()}
        
        # Generate attention score (higher when happy/neutral, lower when negative emotions)
        attention = 0.7 * emotions['happy'] + 0.5 * emotions['neutral'] - \
                   0.3 * emotions['sad'] - 0.4 * emotions['angry'] - 0.2 * emotions['disgusted']
        attention = max(0.1, min(0.9, attention + random.uniform(-0.1, 0.1)))
        
        return {'emotions': emotions, 'attention': attention}

    def analyze_voice(self):
        # Simulate voice analysis since actual implementation would require microphone access
        # In a real implementation, this would use librosa or similar audio processing library
        import random
        
        # Generate simulated voice data
        # Tone: 0.0 (calm) to 1.0 (agitated)
        tone = random.uniform(0.1, 0.7)
        
        # Volume: 0.0 (silent) to 1.0 (loud)
        volume = random.uniform(0.3, 0.8)
        
        return {'tone': tone, 'volume': volume}

    def analyze_keyboard(self):
        # Simulate keyboard activity since actual implementation would require keyboard hooks
        # In a real implementation, this would use pynput or similar library
        import random
        
        # Generate simulated keyboard data
        # Activity: 0.0 (none) to 1.0 (constant typing)
        activity = random.uniform(0.2, 0.9)
        
        # Typing speed: 0.0 (slow) to 1.0 (fast)
        typing_speed = random.uniform(0.3, 0.8)
        
        return {'activity': activity, 'typing_speed': typing_speed}

    def analyze_mouse(self):
        # Simulate mouse activity since actual implementation would require mouse hooks
        # In a real implementation, this would use pynput or mouseinfo
        import random
        
        # Generate simulated mouse data
        # Movement: 0.0 (none) to 1.0 (constant movement)
        movement = random.uniform(0.2, 0.9)
        
        # Clicks: number of clicks in the sampling period
        clicks = random.randint(0, 5)
        
        return {'movement': movement, 'clicks': clicks}

    def aggregate_focus_score(self, face_data, voice_data, keyboard_data, mouse_data):
        # Calculate focus score based on multiple inputs
        # Face attention is the primary indicator (50% weight)
        face_focus = face_data.get('attention', 0.0) * 0.5
        
        # Keyboard and mouse activity indicate engagement (40% weight)
        activity_focus = (keyboard_data.get('activity', 0.0) * 0.2 + 
                          mouse_data.get('movement', 0.0) * 0.1 + 
                          mouse_data.get('clicks', 0) / 10 * 0.1)
        
        # Voice volume can indicate engagement (10% weight)
        voice_focus = voice_data.get('volume', 0.0) * 0.1
        
        # Combine all factors
        focus_score = face_focus + activity_focus + voice_focus
        
        # Ensure the score is between 0 and 1
        return max(0.0, min(1.0, focus_score))

    def aggregate_frustration_score(self, face_data, voice_data, keyboard_data, mouse_data):
        # Calculate frustration score based on multiple inputs
        # Face emotions are primary indicators (60% weight)
        emotions = face_data.get('emotions', {})
        face_frustration = (emotions.get('angry', 0.0) * 0.3 + 
                           emotions.get('sad', 0.0) * 0.2 + 
                           emotions.get('disgusted', 0.0) * 0.1)
        
        # Voice tone can indicate frustration (20% weight)
        voice_frustration = voice_data.get('tone', 0.0) * 0.2
        
        # Erratic keyboard/mouse behavior can indicate frustration (20% weight)
        activity_frustration = (keyboard_data.get('typing_speed', 0.0) * 0.1 + 
                               mouse_data.get('movement', 0.0) * 0.1)
        
        # Combine all factors
        frustration_score = face_frustration + voice_frustration + activity_frustration
        
        # Ensure the score is between 0 and 1
        return max(0.0, min(1.0, frustration_score))

    def get_latest_scores(self):
        if self.logs:
            return self.logs[-1]
        return None

    def get_all_logs(self):
        return self.logs