import httplib
from unittest import TestCase

import mock
from faker import Faker

from application import app
from auth.models import User

fake = Faker()


class LoginWithFacebookTest(TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.db.create_all(app=app)
        self.client = app.test_client()
        self.context = app.app_context().__enter__()

    def tearDown(self):
        app.db.drop_all(app=app)
        self.context.__exit__(None, None, None)

    def _test_login_with_facebook(self, status, facebook_id):
        with mock.patch('auth.forms.facebook_connect_form.facebook') as facebook:
            facebook_api = facebook.GraphAPI.return_value
            account_info = {
                'id': facebook_id,
                'name': fake.name(),
            }
            facebook_api.get_object.return_value = account_info

            response = self.client.get('/auth/connect_with_facebook', query_string={
                'code': 'example_code',
            })

        assert response.status_code == status

        users = User.query.all()
        assert len(users) == 1

        user = users[0]
        assert user.facebook_id == account_info['id']
        return user, account_info

    def test_login_with_facebook_as_new_account(self):
        user, account_info = self._test_login_with_facebook(httplib.CREATED, str(fake.pyint()))
        assert user.name == account_info['name']

    def test_login_with_facebook_as_existing_account(self):
        user = User(facebook_id=str(fake.pyint()), name='xxx')
        app.db.session.add(user)
        app.db.session.commit()

        user, account_info = self._test_login_with_facebook(httplib.OK, user.facebook_id)
        assert user.name == 'xxx'


