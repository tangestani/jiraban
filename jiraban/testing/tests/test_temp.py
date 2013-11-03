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

__all__ = []

import os

from stat import S_IMODE
from unittest import TestCase

from jiraban.testing.temp import TempMixin
from jiraban.testing.unique import UniqueMixin


class TestTempMixin(TempMixin, UniqueMixin, TestCase):

    def test_make_directory_with_prefix(self):
        """
        When making a directory with a prefix, the basename should start
        with that prefix.
        """
        prefix = self.get_unique_string()
        path = self.make_directory(prefix=prefix)
        basename = os.path.basename(path)
        self.assertTrue(basename.startswith(prefix))

    def test_make_directory_with_suffix(self):
        """
        When making a directory with a suffix, the basename should start
        with that suffix.
        """
        suffix = self.get_unique_string()
        path = self.make_directory(suffix=suffix)
        basename = os.path.basename(path)
        self.assertTrue(basename.endswith(suffix))

    def test_make_directory_with_basename(self):
        """
        When making a directory with a basename, the basename of the path
        should be the same.
        """
        basename = self.get_unique_string()
        path = self.make_directory(basename=basename)
        self.assertEqual(os.path.basename(path), basename)

    def test_make_directory_with_dirname(self):
        """
        When making a directory with a dirname, the dirname of the path
        should be the same.
        """
        dirname = self.make_directory()
        path = self.make_directory(dirname=dirname)
        self.assertEqual(os.path.dirname(path), dirname)

    def test_make_directory_with_path(self):
        """
        When making a directory with a path, the returned path should
        be the same.
        """
        dirname = self.make_directory()
        basename = self.get_unique_string()
        path = os.path.join(dirname, basename)
        self.assertEqual(self.make_directory(path=path), path)

    def test_make_directory_with_mode(self):
        """
        When making a directory with a mode, the returned path should
        have that mode.
        """
        mode = 0
        path = self.make_directory(mode=mode)
        self.assertEqual(S_IMODE(os.stat(path).st_mode), mode)

    def test_make_directory_exists(self):
        """
        When making a directory, it should always be created.
        """
        path = self.make_directory()
        self.assertTrue(os.path.exists(path))

    def test_make_file_with_prefix(self):
        """
        When making a file with a prefix, the basename should start with
        that prefix.
        """
        prefix = self.get_unique_string()
        path = self.make_file(prefix=prefix)
        basename = os.path.basename(path)
        self.assertTrue(basename.startswith(prefix))

    def test_make_file_with_suffix(self):
        """
        When making a file with a suffix, the basename should start with
        that suffix.
        """
        suffix = self.get_unique_string()
        path = self.make_file(suffix=suffix)
        basename = os.path.basename(path)
        self.assertTrue(basename.endswith(suffix))

    def test_make_file_with_basename(self):
        """
        When making a file with a basename, the basename of the path
        should be the same.
        """
        basename = self.get_unique_string()
        path = self.make_file(basename=basename)
        self.assertEqual(os.path.basename(path), basename)

    def test_make_file_with_dirname(self):
        """
        When making a file with a dirname, the dirname of the path
        should be the same.
        """
        dirname = self.make_directory()
        path = self.make_file(dirname=dirname)
        self.assertEqual(os.path.dirname(path), dirname)

    def test_make_file_with_path(self):
        """
        When making a file with a path, the returned path should be
        the same.
        """
        dirname = self.make_directory()
        basename = self.get_unique_string()
        path = os.path.join(dirname, basename)
        self.assertEqual(self.make_file(path=path), path)

    def test_make_file_with_mode(self):
        """
        When making a file with a mode, the returned path should
        have that mode.
        """
        mode = 0
        path = self.make_file(mode=mode, content="")
        self.assertEqual(S_IMODE(os.stat(path).st_mode), mode)

    def test_make_file_with_content(self):
        """
        When making a file with content, it should be created with the
        same content.
        """
        content = self.get_unique_string()
        path = self.make_file(content=content)
        self.assertTrue(os.path.exists(path))
        self.assertEqual(open(path).read(), content)

    def test_make_file_without_content(self):
        """
        When making a file without contnet, it should not actually
        be created.
        """
        path = self.make_file(content=None)
        self.assertFalse(os.path.exists(path))

    def test_make_link(self):
        """
        When making a link with just a source, it should return the
        path to the link destination.
        """
        src = self.make_file(content="")
        dst = self.make_link(src)
        self.assertTrue(os.path.islink(dst))

    def test_remove_path_file(self):
        """
        When removing a file that exists, it should be unlinked.
        """
        path = self.make_file(content="")
        self.assertTrue(os.path.isfile(path))
        self.remove_path(path)
        self.assertFalse(os.path.isfile(path))

    def test_remove_path_directory(self):
        """
        When removing a directory that exists, it should be removed.
        """
        path = self.make_directory()
        self.assertTrue(os.path.isdir(path))
        self.remove_path(path)
        self.assertFalse(os.path.isdir(path))

    def test_remove_path_not_exists(self):
        """
        When removing a path that doesn't exist, nothing should happen.
        """
        path = self.make_file(content=None)
        self.remove_path(path)
