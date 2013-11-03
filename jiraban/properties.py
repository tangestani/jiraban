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

__all__ = [
    "List",
    "String",
    "Unicode",
    ]

from jiraban.attribute import Attribute
from jiraban.variables import (
    ListVariable,
    StringVariable,
    UnicodeVariable,
    VariableFactory,
    Variable,
    get_variable,
    )


class Property:

    def __init__(self, variable_class=Variable, variable_kwargs={}):
        self._variable_class = variable_class
        self._variable_kwargs = variable_kwargs

    def __get__(self, obj, cls=None):
        if obj is None:
            return self._get_attribute(cls)
        if cls is None:
            cls = type(obj)
        attribute = self._get_attribute(cls)
        variable = get_variable(obj, attribute)
        return variable.get()

    def __set__(self, obj, value):
        cls = type(obj)
        attribute = self._get_attribute(cls)
        variable = get_variable(obj, attribute)
        variable.set(value)

    def _detect_name(self, used_cls):
        self_id = id(self)
        for cls in used_cls.__mro__:
            for attr, prop in cls.__dict__.iteritems():
                if id(prop) == self_id:
                    return attr
        raise RuntimeError("Property used in an unknown class")

    def _get_attribute(self, cls):
        try:
            attribute = cls.__dict__["_attributes"].get(self)
        except KeyError:
            cls._attributes = {}
            attribute = None

        if attribute is None:
            name = self._detect_name(cls)
            attribute = PropertyAttribute(self, cls, name,
                self._variable_class, self._variable_kwargs)
            cls._attributes[self] = attribute

        return attribute

    def coerce(self, value):
        return self._variable_class(**self._variable_kwargs).coerce(value)


class PropertyAttribute(Attribute):

    def __init__(self, prop, cls, name, variable_class, variable_kwargs):
        super(PropertyAttribute, self).__init__(name, cls,
            VariableFactory(variable_class, attribute=self, **variable_kwargs))

        # Used by references.
        self.cls = cls

        # Copy attributes from the property to avoid one additional
        # function call on each access.
        for attr in ["__get__", "__set__"]:
            setattr(self, attr, getattr(prop, attr))


class PropertyType(Property):

    def __init__(self, **kwargs):
        kwargs["value"] = kwargs.pop("default", None)
        kwargs["value_factory"] = kwargs.pop("default_factory", None)
        super(PropertyType, self).__init__(self.variable_class, kwargs)


class PropertyFactory(PropertyType):

    def __init__(self, type=None, **kwargs):
        if "default" in kwargs:
            raise ValueError("'default' not allowed for factories. "
                             "Use 'default_factory' instead.")
        if type is None:
            type = Property()
        kwargs["item_factory"] = VariableFactory(type._variable_class,
            **type._variable_kwargs)
        super(PropertyFactory, self).__init__(**kwargs)


class String(PropertyType):

    variable_class = StringVariable


class Unicode(PropertyType):

    variable_class = UnicodeVariable


class List(PropertyFactory):

    variable_class = ListVariable

    def __init__(self, *args, **kwargs):
        kwargs["separator"] = kwargs.pop("separator", r"\s")
        super(List, self).__init__(*args, **kwargs)
