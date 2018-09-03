from flask import Flask
from flask_mail import Mail
from chi.potants.fathom import Config
from flask_socketio import SocketIO
from flask_restful import Api
from chi.chat.lasses import Messages
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_restful import Api


app = Flask(__name__)
app.config.from_object(Config)

mail = Mail()
socketio = SocketIO()
db = SQLAlchemy(app)
migrate = Migrate()
login = LoginManager()
login.login_view = 'user.login'
api = Api()

api.add_resource(Messages, '/messes')

def app_creator(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	mail.init_app(app)
	socketio.init_app(app)
	api.init_app(app)
	migrate.init_app(app, db)
	login.init_app(app)
	db.init_app(app)

	from chi.email.routes import email
	from chi.chat.routes import chat
	from chi.main.routes import home
	from chi.users.routes import user
	from chi.apis.routes import appi
	app.register_blueprint(email)
	app.register_blueprint(chat)
	app.register_blueprint(home)
	app.register_blueprint(user)
	app.register_blueprint(appi)

	return app

from chi import models
from chi.apis.routes import MessagesCls, AUsers, SUsers
api.add_resource(MessagesCls, '/msgs/user/<string:name>/<string:sender_name>')
api.add_resource(AUsers, '/users/all')
api.add_resource(SUsers, '/user/sing/<string:name>')