"""Unit tests for users."""


from peanuts.tests.base import RestTestCase
from peanuts.models.user import User


__all__ = ['UserTest']


class UserTest(RestTestCase):
    """A unit test for Users."""
    base_url = '/user'
    Model = User

    def test_post(self):
        """Tests /user/ POST."""
        super(UserTest, self)._test_post({
            'email': 'test@example.org',
            'password': '123abc',
            'confirm_password': '123abc'
            }, verbosity='self')

        r = self.get('/session/')
        assert r.status_code == 200
        assert 'data' in r.json

        data = r.json['data']
        assert 'user_id' in data

    def test_post_first_admin(self):
        """Tests that an admin may be posted to /user/ POST if there are no
            other users."""
        super(UserTest, self)._test_post({
            'email': 'test@example.org',
            'password': '123abc',
            'confirm_password': '123abc',
            'is_admin': True
            }, verbosity='self')

    def test_post_second_admin(self):
        """Tests that an admin can post a second admin to /user/ POST and stay
            logged in.
        """
        r = self.post(self.base_url + '/', data={
            'email': 'test@example.org',
            'password': '123abc',
            'confirm_password': '123abc',
            'is_admin': True
            }, query_string={'verbosity': 'admin'})
        assert 'data' in r.json
        assert 'id' in r.json['data']
        first_admin_id = r.json['data']['id']

        # The first admin is logged in, create a second.
        r = self.post(self.base_url + '/', data={
            'email': 'test2@example.org',
            'password': '123abc',
            'confirm_password': '123abc',
            'is_admin': True
            })
        assert r.status_code == 201

        # Check that the first admin is still logged in.
        r = self.get('/session/')
        assert 'data' in r.json
        assert 'user_id' in r.json['data']
        assert first_admin_id == r.json['data']['user_id']

    def test_admin_auth(self):
        """Tests that admin permission is needed to post an admin to
            /user/ POST normally.
        """
        user, password = self.data.peanuts_user
        self.login('peanuts', user, password)
        r = self.post(self.base_url + '/', data={
            'email': 'test2@example.org',
            'password': '123abc',
            'confirm_password': '123abc',
            'is_admin': True
            })
        assert r.status_code == 401
