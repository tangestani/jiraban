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
    "run",
    ]

import os
import sys

from getpass import getpass
from optparse import (
    OptionGroup,
    OptionValueError,
    )

from jiraban.attribute import get_attributes
from jiraban.board import (
    Board,
    Item,
    )
from jiraban.html import generate_html
from jiraban.jira import (
    JIRA,
    JIRAError,
    kwargs_to_jql,
    )

from jiraban.scripts.application import (
    Application,
    ApplicationError,
    )
from jiraban.scripts.options import AttributeOption


class RunnerApplication(Application):

    # Application defaults
    usage = """\
Usage: %%prog [OPTIONS] USERNAME [PASSWORD]
Warning, JIRA might limit the number of requests within a period of time.

Attributes:
  %s\
""" % "\n  ".join(sorted(get_attributes(Item).keys()))

    # Runner defaults
    default_media = os.path.abspath(os.path.join(__file__, '../../../media'))
    default_output = "-"
    default_server = "http://localhost:8080"

    # Display defaults
    default_category = "fix_versions"
    default_identity = "assignee"
    default_story = "components"

    def add_options(self, parser):
        """See L{Application}."""
        super(RunnerApplication, self).add_options(parser)

        runner_group = OptionGroup(parser, "Runner options")
        runner_group.add_option("--cache",
            metavar="FILE",
            help=("""Cache to use instead of a request on the server."""))
        runner_group.add_option("-m", "--media",
            metavar="DIR",
            default=self.default_media,
            help=("""Media directory, defaults to "%default"."""))
        runner_group.add_option("-o", "--output",
            metavar="FILE",
            default=self.default_output,
            help=("""Output file, defaults to "%default"."""))
        runner_group.add_option("-s", "--server",
            metavar="URL",
            default=self.default_server,
            help=("""JIRA server, defaults to "%default"."""))

        filter_group = OptionGroup(parser, "Filter options")
        filter_group.add_option("-a", "--assignee",
            metavar="NAME",
            action="append",
            type="string",
            default=[],
            help=("""Assignees to filter, defaults to the current user """
                """without other filters. More than one can be specified."""))
        filter_group.add_option("-c", "--component",
            metavar="NAME",
            action="append",
            type="string",
            default=[],
            help=("""Components to filter. """
                """More than one can be specified."""))
        filter_group.add_option("-j", "--jql",
            metavar="QUERY",
            help=("""JIRA query language. """
                """Cannot be specified with assignee or component."""))

        display_group = OptionGroup(parser, "Display options")
        display_group.option_class = AttributeOption
        display_group.add_option("--category",
            metavar="ATTR",
            type="attribute",
            default=self.default_category,
            help=("""Category attribute to group items horizontally, """
                """defaults to "%default"."""))
        display_group.add_option("--identity",
            metavar="ATTR",
            type="attribute",
            default=self.default_identity,
            help=("""Identity attribute to group items by color, """
                """defaults to "%default"."""))
        display_group.add_option("--story",
            metavar="ATTR",
            type="attribute",
            default=self.default_story,
            help=("""Story attribute to group items vertically, """
                """defaults to "%default"."""))

        parser.add_option_group(runner_group)
        parser.add_option_group(filter_group)
        parser.add_option_group(display_group)

    def parse_options(self, options, args):
        """See L{Application}."""
        super(RunnerApplication, self).parse_options(options, args)

        if len(args) < 1:
            raise OptionValueError("Missing USERNAME.")
        if len(args) > 2:
            raise OptionValueError("Too many arguments.")

        username = args[0]
        password = args[1] if len(args) > 1 else getpass("Password: ")

        if options.jql:
            if options.assignee or options.component:
                raise OptionValueError(
                    "Cannot use JQL with assignee or component")
            self.jql = options.jql
        else:
            if not options.assignee and not options.component:
                assignee = "currentUser()"
            else:
                assignee = options.assignee

            self.jql = kwargs_to_jql(
                resolution="unresolved",
                assignee=assignee,
                component=options.component)

        self.jira = JIRA(username, password, server=options.server)
        self.board = Board(
            self.jql, self.jira.get_html_url(self.jql),
            options.category, options.story, options.identity)
        self.cache = options.cache
        self.media = options.media
        self.output = options.output

    def process(self):
        """See L{Application}."""
        try:
            for item in self.jira.get_items(self.jql, self.cache):
                self.board.add(item)
        except JIRAError, e:
            raise ApplicationError(e)

        html = generate_html(self.board, self.media)

        if self.output != "-":
            output_file = open(self.output, "w")
        else:
            output_file = sys.stdout
        try:
            print >>output_file, html.encode('utf-8')
        finally:
            if self.output != "-":
                output_file.close()


def run():
    application = RunnerApplication()
    application.run()
