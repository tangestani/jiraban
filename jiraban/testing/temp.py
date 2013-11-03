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
    "TempMixin",
    ]

import os

from shutil import rmtree
from tempfile import (
    mkdtemp,
    mkstemp,
    )


class TempMixin:

    def setUp(self):
        """Keep a list of temporary directories, files and links."""
        super(TempMixin, self).setUp()

        self._temppaths = []

    def tearDown(self):
        """Remove all the temporary directories, files and links."""
        super(TempMixin, self).tearDown()

        for path in self._temppaths:
            self.remove_path(path)

    def make_directory(
        self, prefix="tmp", suffix="", basename=None, dirname=None,
        path=None, mode=None):
        """Create a temporary directory and return the path to it.

        The directory is removed after the test runs.
        """
        if path is not None:
            os.mkdir(path)
            self._temppaths.append(path)
        elif basename is not None:
            if dirname is None:
                dirname = mkdtemp()
                self._temppaths.append(dirname)
            path = os.path.join(dirname, basename)
            os.mkdir(path)
        else:
            path = mkdtemp(suffix, prefix, dirname)
            self._temppaths.append(path)

        if mode is not None:
            os.chmod(path, mode)

        return path

    def make_file(
        self, prefix="tmp", suffix="", basename=None, dirname=None,
        path=None, mode=None, content=None):
        """Create a temporary file and return the path to it.

        The file is removed after the test runs.
        """
        if path is not None:
            self._temppaths.append(path)
        elif basename is not None:
            if dirname is None:
                dirname = mkdtemp()
                self._temppaths.append(dirname)
            path = os.path.join(dirname, basename)
        else:
            fd, path = mkstemp(suffix, prefix, dirname)
            self._temppaths.append(path)
            os.close(fd)
            if content is None:
                os.unlink(path)

        if content is not None:
            file = open(path, "w")
            try:
                file.write(content)
            finally:
                file.close()
            if mode is not None:
                os.chmod(path, mode)

        return path

    def make_link(
        self, src, prefix="tmp", suffix="", basename=None, dirname=None,
        path=None, mode=None):
        """Create a temporary link with the source and return the path
        to the destination.

        The link is removed after the test runs.
        """
        dst = self.make_file(prefix, suffix, basename, dirname, path, mode)
        os.symlink(src, dst)

        return dst

    def remove_path(self, path):
        """Remove a temporary path; called on tear down."""
        if os.path.isdir(path):
            rmtree(path, ignore_errors=True)
        elif os.path.isfile(path):
            os.unlink(path)
        elif os.path.islink(path):
            os.unlink(path)
