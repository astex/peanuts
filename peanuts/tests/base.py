"""Base class(es) for performing unit tests."""


from flask import json
from flask.ext.testing import TestCase

from peanuts import create_app
from peanuts.lib.database import db


__all__ = ['BaseTestCase', 'RestTestCase']


class BaseTestCase(TestCase):
    """A base test case."""
    base_url = ''

    def __init__(self, *args, **kargs):
        self.db_session = db.session
        super(BaseTestCase, self).__init__(*args, **kargs)

    def commit(self):
        """Rolls back database commits if they fail."""
        try:
            self.db_session.commit()
        except:
            self.db_session.rollback()

    def create_app(self):
        """Creates the application object."""
        return create_app('config/test.py')

    def setUp(self):
        """Creates the database and requisite models."""
        db.create_all()

    def tearDown(self):
        """Drops the (data)base."""
        db.session.remove()
        db.drop_all()

    def get(self, url, **kargs):
        """A wrapper for TestClient.get()."""
        kargs.update({
            'headers': [('accepts','application/json; charset=utf-8')]
            })
        return self.client.get(url, **kargs)

    def post(self, url, **kargs):
        """A wrapper for TestClient.post()."""
        kargs.update({
            'headers': [
                ('accepts', 'application/json; charset=utf-8'),
                ('content-type', 'application/json; charset=utf-8')
                ],
            'data': json.dumps(kargs.get('data', {}))
            })
        return self.client.post(url, **kargs)

    def put(self, url, **kargs):
        """A wrapper for TestClient.put()."""
        kargs.update({
            'headers': [
                ('accepts', 'application/json; charset=utf-8'),
                ('content-type', 'application/json; charset=utf-8')
                ],
            'data': json.dumps(kargs.get('data', {}))
            })
        return self.client.put(url, **kargs)

    def delete(self, url, **kargs):
        """A wrapper for TestClient.delete()."""
        kargs.update({
            'headers': [('accepts', 'application/json; charset=utf-8')]
            })
        return self.client.delete(url, **kargs)

    def login(self, provider, user, password):
        """Logs in a user via a given auth provider."""
        if provider == 'peanuts':
            return self.post('/session/peanuts/', data={
                'email': user.peanuts_auth.email,
                'password': password
                })
        else:
            raise ValueError('Please use a valid provider.')

class RestTestCase(BaseTestCase):
    """A base test case for RESTful views."""
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

        id_ = str(model.id_)
        r = self.get(
            self.base_url + '/' + id_,
            query_string={'verbosity': 'all'}
            )
        assert r.status_code == 200
        assert 'data' in r.json

        data = r.json['data']
        assert 'id' in data
        assert data['id'] == id_

    def _test_post(self, model_dict, **kargs):
        """Tests the post endpoint of a given view."""
        kargs.setdefault('verbosity', 'all')
        r = self.post(
            self.base_url + '/',
            query_string=kargs,
            data=model_dict
            )
        assert r.status_code == 201
        assert 'data' in r.json

        data = r.json['data']
        assert 'id' in data

        id_ = data['id']
        model = db.session.query(self.Model).get(id_)
        assert model

    def _test_put(self, model, model_dict):
        """Tests the put endpoint of a given view."""
        db.session.add(model)
        db.session.commit()

        id_ = str(model.id_)
        r = self.put(
            self.base_url + '/' + id_,
            query_string={'verbosity': 'all'},
            data=model_dict
            )
        assert r.status_code == 200
        assert 'data' in r.json

        data = r.json['data']
        assert data['id'] == id_

    def _test_delete(self, model):
        """Tests the delete endpoint of a given view."""
        db.session.add(model)
        db.session.commit()

        id_ = str(model.id_)
        r = self.delete(self.base_url + '/' + id_)
        assert r.status_code == 204

        model = db.session.query(self.Model).get(id_)
        assert not model
