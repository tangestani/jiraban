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

import sys

from cStringIO import StringIO
from optparse import OptionValueError
from unittest import TestCase

from jiraban.testing.unique import UniqueMixin
from jiraban.scripts.application import (
    Application,
    ApplicationError,
    )


class StubApplication(Application):

    usage = None
    option_parsed = None
    process_called = False
    pre_process_called = False
    post_process_called = False

    def add_options(self, parser):
        """See L{Application}."""
        super(StubApplication, self).add_options(parser)

        parser.add_option("-f", "--foo",
            action="store_true",
            default=False,
            help="Foo option.")

    def parse_options(self, options, args):
        """See L{Application}."""
        super(StubApplication, self).parse_options(options, args)

        self.option_parsed = options.foo

    def pre_process(self):
        """See L{Application}."""
        self.pre_process_called = True

    def post_process(self, error):
        """See L{Application}."""
        self.post_process_called = True

    def process(self):
        """See L{Application}."""
        self.process_called = True


class TestApplication(UniqueMixin, TestCase):

    def setUp(self):
        """Overwrite standard error with a memory buffer."""
        super(TestApplication, self).setUp()
        self.original_stderr = sys.stderr
        sys.stderr = StringIO()

    def tearDown(self):
        """Recover the original standard error."""
        super(TestApplication, self).tearDown()
        sys.stderr = self.original_stderr

    def test_process(self):
        """
        When calling the process method on the Application class, a
        NotImplementedError exception should be raised.
        """
        application = Application()
        self.assertRaises(NotImplementedError, application.process)

    def test_instantiate_with_name(self):
        """
        When instantiating an Application with a name, it should use
        that name.
        """
        name = self.get_unique_string()
        application = Application(name)
        self.assertEqual(application.name, name)

    def test_instantiate_without_name(self):
        """
        When instantiating an Application without a name, a default name
        should be defined based on the class name.
        """
        application = Application()
        self.assertEqual(application.name, "application")

    def test_pass_invalid_option(self):
        """
        When passing an invalid option, a SystemExit exception should be
        raised.
        """
        application = Application()
        self.assertRaises(SystemExit, application.run, ["--foo"])

    def test_pass_custom_option(self):
        """
        When subclassing an Application, it should be possible to add
        custom options.
        """
        application = StubApplication()
        application.run(["--foo"])

    def test_parse_options(self):
        """
        When subclassing an Application, it should be possible to parse
        custom options.
        """
        application = StubApplication()
        self.assertIs(application.option_parsed, None)

        application.run([])
        self.assertFalse(application.option_parsed)

        application.run(["--foo"])
        self.assertTrue(application.option_parsed)

    def test_parse_options_with_an_option_value_error(self):
        """
        When subclassing an Application, parsing custom options should
        handle the OptionValueError exception.
        """
        class StubApplication(Application):

            def parse_options(self, options, args):
                raise OptionValueError("Stub error")

        application = StubApplication()
        self.assertRaises(SystemExit, application.run)

    def test_run_with_pre_process(self):
        """
        When running an application, the pre_process method should
        be called.
        """
        application = StubApplication()
        self.assertFalse(application.pre_process_called)

        application.run([])
        self.assertTrue(application.pre_process_called)

    def test_run_with_post_process(self):
        """
        When running an application, the post_process method should
        be called.
        """
        application = StubApplication()
        self.assertFalse(application.post_process_called)

        application.run([])
        self.assertTrue(application.post_process_called)

    def test_run_with_process(self):
        """
        When running an application, the process method should be called.
        """
        application = StubApplication()
        self.assertFalse(application.process_called)

        application.run([])
        self.assertTrue(application.process_called)

    def test_run_with_an_application_error(self):
        """
        When running an application, the run method should handle the
        ApplicationError exception.
        """
        def process():
            raise ApplicationError

        application = StubApplication()
        application.process = process
        self.assertRaises(SystemExit, application.run)
