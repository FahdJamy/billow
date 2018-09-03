from chi import app_creator
from datetime import datetime

app = app_creator()

from chi import db
from chi.models import User, Post

@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User}


from flask import render_template
@app.errorhandler(404)
def not_found(error):
	return render_template ('errors/404.html')

@app.errorhandler(500)
def internal_server_error(error):
	db.session.rollback()
	return render_template ('errors/500.html')

if __name__ == '__main__':
	app.run()