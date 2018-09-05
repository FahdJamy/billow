import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
	SECRET_KEY = os.environ.get('SECRET_KEY') or '8ffb275e274afe8cfb8d6e62573e4a'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'lorium.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	MAIL_SERVER = 'smtp.google.mail'
	MAIL_PORT = 465 # for SSL
	MAIL_USE_SSL = True
	MAIL_USERNAME = os.environ.get('USER_EMAIL')
	MAIL_PASSWORD = os.environ.get('USER_PASSWORD')
	POSTS_PER_PAGE = 2
	
	DEBUG = True


class Deploy(Config):
	DEBUG = False