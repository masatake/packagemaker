#
# Copyright (C) 2011 Satoru SATOH <satoru.satoh @ gmail.com>
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
import pmaker.backend.utils as U
import unittest


class Test_00_to_srcdir(unittest.TestCase):

    def test_to_srcdir(self):
        srcdir = "/tmp/w/src"

        self.assertEquals(U.to_srcdir(srcdir, "/a/b/c"), "/tmp/w/src/a/b/c")
        self.assertEquals(U.to_srcdir(srcdir, "a/b"),    "/tmp/w/src/a/b")
        self.assertEquals(U.to_srcdir(srcdir, "/"),      "/tmp/w/src/")


# vim:sw=4 ts=4 et:
