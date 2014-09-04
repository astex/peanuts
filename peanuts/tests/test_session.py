"""Unit tests for sessions (login/logout)."""


from peanuts.tests.base import BaseTestCase


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
