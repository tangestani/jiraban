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
    "Application",
    "ApplicationError",
    ]

import sys

from optparse import (
    OptionParser,
    OptionValueError,
    )


class ApplicationError(Exception):
    """Error raised when application fails."""

    status = 1


class Application:

    # Application defaults
    usage = "Usage: %prog [OPTIONS]"

    def __init__(self, name=None):
        """Construct new Application.

        @param name: A short name for the application.
        """
        if name is None:
            self._name = self.__class__.__name__.lower()
        else:
            self._name = name

    @property
    def name(self):
        """Enable subclasses to override with command-line arguments."""
        return self._name

    def add_options(self, parser):
        """Add options and option groups to the parser."""

    def parse_options(self, options, args):
        """Parse the options as returned by the parser."""

    def process(self):
        """Process the application here. Must be defined."""
        raise NotImplementedError()

    def pre_process(self):
        """
        This should set up any state necessary before loading and
        processing the Application.
        """

    def post_process(self, error):
        """This will be called after the processing has finished."""

    def run(self, args=None):
        """Run the application.

        @param args: List of command-line arguments.
        """
        parser = OptionParser(usage=self.usage)
        self.add_options(parser)
        options, args = parser.parse_args(args)
        try:
            self.parse_options(options, args)
        except OptionValueError as error:
            parser.error(error)

        error = None
        self.pre_process()
        try:
            self.process()
        except ApplicationError as application_error:
            error = application_error
            print >>sys.stderr, error
            sys.exit(error.status)
        finally:
            self.post_process(error)
