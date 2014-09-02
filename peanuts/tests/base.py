"""Base class(es) for performing unit tests."""


from flask import json
from flask.ext.testing import TestCase

from peanuts import create_app
from peanuts.lib.database import db


__all__ = ['RestTestCase']


class RestTestCase(TestCase):
    """A base test case for RESTful views."""
    base_url = ''

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

    def _test_post(self, model_dict):
        """Tests the post endpoint of a given view."""
        r = self.post(
            self.base_url + '/',
            query_string={'verbosity': 'all'},
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

        id_ = str(model.id)
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

        id_ = str(model.id)
        r = self.delete(self.base_url + '/' + id_)
        assert r.status_code == 204

        model = db.session.query(self.Model).get(id_)
        assert not model
