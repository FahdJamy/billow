from flask import Blueprint, render_template, url_for, request, jsonify, redirect
from chi import socketio, api, db
from flask_socketio import emit
from chi.chat.lasses import Messages
from flask_login import login_required, current_user
from chi.models import Messages

chat = Blueprint('chat', __name__)


@chat.route('/messages/<string:reciever>', methods=['POST', 'GET'])
@login_required
def message(reciever):
	messages = Messages.query.filter_by(recepient=reciever)
	if request.method == 'POST':
		message = request.form['message']
		sender = current_user
		receiver = request.form['receiver']

		newMessage = Messages(user_id=sender, recepient=receiver, msg=message)
		db.session.add(newMessage)
		db.session.commit()

		new_msg = Messages.query.filter_by(id=newMessage.id).first()
		return jsonify({'message': new_msg})

	return render_template('chat.html', messages=messages)

# @socketio.on( 'my_event' )
# def  event_hadler(msg):
# 	message = str(msg)
# 	socketio.emit('my response', msg) #sending new message 4rm the server to 'my_response' event