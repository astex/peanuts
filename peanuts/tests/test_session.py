"""Unit tests for sessions (login/logout)."""


from peanuts.tests.base import BaseTestCase
from peanuts.models.user import User, PeanutsAuth


__all__ = ['SessionTest']


class SessionTest(BaseTestCase):
    """A unit test for sessions."""
    base_url = '/session'

    def test_get_401(self):
        """Tests that the /session/ GET endpoint 401s if not logged in."""
        r = self.get(self.base_url + '/')
        assert r.status_code == 401

    def test_delete_401(self):
        """Tests that the /session/ DELETE endpoint 401s if not logged in."""
        r = self.delete(self.base_url + '/')
        assert r.status_code == 401

class AuthPeanutsTest(BaseTestCase):
    """A unit test to create a peanuts user."""
    base_url = '/session/peanuts'

    def test_post(self):
        """Tests /session/peanuts/ POST (logs in)."""
        password = '123abc'
        peanuts_auth = PeanutsAuth(
            email = 'test@example.org',
            password = password
            )
        user = User(
            peanuts_auth = peanuts_auth
            )

        self.db_session.add(user)
        self.commit()

        r = self.post(self.base_url + '/', data={
            'email': peanuts_auth.email,
            'password': password
            })
        assert r.status_code == 200
        assert 'data' in r.json

        data = r.json['data']
        assert 'user_id' in data
        assert data['user_id'] == user.id_
