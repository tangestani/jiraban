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
    "AttributeOption",
    "check_attribute",
    ]

from copy import copy
from optparse import (
    Option,
    OptionValueError,
    )

from jiraban.attribute import get_attributes
from jiraban.board import Item


def check_attribute(option, opt, value):
    """Check that the given value is a valid attribute."""
    if value not in get_attributes(Item):
        raise OptionValueError(
            "option %s: invalid value: %r, not found in available attributes."
            % (opt, value))

    return value


class AttributeOption(Option):
    TYPES = Option.TYPES + ("attribute",)
    TYPE_CHECKER = copy(Option.TYPE_CHECKER)
    TYPE_CHECKER["attribute"] = check_attribute
