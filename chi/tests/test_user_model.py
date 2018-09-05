import unittest
from datetime import datetime, timedelta

class TestUserCase (unittest.TestCase) :
	def setUp(self):
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()


	def test_password_hashing(self):
		u1 = User (username='Winnie', email='wed@wed.com')
		u1.hash_password('google')
		db.session.add(u1)
		db.session.commit()
		self.assertFalse(u1.check_password('facebook'))
		self.assertTrue(u1.check_password('google'))


if __name__ == '__main__':
	unittest.main(verbosity=2)