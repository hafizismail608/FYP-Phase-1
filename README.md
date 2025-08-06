# TransLearn LMS

A comprehensive, modern learning management system built with Flask, featuring AI-powered behavior monitoring, adaptive quizzes, and intelligent student support.

## 🚀 Features

### Core TransLearn Features
- **Multi-role Support**: Students, Instructors, Admin, and Super Admin roles
- **Course Management**: Create, manage, and enroll in courses
- **Assignment System**: Submit and grade assignments
- **Quiz System**: Adaptive quizzes with difficulty levels
- **Discussion Forums**: Interactive course discussions
- **Calendar Integration**: Track deadlines and events
- **File Management**: Upload and share course materials

### AI-Powered Features
- **Real-time Behavior Monitoring**: Track focus and frustration levels
- **Emotion Analysis**: AI-powered emotion detection using computer vision
- **Adaptive Learning**: Dynamic quiz difficulty based on performance
- **Intelligent Suggestions**: AI-generated study recommendations
- **Performance Analytics**: Detailed student progress tracking
- **Gemini AI Integration**: Smart content generation and assistance

### Advanced Features
- **Live Dashboard**: Real-time statistics and progress tracking
- **Responsive Design**: Modern, mobile-friendly interface
- **Real-time Updates**: Live data synchronization via WebSockets
- **Admin Panel**: Comprehensive system management
- **User Management**: Advanced user role and permission system
- **Enhanced Security**: Protected admin accounts, secure password storage

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Database**: SQLAlchemy with SQLite
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **AI/ML**: DeepFace for emotion analysis, Google Gemini AI
- **Real-time**: Socket.IO for live updates
- **Authentication**: Flask-Login with role-based access
- **Security**: CSRF protection, secure cookies, password hashing

## 📋 Prerequisites

- Python 3.8 or higher
- Git
- Web browser with camera access (for behavior monitoring)
- Google Gemini API key (for AI features)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/translearn-lms.git
   cd translearn-lms
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```
   SECRET_KEY=your-secure-secret-key-here
   DATABASE_URL=sqlite:///site.db
   GEMINI_API_KEY=your-gemini-api-key-here
   ```

6. **Initialize and fix database**
   ```bash
   # Apply migrations and create super admin user
   python fix_database.py
   ```

7. **Run the application**
   ```bash
   python app.py
   ```

8. **Access the application**
   Open your browser and go to `http://localhost:5000`

9. **Login as Super Admin**
   ```
   Email: admin@translearn.com
   Password: admin@123
   URL: http://localhost:5000/admin/login
   ```
   *Note: Change the default password after first login*

## 👥 User Roles

### Super Admin
- Manage all system aspects
- Create and manage admin accounts
- Cannot be deleted or deactivated

### Admin
- Manage users and courses
- Create instructor and student accounts
- Monitor system performance

### Instructor
- Create and manage courses
- Add course materials and modules
- Create assignments and quizzes
- Grade student submissions
- View student behavior analytics
- Track student progress

### Student
- Enroll in courses
- Access course materials
- Submit assignments
- Take adaptive quizzes
- Participate in discussions
- View personal progress analytics
- Receive AI-powered study suggestions

## 🔒 Security Features

- **Protected Admin Accounts**: Super admin accounts cannot be deleted or deactivated
- **Role-Based Access Control**: Strict permission system based on user roles
- **Secure Password Storage**: Password hashing with Werkzeug security
- **CSRF Protection**: Cross-Site Request Forgery prevention
- **Secure Cookies**: HTTP-only and secure cookie settings
- **Input Validation**: Form validation with WTForms
- **Session Management**: Secure session handling

## 📊 AI Monitoring Features

- **Focus Detection**: Real-time head pose estimation using OpenCV
- **Emotion Analysis**: Facial emotion detection with DeepFace
- **Activity Tracking**: Keyboard and mouse activity monitoring
- **Frustration Detection**: AI-powered frustration level analysis
- **Engagement Scoring**: Combined metrics for student engagement

## 🧠 Adaptive Learning

- **Dynamic Quiz Difficulty**: Adjusts based on student performance
- **Personalized Recommendations**: AI-generated study suggestions
- **Learning Style Adaptation**: Content tailored to individual learning styles
- **Progress Tracking**: Detailed analytics on student progress

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact

For any questions or support, please contact the development team at support@translearn.com.
- Track progress and performance

### Instructor
- Create and manage courses
- Design assignments and quizzes
- Grade submissions
- Monitor student behavior
- View detailed analytics
- Manage course content

### Admin
- Manage all users and courses
- System-wide analytics
- User role management
- Course oversight
- System configuration

## 🎯 Key Features in Detail

### AI Behavior Monitoring
- Real-time focus and frustration tracking
- Computer vision-based emotion analysis
- Live dashboard updates every 5 seconds
- Historical behavior data visualization

### Adaptive Quiz System
- Dynamic difficulty adjustment
- Performance-based question selection
- Real-time behavior integration
- Comprehensive result analytics

### Modern Dashboard
- Real-time statistics
- Upcoming events calendar
- AI-powered suggestions
- Motivational quotes
- Live progress tracking

## 📁 Project Structure

```
ai-lms2/
├── app.py                 # Main application file
├── config.py             # Configuration settings
├── models.py             # Database models
├── requirements.txt      # Python dependencies
├── student/              # Student blueprint
│   ├── views.py         # Student routes
│   └── behavior_monitor.py
├── instructor/           # Instructor blueprint
│   └── views.py         # Instructor routes
├── admin/               # Admin blueprint
│   └── views.py         # Admin routes
├── auth/                # Authentication blueprint
│   └── views.py         # Auth routes
├── services/            # External services
│   └── gemini_service.py
├── templates/           # HTML templates
│   ├── base.html
│   ├── student_dashboard.html
│   ├── instructor_dashboard.html
│   └── admin/
├── static/              # Static files (CSS, JS, images)
└── uploads/             # File uploads directory
```

## 🔧 Configuration

### Environment Variables
- `SECRET_KEY`: Flask secret key for session management
- `GEMINI_API_KEY`: Google Gemini API key for AI features
- `DATABASE_URL`: Database connection string (optional)

### Database Configuration
The application uses SQLite by default. For production, consider using PostgreSQL or MySQL.

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. Set up a production web server (Gunicorn, uWSGI)
2. Configure environment variables
3. Set up a production database
4. Configure SSL certificates
5. Set up monitoring and logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Flask framework and community
- Bootstrap for responsive design
- DeepFace for emotion analysis
- Google Gemini for AI features

## 📞 Support

For support and questions, please open an issue in the GitHub repository or contact the development team.

---

**Built with ❤️ for modern education**#   F Y P - P h a s e - 1  
 