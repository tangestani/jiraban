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

from jiraban.properties import (
    List,
    PropertyAttribute,
    PropertyType,
    String,
    Unicode,
    )
from jiraban.variables import (
    ListVariable,
    StringVariable,
    UnicodeVariable,
    Variable,
    get_variable,
    )

from unittest import TestCase


class FakeVariable(Variable):
    pass


class FakeType(PropertyType):
    variable_class = FakeVariable


class TestProperty(TestCase):

    def setUp(self):
        class Class:
            prop1 = FakeType()
            prop2 = FakeType()
            prop3 = FakeType(default=50, required=True)

        class SubClass(Class):
            pass

        self.Class = Class
        self.SubClass = SubClass

    def test_attribute(self):
        self.assertTrue(isinstance(self.Class.prop1, PropertyAttribute))

    def test_cls(self):
        self.assertEqual(self.Class.prop1.cls, self.Class)
        self.assertEqual(self.Class.prop2.cls, self.Class)
        self.assertEqual(self.SubClass.prop1.cls, self.SubClass)
        self.assertEqual(self.SubClass.prop2.cls, self.SubClass)
        self.assertEqual(self.Class.prop1.cls, self.Class)
        self.assertEqual(self.Class.prop2.cls, self.Class)

    def test_cls_reverse(self):
        self.assertEqual(self.SubClass.prop1.cls, self.SubClass)
        self.assertEqual(self.SubClass.prop2.cls, self.SubClass)
        self.assertEqual(self.Class.prop1.cls, self.Class)
        self.assertEqual(self.Class.prop2.cls, self.Class)
        self.assertEqual(self.SubClass.prop1.cls, self.SubClass)
        self.assertEqual(self.SubClass.prop2.cls, self.SubClass)

    def test_name(self):
        self.assertEqual(self.Class.prop1.name, "prop1")

    def test_variable_factory(self):
        variable = self.Class.prop1.variable_factory()
        self.assertTrue(isinstance(variable, FakeVariable))

        variable = self.Class.prop3.variable_factory()
        self.assertTrue(isinstance(variable, FakeVariable))

    def test_coerce(self):
        prop = FakeType()
        self.assertEqual(prop.coerce(None), None)
        self.assertEqual(prop.coerce(0), 0)

    def test_default(self):
        obj = self.SubClass()
        self.assertEqual(obj.prop1, None)
        self.assertEqual(obj.prop2, None)
        self.assertEqual(obj.prop3, 50)

    def test_set_get(self):
        obj = self.Class()
        obj.prop1 = 10
        obj.prop2 = 20
        obj.prop3 = 30
        self.assertEqual(obj.prop1, 10)
        self.assertEqual(obj.prop2, 20)
        self.assertEqual(obj.prop3, 30)

    def test_set_get_none(self):
        obj = self.Class()
        obj.prop1 = None
        obj.prop2 = None
        self.assertEqual(obj.prop1, None)
        self.assertEqual(obj.prop2, None)
        self.assertRaises(ValueError, setattr, obj, "prop3", None)

    def test_set_get_subclass(self):
        obj = self.SubClass()
        obj.prop1 = 10
        obj.prop2 = 20
        obj.prop3 = 30
        self.assertEqual(obj.prop1, 10)
        self.assertEqual(obj.prop2, 20)
        self.assertEqual(obj.prop3, 30)

    def test_set_get_explicitly(self):
        obj = self.Class()
        prop1 = self.Class.prop1
        prop2 = self.Class.prop2
        prop3 = self.Class.prop3
        prop1.__set__(obj, 10)
        prop2.__set__(obj, 20)
        prop3.__set__(obj, 30)
        self.assertEqual(prop1.__get__(obj), 10)
        self.assertEqual(prop2.__get__(obj), 20)
        self.assertEqual(prop3.__get__(obj), 30)

    def test_set_get_subclass_explicitly(self):
        obj = self.SubClass()
        prop1 = self.Class.prop1
        prop2 = self.Class.prop2
        prop3 = self.Class.prop3
        prop1.__set__(obj, 10)
        prop2.__set__(obj, 20)
        prop3.__set__(obj, 30)
        self.assertEqual(prop1.__get__(obj), 10)
        self.assertEqual(prop2.__get__(obj), 20)
        self.assertEqual(prop3.__get__(obj), 30)


