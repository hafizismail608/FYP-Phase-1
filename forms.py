from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Regexp
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Please enter a valid email address')])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('student', 'Student'), ('instructor', 'Instructor')], validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
    def validate_email(self, email):
        # Convert to lowercase for case-insensitive comparison
        self.email.data = email.data.lower().strip()

class StudentRegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Please enter a valid email address')])
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=8, message='Password must be at least 8 characters long'),
        Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]', 
               message='Password must include at least one uppercase letter, one lowercase letter, one number, and one special character')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    agree_terms = BooleanField('I agree to the Terms and Conditions', validators=[DataRequired(message='You must agree to the terms and conditions')])
    submit = SubmitField('Register as Student')
    
    def validate_email(self, email):
        # Convert to lowercase for case-insensitive comparison
        self.email.data = email.data.lower().strip()

class InstructorRegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Please enter a valid email address')])
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=8, message='Password must be at least 8 characters long'),
        Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]', 
               message='Password must include at least one uppercase letter, one lowercase letter, one number, and one special character')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    agree_terms = BooleanField('I agree to the Terms and Conditions', validators=[DataRequired(message='You must agree to the terms and conditions')])
    submit = SubmitField('Register as Instructor')
    
    def validate_email(self, email):
        # Convert to lowercase for case-insensitive comparison
        self.email.data = email.data.lower().strip()

class StudentProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    grade_level = StringField('Grade Level', validators=[DataRequired()])
    subject_interests = StringField('Subject Interests', validators=[DataRequired()])
    learning_style = StringField('Learning Style', validators=[DataRequired()])
    support_needs = StringField('Support Needed', validators=[DataRequired()])
    goal = StringField('Goal', validators=[DataRequired()])
    submit = SubmitField('Save Profile')

class InstructorProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    bio = TextAreaField('Bio', validators=[DataRequired()])
    area_of_expertise = StringField('Area of Expertise', validators=[DataRequired()])
    teaching_style = StringField('Teaching Style', validators=[DataRequired()])
    years_of_experience = IntegerField('Years of Experience', validators=[DataRequired()])
    subjects_taught = StringField('Subjects Taught', validators=[DataRequired()])
    student_feedback_summary = TextAreaField('Student Feedback Summary')
    submit = SubmitField('Save Profile')