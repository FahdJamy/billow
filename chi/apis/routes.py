from chi import api
from flask_restful import Resource
from flask import jsonify, render_template, request
from flask import Blueprint
from chi.models import Messages, User
from flask_login import login_required

appi = Blueprint('appi', __name__)


messages = [
	{
		'sender': 'fahd',
		'receiver': 'wow',
		'msg_date': '11/12/03',
		'body': 'What you doing ryt now'
	},
	{
		'sender': 'fahd',
		'receiver': 'wow',
		'msg_date': '11/12/04',
		'body': 'What you doing ryt now'
	},
	{
		'sender': 'fahd',
		'receiver': 'wow',
		'msg_date': '11/12/05',
		'body': 'What you doing ryt now'
	},
	{
		'sender': 'fahd',
		'receiver': 'mellow',
		'msg_date': '11/12/06',
		'body': 'What you doing ryt now'
	}

]

# api.add_resource(Student, '/student/<string:name>')


@appi.route('/user/messages')
def index():
	return render_template ('messages.html')



class  Student(Resource):
	def get(sel, name):
		return {'student': name}


# creating new stores
@appi.route('/user/newmsg', methods=['POST', 'GET'])
def create_store():
	request_sent = request.get_json()
	new_store = {
		'name': request_sent['name'],
		'item': []
	}
	stores.append(new_store)
	return jsonify(new_store)


# returning all messages
@appi.route('/user/msgs')
# @login_required
def get_stores():
	return jsonify({'messages': messages})


# create item in store
# @appi.route('/store/<string:name>/item', methods=['GET', 'POST'])
# def create_item_in_store(name):
# 	request_sent = request.get_json()
# 	for store in stores:
# 		if store['name'] == name:
# 			new_item = {
# 				'name': request_sent['name'],
# 				'price': request_sent['price']
# 			}
# 			store['items'].append(new_item)
# 			return jsonify(new_item)
# 	return jsonify({'message': 'sorry store doesnt exit'})


# Get messages for users
class MessagesCls(Resource):
	def get(self, name, sender_name):
		for all_message in messages:
			if all_message['receiver'] == name:
				if all_message['sender']  == sender_name:
					return all_message
		return jsonify ({'response' : 'sorry that user is not registered with us'})

	def post(self, receiver, sender):
		pass


class AUsers (Resource):
	def get(self):
		users = [{'username' : user.username, 'profile' : user.profile_pic} for user in User.query.all()]
		
		return jsonify({'Users' : users})


class SUsers (Resource):
	def get(self, name):
		try:
			u = User.query.filter_by(username=name).first()
			if u:
				return jsonify({'user': u.username})
			else:
				return jsonify({'message' : 'No User Found'})
		except :
			raise jsonify({'Message' : 'No Results'})