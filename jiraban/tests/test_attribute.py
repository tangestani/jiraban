#
# Copyright (c) 2012, Marc Tardif <marc@interunion.ca>
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

from jiraban.attribute import (
    Attribute,
    get_attributes,
    )
from jiraban.properties import String
from jiraban.variables import Variable

from unittest import TestCase


class TestAttribute(TestCase):

    def test_instantiate_with_default_values(self):
        """
        A name and class must be provided when an L{Attribute} is
        instantiated. The only other value defaults to Variable.
        """
        class Class:
            pass

        attribute = Attribute("name", Class)
        self.assertEqual(attribute.name, "name")
        self.assertEqual(attribute.cls, Class)
        self.assertEqual(attribute.variable_factory, Variable)

    def test_instantiate_with_other_values(self):
        """
        In addition to the required values an variable factory
        can be provided when an L{Attribute} is instantiated.
        """
        class Class:
            pass

        class VariableFactory:
            pass

        attribute = Attribute("name", Class, VariableFactory)
        self.assertEqual(attribute.name, "name")
        self.assertEqual(attribute.cls, Class)
        self.assertEqual(attribute.variable_factory, VariableFactory)


class TestGetAttributes(TestCase):

    def test_attribute(self):
        """
        The L{get_attributes} function returns a dictionary with
        each class attribute.
        """
        class Class:
            attr = String()

        attributes = get_attributes(Class)
        self.assertEqual(len(attributes), 1)
        self.assertTrue("attr" in attributes)

    def test_twice(self):
        """Attributes are expensive to get so they are cached."""
        class Class:
            pass

        old_attributes = get_attributes(Class)
        new_attributes = get_attributes(Class)
        self.assertEqual(old_attributes, new_attributes)
