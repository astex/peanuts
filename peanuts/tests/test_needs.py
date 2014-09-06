"""A module to test the behavior of the Need class."""


import unittest

from peanuts.lib.auth import Need


__all__ = ['TestNeed']


class TestNeed(unittest.TestCase):
    """Tests peanuts.lib.auth.Need."""
    def setUp(self):
        self.need = Need()

    def test_need(self):
        assert self.need()

    def test_invert_need(self):
        assert not (~self.need)()

    def test_or_need(self):
        assert (self.need | self.need)()
        assert (~self.need | self.need)()
        assert (self.need | ~self.need)()
        assert not (~self.need | ~self.need)()

    def test_and_need(self):
        assert (self.need & self.need)()
        assert not (~self.need & self.need)()
        assert not (self.need & ~self.need)()
        assert not (~self.need & ~self.need)()