class PropertyMixin:

    def setup(self, property, *args, **kwargs):
        prop2_kwargs = kwargs.pop("prop2_kwargs", {})

        class Class:
            prop1 = property(*args, **kwargs)
            prop2 = property(**prop2_kwargs)

        class SubClass(Class):
            pass

        self.Class = Class
        self.SubClass = SubClass
        self.obj = SubClass()
        self.attribute1 = self.SubClass.prop1
        self.attribute2 = self.SubClass.prop2
        self.variable1 = get_variable(self.obj, self.attribute1)
        self.variable2 = get_variable(self.obj, self.attribute2)


class TestString(PropertyMixin, TestCase):

    def test_str(self):
        self.setup(String, default="def", required=True)

        self.assertTrue(isinstance(self.attribute1, PropertyAttribute))
        self.assertTrue(isinstance(self.attribute2, PropertyAttribute))
        self.assertEqual(self.attribute1.name, "prop1")
        self.assertEqual(self.attribute1.cls, self.SubClass)
        self.assertEqual(self.attribute2.name, "prop2")
        self.assertEqual(self.attribute2.cls, self.SubClass)
        self.assertTrue(isinstance(self.variable1, StringVariable))
        self.assertTrue(isinstance(self.variable2, StringVariable))

        self.assertEqual(self.obj.prop1, "def")
        self.assertRaises(ValueError, setattr, self.obj, "prop1", None)
        self.obj.prop2 = None
        self.assertEqual(self.obj.prop2, None)

        self.assertRaises(ValueError, setattr, self.obj, "prop1", 0)


class TestUnicode(PropertyMixin, TestCase):

    def test_unicode(self):
        self.setup(Unicode, default=u"def", required=True)

        self.assertTrue(isinstance(self.attribute1, PropertyAttribute))
        self.assertTrue(isinstance(self.attribute2, PropertyAttribute))
        self.assertEqual(self.attribute1.name, "prop1")
        self.assertEqual(self.attribute1.cls, self.SubClass)
        self.assertEqual(self.attribute2.name, "prop2")
        self.assertEqual(self.attribute2.cls, self.SubClass)
        self.assertTrue(isinstance(self.variable1, UnicodeVariable))
        self.assertTrue(isinstance(self.variable2, UnicodeVariable))

        self.assertEqual(self.obj.prop1, u"def")
        self.assertRaises(ValueError, setattr, self.obj, "prop1", None)
        self.obj.prop2 = None
        self.assertEqual(self.obj.prop2, None)

        self.assertRaises(ValueError, setattr, self.obj, "prop1", 0)


class TestList(PropertyMixin, TestCase):

    def test_list(self):
        self.setup(List, default_factory=list, required=True)

        self.assertTrue(isinstance(self.attribute1, PropertyAttribute))
        self.assertTrue(isinstance(self.attribute2, PropertyAttribute))
        self.assertEqual(self.attribute1.name, "prop1")
        self.assertEqual(self.attribute1.cls, self.SubClass)
        self.assertEqual(self.attribute2.name, "prop2")
        self.assertEqual(self.attribute2.cls, self.SubClass)
        self.assertTrue(isinstance(self.variable1, ListVariable))
        self.assertTrue(isinstance(self.variable2, ListVariable))

        self.assertEqual(self.obj.prop1, [])
        self.assertRaises(ValueError, setattr, self.obj, "prop1", None)
        self.obj.prop2 = None
        self.assertEqual(self.obj.prop2, None)

        self.obj.prop1 = ["a"]
        self.assertEqual(self.obj.prop1, ["a"])
        self.obj.prop1.append("b")
        self.assertEqual(self.obj.prop1, ["a", "b"])

    def test_default(self):
        self.assertRaises(ValueError, List, default=[])
