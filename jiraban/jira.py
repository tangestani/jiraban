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


class JIRA:

    DEFAULT_OPTIONS = {
        "server": "http://localhost:8080/jira",
        "verify": True,
    }

    def __init__(self, username=None, password=None, **options):
        session_factory = options.pop("session_factory", Session)
        self._options = self.DEFAULT_OPTIONS
        self._options.update(options)

        # Rip off trailing slash since all urls depend on that.
        if self._options["server"].endswith("/"):
            self._options["server"] = self._options["server"][:-1]

        self._session = session_factory()
        self._session.verify = self._options["verify"]
        self._session.auth = (username, password)

    def get_items(self, jql, cache=None):
        xml_url = self.get_xml_url(jql)

        if cache and os.path.exists(cache):
            with open(cache) as f:
                content = f.read()
        else:
            response = self._session.get(xml_url)
            try:
                response.raise_for_status()
            except HTTPError, e:
                raise JIRAError(e)

            content = response.content
            if cache:
                with open(cache, "w") as f:
                    f.write(content)

        try:
            root = etree.fromstring(content)
        except etree.ParseError, e:
            raise JIRAError(e)

        for element in root.findall(".//item"):
            yield self._create_item(element)

    def get_xml_url(self, jql):
        return self.get_url(
            "/sr/jira.issueviews:searchrequest-xml/temp/SearchRequest.xml", {
                "jqlQuery": jql,
                "tempMax": 1000,
                })

    def get_html_url(self, jql):
        return self.get_url("/secure/IssueNavigator!executeAdvanced.jspa", {
            "jqlQuery": jql,
            "runQuery": True,
            "clear": True,
            })

    def get_url(self, path, query):
        base_url = urlparse(self._options["server"])
        qs = urlencode(query)
        return urlunparse(
            (base_url.scheme, base_url.netloc, path, None, qs, None))

    def _create_item(self, element):
        return Item(
            element.find("key").text,
            element.find("link").text,
            element.find("priority").text,
            element.find("status").text,
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
