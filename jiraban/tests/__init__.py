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
    "find_tests",
    ]

import os

import unittest


def find_tests(testpaths=()):
    """Find all test paths, or test paths contained in the provided sequence.

    @param testpaths: If provided, only tests in the given sequence will
           be considered.  If not provided, all tests are considered.
    """
    suite = unittest.TestSuite()
    testpaths = set(testpaths)
    testdir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    topdir = os.path.abspath(os.path.join(testdir, os.pardir))
    for root, dirnames, filenames in os.walk(testdir):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            relpath = filepath[len(topdir) + 1:]

            if (filename == "__init__.py" or
                filename.endswith(".pyc") or
                not filename.startswith("test_")):
                # Skip non-tests.
                continue

            if testpaths:
                # Skip any tests not in testpaths.
                for testpath in testpaths:
                    if relpath.startswith(testpath):
                        break
                else:
                    continue

            if filename.endswith(".py"):
                modpath = relpath.replace(os.path.sep, ".")[:-3]
                module = __import__(modpath, None, None, [""])
                suite.addTest(
                    unittest.defaultTestLoader.loadTestsFromModule(module))

    return suite
