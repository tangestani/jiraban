#
# Copyright (c) 2013, Marc Tardif <marc@interunion.ca>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
__metaclass__ = type

__all__ = []

from unittest import TestCase
from urlparse import urlparse

from jiraban.testing.unique import UniqueMixin


class TestUniqueMixin(UniqueMixin, TestCase):

    def test_get_unique_integer_twice(self):
        """
        When getting a unique integer twice, the same integer should not
        be returned.
        """
        self.assertNotEqual(
            self.get_unique_integer(), self.get_unique_integer())

    def test_get_unique_integer_with_bits(self):
        """
        When getting a unique integer with bits, the integer should be
        contained within that number of bits.
        """
        bits = 2
        for i in xrange((2 ** bits) + 1):
            integer = self.get_unique_integer(bits=bits)
            self.assertTrue(integer >= 0)
            self.assertTrue(integer < 2 ** bits)

    def test_get_unique_string_twice(self):
        """
        When getting a unique string twice, the same string should not
        be returned.
        """
        self.assertNotEqual(
            self.get_unique_string(), self.get_unique_string())

    def test_get_unique_string_with_prefix(self):
        """
        When getting a unique string with a prefix, the string should
        start with that prefix.
        """
        string = self.get_unique_string(prefix="with-my-prefix")
        self.assertTrue(string.startswith("with-my-prefix"))

    def test_get_unique_string_with_separator(self):
        """
        When getting a unique string with a separator, the string should
        contain that separator between its parts.
        """
        string = self.get_unique_string(separator="*")
        self.assertTrue("*" in string)
