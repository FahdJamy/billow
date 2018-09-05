import unittest
from datetime import datetime, timedelta
from chi import db, app
from chi.models import Post, User, PaginatedAPIMixin

class TestUserCase (unittest.TestCase) :
	def setUp(self):
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
		db.create_all()
		self.u1 = User (username='Winnie', email='wed@wed.com')
		self.u2 = User (username='Hinnie', email='hen@hen.com')
		self.u3 = User (username='Lorium', email='Lor@Lor.com')
		self.u1.hash_password('google')
		self.u2.hash_password('apple')
		self.u3.hash_password('lor')
		db.session.add_all([self.u1, self.u2, self.u3])
		db.session.commit()

		now = datetime.utcnow()
		self.post1 = Post (title='Mines', body='Football', author=self.u1, 
			date_posted=now + timedelta(seconds=5))
		self.post2 = Post (title='Mines', body='Football', author=self.u2)
		db.session.add_all([self.post1, self.post2])
		db.session.commit()


	def tearDown(self):
		db.session.remove()
		db.drop_all()


	def test_password_hashing(self):
		self.assertFalse(self.u1.check_password('facebook'))
		self.assertTrue(self.u1.check_password('google'))
		


if __name__ == '__main__':
	unittest.main(verbosity=2)
