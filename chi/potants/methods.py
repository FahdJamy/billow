from flask import current_app
from chi import mail, app
from flask_mail import Message
from itsdangerous import TimedJSONWebSignatureSerializer as TokenSerial



def token_generator():
	expiration_d = 1800
	token_serializer = TokenSerial(app.config['SECRET_KEY'], expiration_d)
	token = token_serializer.dumps({'user_id': 1}).decode('utf-8')
	return token

def token_verifier(token):
	token_serializer = TokenSerial(app.config['SECRET_KEY'])
	try:
		user_id = token_serializer.loads(token).user_id
	except:
		return None
	user = user_id
	return user


def mail_sender():
	msg = Message('Confirmation', sender='nonreply@replies.com', recipients=['fahdjamy2@gmail.com'])
	msg.body = f'''For confiramtion of the Email please follow the link below and complete registation
link@link.com
if you did not send this please simply ignore this message

Thanks'''
	mail.send(msg)