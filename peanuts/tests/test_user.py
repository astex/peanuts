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

        r = self.client.get('/session/', headers=[
            ('accepts', 'application/json; charset=utf-8')
            ])
        assert r.status_code == 200
        assert 'data' in r.json

        data = r.json['data']
        assert 'user_id' in data
