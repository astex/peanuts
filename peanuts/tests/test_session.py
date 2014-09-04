"""Unit tests for sessions (login/logout)."""


from peanuts.tests.base import RestTestCase


__all__ = ['SessionTest']


class SessionTest(RestTestCase):
    """A unit test for sessions."""
    base_url = '/session'

    def test_get_401(self):
        """Tests that the /session/ GET endpoint 401s if not logged in."""
        r = self.get(self.base_url + '/')
        assert r.status_code == 401
