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

from jiraban.variables import (
    StringVariable,
    UnicodeVariable,
    ListVariable,
    Variable,
    VariableFactory,
    raise_none_error,
    )

from unittest import TestCase


class Marker:

    def __init__(self, name):
        self.name = name


marker = Marker("marker")


class CustomVariable(Variable):

    def __init__(self, *args, **kwargs):
        self.gets = []
        self.sets = []
        super(CustomVariable, self).__init__(*args, **kwargs)

    def get(self):
        """Cache in L{gets} if the returned value is not None."""
        value = super(CustomVariable, self).get()
        if value is not None:
            self.gets.append(value)

        return value

    def set(self, value):
        """Cache in L{sets} if the given value is not None."""
        super(CustomVariable, self).set(value)
        if value is not None:
            self.sets.append(value)


class TestVariable(TestCase):

    def test_instantiate_with_value(self):
        variable = CustomVariable(value=marker)
        self.assertEqual(variable.sets, [marker])

    def test_instantiate_with_value_factory(self):
        variable = CustomVariable(value_factory=lambda: marker)
        self.assertEqual(variable.sets, [marker])

    def test_instantiate_with_attribute(self):
        variable = CustomVariable(attribute=marker)
        self.assertEqual(variable.attribute, marker)

    def test_get_none(self):
        variable = CustomVariable()
        self.assertIs(variable.get(), None)
        self.assertEqual(variable.sets, [])
        self.assertEqual(variable.gets, [])

    def test_set_get_none(self):
        variable = CustomVariable()
        variable.set(None)
        self.assertIs(variable.get(), None)
        self.assertEqual(variable.sets, [])
        self.assertEqual(variable.gets, [])

    def test_set_none_with_required(self):
        variable = CustomVariable(required=True)
        self.assertRaises(ValueError, variable.set, None)

    def test_get_none_with_required(self):
        variable = CustomVariable(required=True)
        self.assertRaises(ValueError, variable.get)


class TestStringVariable(TestCase):

    def test_set_get_string(self):
        variable = StringVariable()
        variable.set("string")
        self.assertEqual(variable.get(), "string")

    def test_set_get_unicode(self):
        variable = StringVariable()
        variable.set(u"unicode")
        self.assertEqual(variable.get(), "unicode")

    def test_set_get_integer(self):
        variable = StringVariable()
        self.assertRaises(ValueError, variable.set, 0)


class TestUnicodeVariable(TestCase):

    def test_set_get_unicode(self):
        variable = UnicodeVariable()
        variable.set(u"unicode")
        self.assertEqual(variable.get(), u"unicode")

    def test_set_get_string(self):
        variable = UnicodeVariable()
        variable.set("string")
        self.assertEqual(variable.get(), u"string")

    def test_set_get_integer(self):
        variable = UnicodeVariable()
        self.assertRaises(ValueError, variable.set, 0)


class TestListVariable(TestCase):

    def test_set_get_list(self):
        item_factory = VariableFactory(StringVariable)
        variable = ListVariable(item_factory, ",")

        l = ["a", "b"]
        variable.set(l)
        self.assertEqual(variable.get(), l)

    def test_set_get_string(self):
        item_factory = VariableFactory(StringVariable)
        variable = ListVariable(item_factory, ",")

        variable.set("a,b")
        self.assertEqual(variable.get(), ["a", "b"])

    def test_set_get_integer(self):
        item_factory = VariableFactory(StringVariable)
        variable = ListVariable(item_factory, ",")
        self.assertRaises(ValueError, variable.set, 0)


class TestRaiseNoneError(TestCase):

    def test_attribute(self):
        try:
            raise_none_error(marker)
        except ValueError, e:
            pass
        self.assertTrue("marker" in e.message)

    def test_none(self):
        self.assertRaises(ValueError, raise_none_error, None)
