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

from jiraban.board import (
    BLOCKER,
    CLOSED,
    CRITICAL,
    IN_PROGRESS,
    MAJOR,
    MINOR,
    OPEN,
    READY_FOR_QA,
    READY_FOR_SPRINT,
    REOPENED,
    RESOLVED,
    TRIVIAL,
    Board,
    Category,
    GroupCollection,
    Identity,
    Item,
    ItemCollection,
    Story,
    )
from jiraban.testing.unique import UniqueMixin

from unittest import TestCase


class ItemMixin:

    def create_item(
            self, id="1", link="test link", priority=MAJOR, status=OPEN,
            project="test project", summary="test summary", **kwargs):
        """Create an L{Item} with sensible default values."""
        return Item(id, link, priority, status, project, summary, **kwargs)


class TestItem(ItemMixin, UniqueMixin, TestCase):

    def test_instantiate_with_default_values(self):
        """
        An ID, link, priority, status and summary must be provided when a
        L{Item} is instantiated. All other values default to C{None}.
        """
        project = self.get_unique_string()
        summary = self.get_unique_string()
        item = Item("1", "link", MAJOR, OPEN, project, summary)
        self.assertEqual(item.id, "1")
        self.assertEqual(item.priority, MAJOR)
        self.assertEqual(item.status, OPEN)
        self.assertEqual(item.project, project)
        self.assertEqual(item.summary, summary)
        self.assertEqual(item.assignee, None)
        self.assertEqual(item.components, [])
        self.assertEqual(item.fix_versions, [])

    def test_instantiate_with_other_values(self):
        """
        In addition to the required values an assignee, 'In progress' date
        and a list of tags can be provided when a L{Item} is instantiated.
        """
        assignee = self.get_unique_string()
        username = self.get_unique_string()
        component = self.get_unique_string()
        fix_version = self.get_unique_string()
        item = self.create_item(
            assignee=assignee, username=username,
            components=[component], fix_versions=[fix_version])

        self.assertEqual(item.assignee, assignee)
        self.assertEqual(item.username, username)
        self.assertEqual(item.components, [component])
        self.assertEqual(item.fix_versions, [fix_version])

    def test_sort_order_by_priority(self):
        """Higher priority items come first."""
        items = [
            self.create_item(priority=TRIVIAL),
            self.create_item(priority=MINOR),
            self.create_item(priority=MAJOR),
            self.create_item(priority=CRITICAL),
            self.create_item(priority=BLOCKER),
            ]
        self.assertEqual(list(reversed(items)), sorted(items))

    def test_sort_order_by_status(self):
        """After priority, higher status items come first."""
        items = [
            self.create_item(status=CLOSED),
            self.create_item(status=OPEN),
            self.create_item(status=REOPENED),
            self.create_item(status=RESOLVED),
            self.create_item(status=READY_FOR_SPRINT),
            self.create_item(status=READY_FOR_QA),
            self.create_item(status=IN_PROGRESS),
            ]
        self.assertEqual(list(reversed(items)), sorted(items))

    def test_sort_order_by_id(self):
        """After priority and status, item ids are sorted alphabetically."""
        items = [
            self.create_item(id="2"),
            self.create_item(id="1"),
            ]
        self.assertEqual(list(reversed(items)), sorted(items))


