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

from jiraban.colors import (
    hsv_colors,
    html_colors,
    rgb_colors,
    )

from fractions import Fraction
from unittest import TestCase


class ColorsMixin:

    def test_none(self):
        """
        No colors returns an empty list.
        """
        self.assertEqual(self.create_colors(0), [])

    def test_count(self):
        """
        The same number of items are returned as the given n.
        """
        for i in 1, 10, 15:
            self.assertEqual(len(self.create_colors(i)), i)

    def test_always_same(self):
        """
        Colors returned are always the same for a given n.
        """
        old = self.create_colors(10)
        new = self.create_colors(10)
        self.assertEqual(old, new)

    def test_always_start_the_same(self):
        """
        Colors for different n always start the same.
        """
        old = self.create_colors(1)
        new = self.create_colors(10)
        self.assertEqual(old, new[:1])

    def test_only_appear_once(self):
        """
        Each color only appears once in the returned list.
        """
        colors = self.create_colors(1)
        for c in colors:
            self.assertEqual(colors.count(c), 1)


class TestHsvColors(ColorsMixin, TestCase):

    def create_colors(self, n):
        return list(hsv_colors(n))

    def test_type(self):
        """
        An HSV color consists of three fractions.
        """
        h, s, v = self.create_colors(1)[0]
        self.assertTrue(isinstance(h, Fraction))
        self.assertTrue(isinstance(s, Fraction))
        self.assertTrue(isinstance(v, Fraction))


class TestRgbColors(ColorsMixin, TestCase):

    def create_colors(self, n):
        return list(rgb_colors(n))

    def test_type(self):
        """
        An RGB color consists of three fractions.
        """
        r, g, b = self.create_colors(1)[0]
        self.assertTrue(isinstance(r, float))
        self.assertTrue(isinstance(g, float))
        self.assertTrue(isinstance(b, float))


class TestHtmlColors(ColorsMixin, TestCase):

    def create_colors(self, n):
        return list(html_colors(n))

    def test_type(self):
        """
        An HTML color consists of a 7 character string.
        """
        html = self.create_colors(1)[0]
        self.assertTrue(isinstance(html, str))
        self.assertEqual(len(html), 7)
