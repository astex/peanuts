"""Base class(es) for performing unit tests."""


from flask.ext.testing import TestCase

from peanuts import create_app
from peanuts.database import db


__all__ = ['RestTestCase']


class RestTestCase(TestCase):
    """A base test case for RESTful views."""
    base_url = ''

    def create_app(self):
        """Creates the application object."""
        return create_app('../config/test.py')

    def setUp(self):
        """Creates the database and requisite models."""
        db.create_all()

    def tearDown(self):
        """Drops the (data)base."""
        db.session.remove()
        db.drop_all()

    def get(self, url, **kargs):
        """A wrapper for Session.get() which appends the base_url and
            metadata.
        """
        kargs.update({
            'headers': [('accepts','application/json; charset=utf-8')]
            })
        return self.client.get(url, **kargs)

    def _test_index(self, models):
        """Tests the index endpoint of a given view."""
        for model in models:
            db.session.add(model)
        db.session.commit()

        r = self.get(self.base_url + '/', query_string={'verbosity': 'all'})
        assert r.status_code == 200
        assert 'data' in r.json

        data = r.json['data']
        assert len(data) > 0
        assert all(['id' in d for d in data])

    def _test_get(self, model):
        """Tests the get endpoint of a given view."""
        db.session.add(model)
        db.session.commit()

        id_ = str(model.id)
        r = self.get(
            self.base_url + '/' + id_,
            query_string={'verbosity': 'all'}
            )
        assert r.status_code == 200
        assert 'data' in r.json

        data = r.json['data']
        assert data['id'] == id_
