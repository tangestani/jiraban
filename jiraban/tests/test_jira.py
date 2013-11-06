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

from jiraban.jira import (
    JIRA,
    JIRAError,
    JIRALink,
    )
from jiraban.testing.unique import UniqueMixin

from cStringIO import StringIO
from requests.models import Response
from unittest import TestCase


def fake_session_factory(content, status_code):
    def fake_session():
        return FakeSession(content, status_code)

    return fake_session


class FakeSession:

    def __init__(self, content="", status_code=200):
        self.content = content
        self.status_code = status_code

    def get(self, url):
        response = Response()
        response.raw = StringIO(self.content)
        response.status_code = self.status_code
        return response


class JIRAMixin:

    def create_jira(
            self, server="http://localhost", username="user", password="pass",
            verify=True, session_content="", session_status_code=200):
        """Create a L{JIRA} with sensible default values."""
        session_factory = fake_session_factory(
            session_content, session_status_code)
        return JIRA(server, username, password, verify, session_factory)


class TestJIRALink(JIRAMixin, UniqueMixin, TestCase):

    def test_url(self):
        """
        A link contains a url.
        """
        url = self.get_unique_url()
        link = JIRALink(None, url)
        self.assertEqual(link.url, url)

    def test_read(self):
        """
        A link reads the contents of a url.
        """
        string = self.get_unique_string()
        session = FakeSession(string)
        link = JIRALink(session, self.get_unique_url())
        self.assertEqual(link.read(), string)

    def test_read_error(self):
        """
        A link that doesn't return 200 raises an exception.
        """
        session = FakeSession(status_code=404)
        link = JIRALink(session, self.get_unique_url())
        self.assertRaises(JIRAError, link.read)


class TestJIRA(JIRAMixin, UniqueMixin, TestCase):

    def test_icon_url(self):
        """
        Icons are located under /images/icons.
        """
        jira = self.create_jira()
        icon = jira.get_icon("foo")
        self.assertEqual(icon.url, "http://localhost/images/icons/foo.gif")

    def test_xml_query(self):
        """
        XML queries contains jqlQuery in the query string.
        """
        jira = self.create_jira()
        string = self.get_unique_string()
        xml_link = jira.query_xml(string)
        self.assertTrue(("jqlQuery=%s" % string) in xml_link.url)
        self.assertTrue("tempMax=1000" in xml_link.url)

    def test_xml_temp_max(self):
        """
        XML queries can specify a tempMax in the query string.
        """
        jira = self.create_jira()
        temp_max = self.get_unique_integer()
        xml_link = jira.query_xml("", temp_max)
        self.assertTrue(("tempMax=%s" % temp_max) in xml_link.url)

    def test_html_query(self):
        """
        HTML queries contains jqlQuery in the query string.
        """
        jira = self.create_jira()
        string = self.get_unique_string()
        html_link = jira.query_html(string)
        self.assertTrue(("jqlQuery=%s" % string) in html_link.url)
        self.assertTrue("runQuery=True" in html_link.url)
        self.assertTrue("clear=True" in html_link.url)

    def test_html_run_query_and_clear(self):
        """
        HTML queries can specify a runQuery and clear in the query string.
        """
        jira = self.create_jira()
        html_link = jira.query_html("", False, False)
        self.assertTrue("runQuery=False" in html_link.url)
        self.assertTrue("clear=False" in html_link.url)
