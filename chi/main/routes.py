from flask import Blueprint, render_template, redirect, url_for, current_app, request
from flask_login import login_required, current_user
from chi.users.forms import PostForm
from chi.models import Post
from chi import db

home = Blueprint('home', __name__)

@home.route('/')
@home.route('/index', methods=['POST', 'GET'])
@login_required
def main():
	title = 'Home'
	form = PostForm()
	page = request.args.get('page', 1, type=int)
	if form.validate_on_submit():
		title = form.title.data
		body = form.body.data
		newpost = Post (title=title, body=body, author=current_user )
		db.session.add(newpost)
		db.session.commit()
		return redirect (url_for ('home.main', username=current_user.username))
	posts = current_user.followed_user_posts().paginate(page, current_app.config['POSTS_PER_PAGE'], False)
	other_posts = url_for('home.main', page=posts.next_num) if posts.has_next else None
	previous_posts = url_for('home.main', page=posts.prev_num) if posts.has_prev else None
	return render_template('main/home.html', posts=posts.items, title=title, form=form, other_posts=other_posts, previous_posts=previous_posts)