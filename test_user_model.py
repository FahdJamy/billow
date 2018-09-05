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

	def test_avatar	(self):
		result = self.u2.avatar_pic (128)
		self.assertEqual (result, ('https://www.gravatar.com/avatar/'
                                         '1d708d7f95591b518dc5b759aec3c27b'
                                         '?d=identicon&s=128'))

	# test Follow
	def test_user_follow_case(self):
		self.assertEqual (self.u2.followed_user.all(), [])
		self.assertEqual (self.u2.followers.all(), [])

		self.u2.followed_user.append (self.u1)
		db.session.commit()
		self.assertTrue (self.u2.is_following(self.u1))
		self.assertFalse (self.u2.is_following(self.u3))

		self.u3.follow_user (self.u1)
		self.u3.follow_user (self.u2)
		self.u3.unfollow_user (self.u1)
		db.session.commit()

		self.assertTrue (self.u3.is_following(self.u3))
		self.assertTrue (self.u3.is_following(self.u2))
		self.assertFalse (self.u3.is_following(self.u1))
		self.assertEqual (self.u3.followers.count(), 0)
		self.assertEqual (self.u3.followed_user.count(), 1)


	def test_followed_posts(self):
		self.u3.follow_user (self.u1) # Lorium follow Winnie
		self.u3.follow_user (self.u2) # Lorium follow Winnie
		self.u2.follow_user (self.u1) # Hinnie follow Winnie
		db.session.commit()

		r3 = self.u3.followed_user_posts ().all()
		r2 = self.u2.followed_user_posts ().all()
		r1 = self.u1.followed_user_posts ().all()

		self.assertEqual (r3, [self.post1, self.post2])
		self.assertEqual (r2, [self.post1, self.post2])
		self.assertEqual (r1, [self.post1])

		


if __name__ == '__main__':
	unittest.main(verbosity=2)