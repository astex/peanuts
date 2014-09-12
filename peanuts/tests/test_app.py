"""Tests regarding app protection of the API."""


from peanuts.tests.base import BaseTestCase


class AppTestCase(BaseTestCase):
    """A series of tests that confirm that the API requires an application token
        to function.
    """
    def test_forbidden(self):
        """Tests that access is forbidden if no app token is provided.

            In order to get a CSRF token, an application token is sent in, so
            this will only succeed if providing a token works *and* not
            providing a token fails.
        """
        r = self.client.get('/csrf/', headers=[
            ('accepts', 'application/json; charset=utf-8'),
            ('x-peanuts-csrf', self.csrf)
            ])

        assert r.status_code == 403
