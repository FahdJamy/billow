from chi import api, db
from flask_restful import Resource
from flask import jsonify, render_template, request, url_for
from flask import Blueprint
from chi.models import Messages, User
from flask_login import login_required
from .errors import bad_request

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

# Get messages for users
class MessagesCls (Resource):
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


@appi.route('/api/users/<int:id>')
def get_user(id):
	return jsonify(User.query.get_or_404(id).py_dict())


@appi.route('/api/users', methods=['GET'])
def get_users():
	page = request.args.get('page', 1, type=int)
	per_page = min(request.args.get('page', 10, type=int), 50)
	data = User.to_dict_collection(User.query, page, per_page, 'appi.get_users')
	return jsonify(data)

@appi.route('/api/users/followers/<int:id>', methods=['GET'])
def user_followers(id):
	user = User.query.get_or_404(id)
	page = request.args.get('page', 1, type=int)
	per_page = min(request.args.get('page', 1, type=int), 50)
	data = User.to_dict_collection(user.followers, page, per_page, 'appi.user_followers', id=id)
	return jsonify(data)


@appi.route('/api/users/followed/<int:id>', methods=['GET'])
def followed_users(id):
	user = User.query.get_or_404(id)
	page = request.args.get('page', 1, type=int)
	per_page = min(request.args.get('page', 1, type=int), 50)
	data = User.to_dict_collection(user.followed_user, page, per_page, 'appi.followed_users', id=id)
	return jsonify(data)

@appi.route('/api/users', methods=['POST'])
def new_user():
	data = request.get_json()
	if 'username' not in data or 'email' not in data or 'password' not in data :
		return bad_request('Sorry you miss the email, username and password fields')
	if User.query.filter_by(username=data['username']).first():
		return bad_request('sorry that username already exists')
	if User.query.filter_by(email=data['email']).first():
		return bad_request('sorry that email already exists')
	user = User()
	user.py_dict_to_model(data, new_user=True)
	db.session.add(user)
	db.session.commit()
	response = jsonify(user.py_dict())
	response.status_code = 201
	response.headers['location'] = url_for('appi.get_user', id=user.id)
	return response

@appi.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
	user = User.query.get_or_404(id)
	data = request.get_json() or {}
	if 'username' in data and data['username'] != user.username and User.query.filter_by(username=data['username']).first() :
		bad_request('please choose a different username')
	if 'email' in data and data['email'] != user.email and User.query.filter_by(email=data['email']).first() :
		bad_request('please choose a different email')
	user.py_dict_to_model(data, new_user=False)
	db.session.commit()
	return jsonify(user.py_dict())