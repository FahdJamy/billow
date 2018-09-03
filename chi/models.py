from chi import db, app, login
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from hashlib import md5


@login.user_loader
def load_user(id):
	return User.query.get(int(id))


followers = db.Table ('followers', 
		db.Column ('followed_user_id', db.Integer, db.ForeignKey('user.id')),
		db.Column ('follower_id', db.Integer, db.ForeignKey('user.id'))
	)


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), index=True, unique=True, nullable=False)
	email = db.Column(db.String(60), index=True, unique=True, nullable=False)
	password = db.Column(db.String(130), nullable=False)
	account_date = db.Column(db.DateTime, default=datetime.utcnow)
	profile_pic = db.Column(db.String(25), default='profile.png')
	last_seen = db.Column(db.DateTime, default=datetime.utcnow)
	about_me = db.Column(db.String(200), nullable=True)
	posts = db.relationship('Post', backref='author', lazy='dynamic')
	messages = db.relationship('Messages', backref='sender', lazy='dynamic')
	followed_user = db.relationship ('User', secondary=followers,
			primaryjoin=(followers.c.follower_id == id), 
			secondaryjoin=(followers.c.followed_user_id == id), 
			backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

	# Checking for user following realtionshipp
	def is_following(self, user):
		if self.id == user.id:
			return f' sorry you cant follow your self'
		return self.followed_user.filter(followers.c.followed_user_id == user.id).count() > 0

	# Follow user
	def follow_user(self, user):
		if not self.is_following(user):
			self.followed_user.append(user)

	# Unfollow user
	def unfollow_user(self, user):
		if self.is_following(user):
			self.followed_user.remove(user)


	def avatar_pic(self, size):
		profile_img = md5(self.email.lower().encode('Utf-8')).hexdigest()
		return f'https://www.gravatar.com/avatar/{profile_img}?d=identicon&s={size}'

	def hash_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password, password)

	def __repr__(self):
		return f'{self.username} has email {self.email}'


	def followed_user_posts(self):
		followed_posts = Post.query.join(followers, 
				(followers.c.followed_user_id == Post.user_id)).filter(followers.c.follower_id == self.id)
		user_posts = Post.query.filter_by(user_id=self.id)
		return followed_posts.union(user_posts).order_by(Post.date_posted.desc())


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	body = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	date_posted = db.Column(db.DateTime, index=True, nullable=False, default=datetime.utcnow)

	def __repr__(self):
		return f'Title : {self.title} - Date Created: '


class Messages(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	recepient = db.Column(db.String(128), nullable=False)
	msg_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	msg = db.Column(db.Text, nullable=False)

	def __repr__(self):
		return f'{ self.user_id } -- {self.msg} to { self.recepient }'