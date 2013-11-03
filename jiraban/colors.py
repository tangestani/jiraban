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

__all__ = [
    "hsv_colors",
    "html_colors",
    "rgb_colors",
    ]

from colorsys import hsv_to_rgb
from fractions import Fraction
from itertools import (
    count,
    islice,
    )


def iter_zenos():
    """
    http://en.wikipedia.org/wiki/Zeno%27s_paradoxes
    """
    for k in count():
        yield Fraction(1, 2 ** k)


def iter_fractions():
    """
    [Fraction(0, 1), Fraction(1, 2), Fraction(1, 4), Fraction(3, 4), ...]
    [0.0, 0.5, 0.25, 0.75, ...]
    """
    yield Fraction(0, 1)
    for k in iter_zenos():
        i = k.denominator
        for j in range(1, i, 2):
            yield Fraction(j, i)


def hsv_colors(n):
    """Return n colors as an HSV tuple of C{Fractions}."""
    s = Fraction(2, 10)
    v = Fraction(9, 10)
    for h in islice(iter_fractions(), n):
        yield (h, s, v)


def rgb_colors(n):
    """Return n colors as an RGB tuple of C{floats}."""
    for hsv in hsv_colors(n):
        r, g, b = hsv_to_rgb(*hsv)
        yield (float(r), g, b)


def html_colors(n):
    """Return n colors as an HTML string starting with a hash (#)."""
    for rgb in rgb_colors(n):
        yield "#" + "".join(["%02x" % int(c * 255) for c in rgb])
