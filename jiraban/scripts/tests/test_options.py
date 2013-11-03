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

from optparse import (
    OptionParser,
    OptionValueError,
    )
from unittest import TestCase

from jiraban.scripts.options import (
    AttributeOption,
    check_attribute,
    )
from jiraban.scripts.tests.cases import ApplicationTestCase


class TestCheckAttribute(TestCase):

    def test_valid(self):
        self.assertEqual(check_attribute(None, "-a", "id"), "id")

    def test_invalid(self):
        self.assertRaises(
            OptionValueError, check_attribute, None, "-a", "test")


class TestAttributeOption(ApplicationTestCase):

    def setUp(self):
        super(TestAttributeOption, self).setUp()
        self.parser = OptionParser(option_class=AttributeOption)
        self.parser.add_option("--attribute", type="attribute")

    def test_valid(self):
        self.parser.parse_args(["--attribute=id"])

    def test_invalid(self):
        self.assertRaises(
            SystemExit, self.parser.parse_args, ["--attribute=test"])
