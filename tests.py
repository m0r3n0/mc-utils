import os
import unittest

from config import basedir
from app import app, db
from app.models import User

class TestCase(unittest.TestCase):

    # run always before our tests
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    # run always after our tests
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # set of tests
    def test_avatar(self):
        u = User(nickname='john', email='john@example.com', social_id='TEST-John')
        avatar = u.avatar(128)
        expected = 'http://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6'
        assert avatar[0:len(expected)] == expected


if __name__ == '__main__':
    unittest.main()


