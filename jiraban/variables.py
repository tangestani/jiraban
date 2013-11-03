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
    "ListVariable",
    "StringVariable",
    "UnicodeVariable",
    "Variable",
    "VariableFactory",
    "get_variable",
    ]

from functools import partial as VariableFactory


class Variable:

    _value = None
    _required = True

    attribute = None

    def __init__(
            self, attribute=None, value=None, value_factory=None,
            required=False):
        self.attribute = attribute
        self._required = required
        if value is not None:
            self.set(value)
        if value_factory is not None:
            self.set(value_factory())

    def get(self):
        if self._value is None and self._required is True:
            raise_none_error(self.attribute)

        return self._value

    def set(self, value):
        if value is None:
            if self._required is True:
                raise_none_error(self.attribute)

            new_value = None
        else:
            new_value = self.coerce(value)

        self._value = new_value

    def coerce(self, value):
        return value


class StringVariable(Variable):

    def coerce(self, value):
        if isinstance(value, unicode):
            value = str(value)
        elif not isinstance(value, str):
            raise ValueError("%r is not a str" % (value,))

        return value


class UnicodeVariable(Variable):

    def coerce(self, value):
        if isinstance(value, str):
            value = unicode(value, encoding="utf-8")
        elif not isinstance(value, unicode):
            raise ValueError("%r is not a unicode" % (value,))

        return value


class ListVariable(Variable):

    def __init__(self, item_factory, separator, *args, **kwargs):
        self._item_factory = item_factory
        self._separator = separator
        super(ListVariable, self).__init__(*args, **kwargs)

    def coerce(self, values):
        item_factory = self._item_factory
        if isinstance(values, str):
            values = values.split(self._separator) if values else []
        elif not isinstance(values, (list, tuple)):
            raise ValueError("%r is not a list or tuple" % (values,))

        for i, v in enumerate(values):
            values[i] = item_factory(value=v).get()

        return values


def get_variable(obj, attribute):
    return get_variables(obj)[attribute]


def get_variables(obj):
    from jiraban.attribute import get_attributes

    if "__variables__" in obj.__dict__:
        return obj.__dict__["__variables__"]
    else:
        variables = {}
        cls = type(obj)
        for attribute in get_attributes(cls).values():
            variable = attribute.variable_factory(attribute=attribute)
            variables[attribute] = variable

        return obj.__dict__.setdefault("__variables__", variables)


def raise_none_error(attribute):
    if not attribute:
        raise ValueError("None isn't acceptable as a value")
    else:
        name = attribute.name
        raise ValueError("None isn't acceptable as a value for %s" % name)
