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
    IN_PROGRESS,
    MAJOR,
    OPEN,
    READY_FOR_QA,
    READY_FOR_SPRINT,
    Board,
    )
from jiraban.html import (
    priority_style,
    sprite_url,
    status_style,
    generate_html,
    )
from jiraban.tests.test_jira import JIRAMixin

from unittest import TestCase


class TestPriorityStyle(TestCase):

    def test_major(self):
        """
        The L{priority_style} filter takes a string representation of a
        priority and generates a CSS class name for it.
        """
        self.assertEqual(priority_style(MAJOR), "priority-major")


class TestStatusStyle(TestCase):

    def test_open(self):
        """
        The L{status_style} filter takes a string representation of a
        status and generates a CSS class name for it.
        """
        self.assertEqual(status_style(OPEN), "status-open")

    def test_in_progress(self):
        """
        The status for READY_FOR_QA and READY_FOR_SPRINT are all treated
        as IN_PROGRESS.
        """
        for status in IN_PROGRESS, READY_FOR_QA, READY_FOR_SPRINT:
            self.assertEqual(status_style(status), "status-inprogress")


class TestSpriteUrl(JIRAMixin, TestCase):

    def test_empty(self):
        """
        An empty sprite returns an empty data string.
        """
        jira = self.create_jira()
        self.assertEqual(
            sprite_url("test.gif", jira), "data:image/gif;base64,")


class TestGenerateHTML(JIRAMixin, TestCase):

    def test_empty_board(self):
        jira = self.create_jira()
        board = Board("test")
        html = generate_html(board, jira)
        self.assertTrue("<title>test</title>" in html)
