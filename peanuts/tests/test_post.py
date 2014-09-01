"""Unit tests for posts."""


from peanuts.tests.base import RestTestCase
from peanuts.models.post import Post


__all__ = ['PostTest']


class PostTest(RestTestCase):
    """A unit test for Posts."""
    base_url = '/post'

    def test_index(self):
        """Tests /post/ GET."""
        super(PostTest, self)._test_index([
            Post(
                content="""
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
                    eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut
                    enim ad minim veniam, quis nostrud exercitation ullamco laboris
                    nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor
                    in reprehenderit in voluptate velit esse cillum dolore eu
                    fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
                    proident, sunt in culpa qui officia deserunt mollit anim id est
                    laborum.
                """
                )
            ])

    def test_get(self):
        """Tests /post/<id> GET."""
        super(PostTest, self)._test_get(
            Post(content='This is a posting.')
            )

    def test_post(self):
        """Tests /post/ POST."""
        super(PostTest, self)._test_post(
            {'content': 'This is a posting.'}
            )
