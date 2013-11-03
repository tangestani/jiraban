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
    "UniqueMixin",
    ]

import os
import sys

from itertools import count


class UniqueMixin:

    # This allocates process-wide unique integers.  We count on Python doing
    # only cooperative threading to make this safe across threads.
    _unique_int_counter = count(100000)

    def get_unique_integer(self, bits=None):
        """Return an integer unique to this test instance.

        For each thread, this will be a series of increasing numbers,
        but the starting point will be unique per thread.

        @param bits: Optional number of bits for the integer.
        """
        integer = next(UniqueMixin._unique_int_counter)
        if bits is not None:
            integer = integer % (2 ** bits)

        return integer

    def get_unique_string(self, prefix=None, separator="-"):
        """Return a string unique to this test instance.

        @param prefix: Prefix for the unique string. If
            unspecified, defaults to "generic-string".
        @param separator: Seperator between parts of the unique
            string. If unspecified, defaults to "-".
        """
        if prefix is None:
            frame = sys._getframe(2)
            source_filename = frame.f_code.co_filename
            # Dots and dashes cause trouble with some consumers of these
            # names.
            source = (
                os.path.basename(source_filename)
                .replace("-", separator)
                .replace("_", separator)
                .replace(".", separator))
            prefix = separator.join([
                "unique", "from", source, "line%d" % frame.f_lineno])
        return separator.join([prefix, str(self.get_unique_integer())])
