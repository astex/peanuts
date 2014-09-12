"""Tests regarding csrf protection of the API."""


from peanuts.tests.base import BaseTestCase


class CSRFTestCase(BaseTestCase):
    """A series of tests that confirm CSRF protection is working as necessary.
    """
    def test_get(self):
        """Tests that we can receive a csrf token."""
        r = self.client.get('/csrf/', headers=[
            ('accepts', 'application/json; charset=utf-8'),
            ('x-peanuts-application', self.test_app.token)
            ])

        assert r.status_code == 200
        assert r.json.get('csrf')

    def test_forbidden(self):
        """Tests that accessing an endpoint without a csrf token fails."""
        r = self.client.get('/api/session/', headers=[
            ('accepts', 'application/json; charset=utf-8'),
            ('x-peanuts-application', self.test_app.token)
            ])

        assert r.status_code == 403

    # NOTE There is no test for correct usage here since that would depend on
    #   testing the validity of other GET endpoints (which is done anyway). If
    #   all requests (including GET) are failing, failure of the CSRF protection
    #   is one possilble culprit.
