from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from chi.models import User
from flask_login import current_user


class LoginForm (FlaskForm):
	username = StringField('Username or Email', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Login')


class RegistrationForm (FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email('Please input a valid email')])
	password = PasswordField('Password', validators=[DataRequired()])
	password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', 'Sorry, your passwords dont match')])
	submit = SubmitField('SignUp')

	def  validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user :
			raise ValidationError('Sorry that username is already taken please select a different one')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user :
			raise ValidationError('Sorry that email is already taken, please choose a different email')


class AccountForm (FlaskForm) :
	about_me = StringField('About Me')
	email = StringField('Email', validators=[Email('Please input a valid email')])
	profile_pic = FileField('Update Profile', validators=[FileAllowed(['png', 'jpg', 'jpeg'])])
	submit = SubmitField('Update Account')

	def __init__(self, original_user_email, *args, **kwargs):
		super(AccountForm, self).__init__(*args, **kwargs)
		self.original_user_email = original_user_email

	def validate_email(self, email):
		if self.original_user_email != email.data:
			user = User.query.filter_by(email=email.data).first()
			if user :
				raise ValidationError ('Sorry That email already exists, please choose a different one or stick with the current one')



class PostForm (FlaskForm):
	title = StringField ('Title', validators=[DataRequired(), Length(max=100)])
	body = TextAreaField ('Content', validators=[DataRequired(), Length(min=2, max=250)])
	submit = SubmitField ('Post')