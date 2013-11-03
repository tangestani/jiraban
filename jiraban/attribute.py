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
    "Attribute",
    "get_attributes",
    ]

from jiraban.variables import Variable


class Attribute:

    def __init__(self, name, cls, variable_factory=None):
        self.name = name
        self.cls = cls
        self.variable_factory = variable_factory or Variable


def get_attributes(cls):
    if "__attributes__" in cls.__dict__:
        return cls.__dict__["__attributes__"]
    else:
        attributes = {}
        for name in dir(cls):
            attribute = getattr(cls, name, None)
            if isinstance(attribute, Attribute):
                attributes[name] = attribute

        cls.__attributes__ = attributes
        return cls.__attributes__
