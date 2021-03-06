"""Unit tests for sessions (login/logout)."""


from peanuts.tests.base import BaseTestCase
from peanuts.models.user import User, PeanutsAuth


__all__ = ['SessionTest']


class SessionTest(BaseTestCase):
    """A unit test for sessions."""
    base_url = '/api/session'

    def test_get_401(self):
        """Tests that the /session/ GET endpoint 401s if not logged in."""
        r = self.get(self.base_url + '/')
        assert r.status_code == 401

    def test_get(self):
        """Tests /session/ GET."""
        user, password = self.data.peanuts_user
        self.login('peanuts', user, password)

        r = self.get(self.base_url + '/')
        assert r.status_code == 200
        assert 'data' in r.json

        data = r.json['data']
        assert 'user_id' in data
        assert data['user_id'] == user.id_

    def test_delete_401(self):
        """Tests that the /session/ DELETE endpoint 401s if not logged in."""
        r = self.delete(self.base_url + '/')
        assert r.status_code == 401

    def test_delete(self):
        """Tests /session/ DELETE."""
        user, password = self.data.peanuts_user
        self.login('peanuts', user, password)

        r = self.delete(self.base_url + '/')
        assert r.status_code == 200

        # Confirm the logout.
        r = self.get(self.base_url + '/')
        assert r.status_code == 401

class AuthPeanutsTest(BaseTestCase):
    """A unit test to create a peanuts user."""
    def test_post(self):
        """Tests /session/peanuts/ POST (logs in)."""
        user, password = self.data.peanuts_user
        r = self.login('peanuts', user, password)
        assert r.status_code == 200
        assert 'data' in r.json

        data = r.json['data']
        assert 'user_id' in data
        assert data['user_id'] == user.id_
