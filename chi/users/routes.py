from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from .forms import LoginForm, RegistrationForm, AccountForm
from flask_login import logout_user, login_user, current_user, login_required
from chi.models import User, Post
from chi import db
from werkzeug.urls import url_parse
from datetime import datetime
from .utils import save_profile_pic
from .forms import PostForm


user = Blueprint('user', __name__)

@user.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home.main'))
	form = LoginForm()
	if form.validate_on_submit():
		email_or_username = form.username.data
		password = form.password.data
		remember_user = form.remember_me.data

		user_username = User.query.filter_by(username=email_or_username).first()
		user_email = User.query.filter_by(email=email_or_username).first()

		if user_username and user_username.check_password(password):
			login_user(user_username, remember_user)
			next_page = request.args.get('next')
			flash('you\'ve logged in successfully')
			if not next_page or url_parse(next_page).netloc != '':
				next_page = url_for('home.main')
			return redirect (next_page)

		elif user_email and user_email.check_password(password):
			login_user(user_email, remember_user)
			next_page = request.args.get('next')
			flash('you\'ve logged in successfully')
			if not next_page or url_parse(next_page).netloc != '':
				next_page = url_for('home.main')
			return redirect (next_page)

		flash('Sorry your username or email dont match with the password')
		return redirect (url_for('user.login'))
	return render_template('user/login.html', form=form)


@user.route('/signup', methods=['POST', 'GET'])
def signup():
	if current_user.is_authenticated:
		return redirect (url_for('home.main'))
	form = RegistrationForm()
	if form.validate_on_submit():
		username = form.username.data
		email = form.email.data
		password = form.password.data

		new_user = User(username=username, email=email)
		new_user.hash_password(password)
		db.session.add(new_user)
		db.session.commit()
		user = User.query.filter_by(username=username).first()
		login_user(user)
		flash ('your account has been created successfully')
		return redirect (url_for('home.main'))
	return render_template('user/signup.html', form=form)


@user.route('/loriumer/<string:username>', methods=['POST', 'GET'])
@login_required
def timeline(username):
	user = User.query.filter_by(username=username).first_or_404()
	page = request.args.get('page', 1, type=int)
	if not user :
		return redirect (url_for('home.main'))
	form = PostForm()
	if form.validate_on_submit():
		title = form.title.data
		body = form.body.data
		newpost = Post (title=title, body=body, author=current_user )
		db.session.add(newpost)
		db.session.commit()
		return redirect (url_for ('user.timeline', username=current_user.username))
	posts = user.posts.order_by(Post.date_posted.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
	other_posts = url_for('user.timeline', username=user.username, page=posts.next_num) if posts.has_next else None
	previous_posts = url_for('user.timeline', username=user.username, page=posts.prev_num) if posts.has_prev else None

	return render_template('user/timeline.html', user=user, posts=posts.items, form=form, other_posts=other_posts, previous_posts=previous_posts)


@user.route('/account/<string:username>', methods=['POST', 'GET'])
@login_required
def account(username):
	if current_user.username == username :
		user = User.query.filter_by(username=username).first_or_404()
		form = AccountForm(current_user.email)
		profile_pic = form.profile_pic.data
		if form.validate_on_submit():
			if profile_pic :
				profile_img = save_profile_pic (profile_pic)
				user.profile_pic = profile_img
			current_user.email = form.email.data
			current_user.about_me = form.about_me.data
			db.session.commit()
		elif request.method == 'GET':
			form.email.data = current_user.email
			if current_user.about_me :
				form.about_me.data = current_user.about_me
		user_profile_pic = url_for( 'static', filename='profilePics' + user.profile_pic )
		return render_template ('user/account.html', user_profile=user_profile_pic, form=form)
	return redirect ( url_for ('home.main'))


@user.route('/follow/user/<string:username>')
@login_required
def follow(username):
	user = User.query.filter_by(username=username).first_or_404()
	if user is None :
		flash ('sorry no user found')
		return redirect (url_for('home.main'))
	if user == current_user:
		flash ('sorry you can\'t follow your self')
		return redirect ( url_for ('user.timeline', username=username))
	current_user.follow_user (user)
	db.session.commit ()
	return redirect (url_for('user.timeline', username=username))


@user.route('/unfollow/user/<string:username>')
@login_required
def unfollow(username):
	user = User.query.filter_by(username=username).first_or_404()
	if user is None :
		flash ('sorry no user found')
		return redirect (url_for('home.main'))
	if user == current_user:
		flash ('sorry you can\'t follow your self')
		return redirect ( url_for ('user.timeline', username=username))
	current_user.unfollow_user (user)
	db.session.commit ()
	return redirect (url_for('user.timeline', username=username))


@user.route('/all/users')
@login_required
def allusers():
	users = User.query.all()
	return render_template ('user/users.html', users=users)


@user.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('user.login'))

@user.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.today()
		db.session.commit()