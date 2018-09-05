from flask import Blueprint, render_template
from flask_mail import Message
from chi import mail

email = Blueprint('email', __name__)

@email.route('/email')
def mail_sender():
	msg = Message('Confirmation Email', sender='noreply@replies.com', recipients=['fahdjamy2@gmail.com'])
	msg.body = f'''To complete your registration please click the following link
link@link.com
if you you werent the one who sent sent this please simply ignore this message
Thanks
'''
	mail.send(msg)
	return 'Message sent'