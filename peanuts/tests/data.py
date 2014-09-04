"""A collections of static fixtures for testing."""


from peanuts.models.user import PeanutsAuth, User


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