class ItemCollectionMixin(ItemMixin):

    def create_item_collection(self, name="test"):
        """Create an L{ItemCollection} with sensible default values."""
        return ItemCollection(name)

    def test_instantiate(self):
        """An item collection starts empty."""
        collection = self.create_item_collection()
        self.assertEqual(len(collection), 0)
        self.assertEqual(list(collection), [])

    def test_sort_order_by_name(self):
        """Item collections are sorted by name first."""
        collections = [
            self.create_item_collection(name="2"),
            self.create_item_collection(name="1"),
            ]
        self.assertEqual(list(reversed(collections)), sorted(collections))

    def test_sort_order_with_default(self):
        """After name, item collections are sorted with the None last."""
        collections = [
            self.create_item_collection(name=None),
            self.create_item_collection(name="1"),
            ]
        self.assertEqual(list(reversed(collections)), sorted(collections))

        collections = [
            self.create_item_collection(name="1"),
            self.create_item_collection(name=None),
            ]
        self.assertEqual(collections, sorted(collections))

    def test_add(self):
        """Adding items affect the length of the collection."""
        collection = self.create_item_collection()
        self.assertEqual(len(collection), 0)

        item = self.create_item()
        collection.add(item)
        self.assertEqual(len(collection), 1)
        self.assertEqual(list(collection), [item])


class TestGroupCollection(ItemMixin, TestCase):

    def test_instantiate(self):
        """A  group collection starts empty."""
        collection = GroupCollection(ItemCollection, "priority")
        self.assertEqual(len(collection), 0)

    def test_add_same_attribute(self):
        """Adding items with the same attribute are grouped together."""
        collection = GroupCollection(ItemCollection, "priority")
        collection.add(self.create_item(priority=MAJOR))
        collection.add(self.create_item(priority=MAJOR))
        self.assertEqual(len(collection), 1)

    def test_add_different_attributes(self):
        """Adding items with different attributes are grouped separately."""
        collection = GroupCollection(ItemCollection, "priority")
        collection.add(self.create_item(priority=MAJOR))
        collection.add(self.create_item(priority=MINOR))
        self.assertEqual(len(collection), 2)

    def test_get_default(self):
        """Getting any name results in an empty L{ItemCollection}."""
        group_collection = GroupCollection(ItemCollection, "priority")
        item_collection = group_collection.get("test")
        self.assertEqual(len(item_collection), 0)
        self.assertEqual(list(item_collection), [])

    def test_get(self):
        """Getting any name results in an empty L{ItemCollection}."""
        group_collection = GroupCollection(ItemCollection, "priority")
        item = self.create_item(priority=MAJOR)
        group_collection.add(item)
        item_collection = group_collection.get(MAJOR)
        self.assertEqual(len(item_collection), 1)
        self.assertEqual(list(item_collection), [item])


class TestCategory(ItemCollectionMixin, TestCase):

    def create_item_collection(self, name="test"):
        return Category(name)


class TestIdentity(ItemCollectionMixin, TestCase):

    def create_item_collection(self, name="test"):
        return Identity(name)


class TestStory(ItemCollectionMixin, TestCase):

    def create_item_collection(
            self, name="test", category_attribute="fix_versions"):
        return Story(name, category_attribute)

    def test_instantiate_categories(self):
        """The categories in a L{Story} also starts empty."""
        story = self.create_item_collection()
        self.assertEqual(len(story.categories), 0)
        self.assertEqual(list(story.categories), [])

    def add_to_categories(self):
        """Items added to a L{Story} are also grouped by categories."""
        story = self.create_item_collection(category_attribute="priority")
        story.add(self.create_item(priority=MAJOR))
        story.add(self.create_item(priority=MAJOR))
        self.assertEqual(len(story.categories), 1)


class TestBoard(TestStory, TestCase):

    def create_item_collection(
            self, name="test", link="link",
            category_attribute="fix_versions", story_attribute="components"):
        return Board(name, link, category_attribute, story_attribute)

    def test_instantiate_stories(self):
        """The stories in a L{Board} also starts empty."""
        board = self.create_item_collection()
        self.assertEqual(len(board.stories), 0)
        self.assertEqual(list(board.stories), [])

    def add_to_stories(self):
        """Items added to a L{Board} are also grouped by stories."""
        board = self.create_item_collection(story_attribute="status")
        board.add(self.create_item(status=OPEN))
        board.add(self.create_item(status=OPEN))
        self.assertEqual(len(board.stories), 1)
