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
    "JIRA",
    "JIRAError",
    "kwargs_to_jql",
    ]

import os

from requests import (
    HTTPError,
    Session,
    )
from urllib import urlencode
from urlparse import (
    urlparse,
    urlunparse,
    )

try:
    import xml.etree.cElementTree as etree
except ImportError:
    import cElementTree as etree

from jiraban.board import Item


class JIRAError(Exception):
    """Error raised when on JIRA failure."""
    pass


class JIRALink:

    def __init__(self, session, url):
        self._session = session
        self.url = url

    def read(self):
        response = self._session.get(self.url)
        try:
            response.raise_for_status()
        except HTTPError, e:
            raise JIRAError("Failed to get %s: %s" % (self.url, e))

        return response.raw.read()


class JIRA:

    def __init__(
            self, server, username=None, password=None, verify=True,
            session_factory=Session):
        # Rip off trailing slash since all urls depend on that.
        self.server = server.rstrip("/")

        self._session = session_factory()
        self._session.verify = verify
        self._session.auth = (username, password)

    def get_link(self, path, query=""):
        base_url = urlparse(self.server)
        qs = urlencode(query)
        url = urlunparse(
            (base_url.scheme, base_url.netloc, path, None, qs, None))
        return JIRALink(self._session, url)

    def get_icon(self, icon):
        return self.get_link("/images/icons/%s.gif" % icon)

    def query_xml(self, jql, temp_max=1000):
        return self.get_link(
            "/sr/jira.issueviews:searchrequest-xml/temp/SearchRequest.xml", {
                "jqlQuery": jql,
                "tempMax": temp_max,
                })

    def query_html(self, jql, run_query=True, clear=True):
        return self.get_link("/secure/IssueNavigator!executeAdvanced.jspa", {
            "jqlQuery": jql,
            "runQuery": run_query,
            "clear": clear,
            })

    def iter_items(self, jql, cache=None):
        xml_link = self.query_xml(jql)

        if cache and os.path.exists(cache):
            with open(cache) as f:
                content = f.read()
        else:
            content = xml_link.read()
            if cache:
                with open(cache, "w") as f:
                    f.write(content)

        try:
            root = etree.fromstring(content)
        except etree.ParseError, e:
            raise JIRAError(e)

        for element in root.findall(".//item"):
            yield self._create_item(element)

    def _create_item(self, element):
        return Item(
            element.find("key").text,
            element.find("link").text,
            element.find("priority").text,
            element.find("status").text,
            element.find("project").text,
            element.find("summary").text,
            element.find("assignee").text,
            element.find("assignee").get("username"),
            components=[c.text for c in element.findall("component")],
            fix_versions=[c.text for c in element.findall("fixVersion")])


def jql_quote(string):
    """Quote a string if it contains reserved characters."""
    reserved_characters = set(" +.,;?|*/%^$#@[]")
    if any((character in reserved_characters) for character in string):
        return "'%s'" % string

    return string


def kwargs_to_jql(**kwargs):
    """Convert keyword arguments into a JQL string.

    Key/value pairs are ANDed whereas value lists are ORed.
    """
    parts = []
    for key, value in kwargs.iteritems():
        if isinstance(value, str):
            value = [value]

        if len(value) == 1:
            parts.append(" = ".join((key, jql_quote(value[0]),)))
        elif len(value) > 1:
            subparts = (" = ".join((key, jql_quote(subvalue),))
                for subvalue in value)
            parts.append("(%s)" % " OR ".join(subparts))

    return " AND ".join(parts)
