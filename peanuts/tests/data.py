"""A collections of static fixtures for testing."""


import uuid

from peanuts.models.user import PeanutsAuth, User
from peanuts.models.app import Application


__all__ = ['Fixtures']


class Fixtures(object):
    """A collection of fixtures."""
    def __init__(self, db_session):
        self.db_session = db_session

    def commit(self):
        """Commits the database session.  Rolls back on failure."""
        try:
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            raise e

    @property
    def peanuts_user(self):
        """A peanuts user.

            Returns:
                (tuple (user, password))
        """
        password = '123abc'
        peanuts_auth = PeanutsAuth(
            email='test@example.org',
            password=password
            )
        user = User(peanuts_auth=peanuts_auth)

        self.db_session.add(user)
        self.commit()

        return user, password

    @property
    def peanuts_admin_user(self):
        """A peanuts user with admin permission.

            Returns:
                (tuple (user, password))
        """
        password = '123abc'
        peanuts_auth = PeanutsAuth(
            email='test1@example.org',
            password=password
            )
        user = User(
            is_admin=True,
            peanuts_auth=peanuts_auth
            )

        self.db_session.add(user)
        self.commit()

        return user, password

    @property
    def test_app(self):
        """A test application."""
        test_app = Application(
            title='Test',
            description='An application to use for unit testing.',
            token=str(uuid.uuid4())
            )

        self.db_session.add(test_app)
        self.commit()

        return test_app
