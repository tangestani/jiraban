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
    "Item",
    "Board",
    ]

from jiraban.properties import (
    List,
    String,
    Unicode,
    )


# Item status states.
CLOSED = "Closed"
IN_PROGRESS = "In Progress"
OPEN = "Open"
READY_FOR_QA = "Ready for QA"
READY_FOR_SPRINT = "Ready for sprint"
REOPENED = "Reopened"
RESOLVED = "Resolved"
STATUS_ORDER = [
    IN_PROGRESS,
    READY_FOR_QA,
    READY_FOR_SPRINT,
    RESOLVED,
    REOPENED,
    OPEN,
    CLOSED,
    ]

# Item priority states.
BLOCKER = "Blocker"
CRITICAL = "Critical"
MAJOR = "Major"
MINOR = "Minor"
TRIVIAL = "Trivial"
PRIORITY_ORDER = [
    BLOCKER,
    CRITICAL,
    MAJOR,
    MINOR,
    TRIVIAL,
    ]


class Item:
    """An item represents a work item."""

    id = String(required=True)
    link = String(required=True)
    priority = String(required=True)
    status = String(required=True)
    summary = Unicode(required=True)
    assignee = Unicode()
    username = String()
    components = List()
    fix_versions = List()

    def __init__(self, id, link, priority, status, summary,
            assignee=None, username=None, components=None, fix_versions=None):
        self.id = id
        self.link = link
        self.priority = priority
        self.status = status
        self.summary = summary
        self.assignee = assignee
        self.username = username
        self.components = components if components else []
        self.fix_versions = fix_versions if fix_versions else []

    def __cmp__(self, other):
        """Compare two L{Item}s.

        Items with a higher priority are sorted first. Items with the same
        priority are ordered by item number.
        """
        priority_cmp = cmp(
            PRIORITY_ORDER.index(self.priority),
            PRIORITY_ORDER.index(other.priority))
        if priority_cmp:
            return priority_cmp

        status_cmp = cmp(
            STATUS_ORDER.index(self.status),
            STATUS_ORDER.index(other.status))
        if status_cmp:
            return status_cmp

        return cmp(self.id, other.id)


class ItemCollection:
    """A named collecton of L{Item}s organized into categories.

    @param name: Name of the L{Item} collection.
    """
    def __init__(self, name):
        self.name = name
        self._items = []

    def __cmp__(self, other):
        """Compare two groups.

        Groups are sorted alphabetically. The default group is always
        sorted last.
        """
        if self.name is None:
            return 1
        if other.name is None:
            return -1
        return cmp(self.name, other.name)

    def __iter__(self):
        return iter(sorted(self._items))

    def __len__(self):
        return len(self._items)

    def add(self, item):
        """Add C{item} to this collection."""
        self._items.append(item)


class GroupCollection:
    """A grouped collection of L{Item}s.

    @param factory: Function to create a collection.
    @param attribute: L{Item} attribute to group by.
    """
    def __init__(self, factory, attribute):
        self._factory = factory
        self._attribute = attribute
        self._groups = {}

    def __iter__(self):
        return iter(sorted(self._groups.values()))

    def __len__(self):
        return len(self._groups)

    def add(self, item):
        """Add C{item} to this group."""
        for group in self._get_groups(item):
            group.add(item)

    def get(self, name):
        """Get an L{ItemCollection} by C{name}."""
        return self._groups.get(name, ItemCollection(name))

    def _get_groups(self, item):
        """Get the L{Story}s that C{item} is associated with."""
        names = getattr(item, self._attribute)
        if names:
            if not isinstance(names, list):
                names = [names]
            for name in names:
                group = self._groups.get(name)
                if group:
                    yield group
                else:
                    group = self._factory(name)
                    self._groups[name] = group
                    yield group
        else:
            if None not in self._groups:
                self._groups[None] = self._factory(None)
            yield self._groups[None]


class Category(ItemCollection):
    """A category is a collection of L{Item}s related to a version.

    @param name: Name of this category.
    """


class Identity(ItemCollection):
    """An identity is a collection of L{Item}s related to an assignee.

    @param name: Name of this identity.
    """


class Story(ItemCollection):
    """A story is a collection of L{Item}s related to a component.

    @param name: Name of this story.
    """
    def __init__(self, name, category_attribute="fix_versions"):
        super(Story, self).__init__(name)
        self.categories = GroupCollection(Category, category_attribute)

    def add(self, item):
        super(Story, self).add(item)
        self.categories.add(item)


class Board(Story):
    """A board contains a collection of L{Item}s grouped into L{Story}s.

    @param name: Name of this board.
    @param link: Optional link to this board.
    """
    def __init__(
            self, name, link=None,
            category_attribute="fix_versions",
            story_attribute="components",
            identity_attribute="assignee"):
        super(Board, self).__init__(name, category_attribute)

        factory = lambda n: Story(n, category_attribute)
        self.stories = GroupCollection(factory, story_attribute)
        self.identities = GroupCollection(Identity, identity_attribute)
        self.link = link

    def add(self, item):
        super(Board, self).add(item)
        self.stories.add(item)
        self.identities.add(item)
