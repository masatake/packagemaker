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
from pmaker.globals import *
from pmaker.collectors.RpmModifiers import *
from pmaker.models.FileInfoFactory import *

import unittest
import os.path



NULL_DICT = dict()
FACTORY = FileInfoFactory()


class TestRpmAttributeModifier(unittest.TestCase):

    def setUp(self):
        self.modifier = RpmAttributeModifier()

    def test_update(self):
        fi = FACTORY.create("/bin/bash")
        new_fi = self.modifier.update(fi)

        self.assertTrue(getattr(new_fi, "rpm_attr", False))



class TestRpmConflictsModifier(unittest.TestCase):

    def test__init__conflicts(self):
        modifier = RpmConflictsModifier("bash")

        savedir = CONFLICTS_SAVEDIR % {"name": "bash"}
        newdir = CONFLICTS_NEWDIR % {"name": "bash"}

        self.assertEquals(modifier.savedir, savedir)
        self.assertEquals(modifier.newdir, newdir)

        owner = modifier.find_owner("/bin/bash")
        self.assertEquals(owner["name"], "bash")

    def test_update(self):

        savedir = CONFLICTS_SAVEDIR % {"name": "bash"}
        newdir = CONFLICTS_NEWDIR % {"name": "bash"}

        fi = FACTORY.create("/bin/bash")
        new_fi = modifier.update(fi)

        self.assertEquals(new_fi.original_path, fi.target)

        #path = fileinfo.target[1:]  # strip "/" at the head.
        #fileinfo.target = os.path.join(self.newdir, path)
        #fileinfo.save_path = os.path.join(self.savedir, path)


# vim: set sw=4 ts=4 expandtab:
