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
    "ApplicationTestCase",
    ]

import sys

from unittest import TestCase
from cStringIO import StringIO


class ApplicationTestCase(TestCase):

    def setUp(self):
        # Trap stderr.
        self._real_stderr = sys.stderr
        sys.stderr = StringIO()

    def tearDown(self):
        sys.stderr = self._real_stderr
