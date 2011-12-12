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
import tests.common as TC
import pmaker.environ as E
import pmaker.tests.common as C

import os.path
import shutil
import unittest


def bootstrap(fileslist="files.list"):
    (name, pversion) = ("foo", "0.0.3")

    (workdir, args) = TC.setup(
        ["--name", name, "--pversion", pversion]
    )
    listfile = os.path.join(workdir, fileslist)

    args = args + [
        "--backend", "autotools.single.tgz", "-vv", listfile
    ]
    pn = "%s-%s" % (name, pversion)

    comp_ext = E.Env().compressor.extension
    tgz = os.path.join(workdir, pn, pn + ".tar." + comp_ext)

    return (workdir, args, listfile, tgz)


class Test_00_filelist(unittest.TestCase):

    def setUp(self):
        (self.workdir, self.args, self.listfile, self.pkgfile) = bootstrap()

    def tearDown(self):
        C.cleanup_workdir(self.workdir)

    def test_00_generated_file(self):
        target = os.path.join(self.workdir, "aaa.txt")

        open(target, "w").write("\n")
        open(self.listfile, "w").write("%s\n" % target)

        TC.run_w_args(self.args, self.workdir)

        self.assertTrue(os.path.exists(self.pkgfile))

    def test_01_generated_files(self):
        os.makedirs(os.path.join(self.workdir, "b"))
        os.makedirs(os.path.join(self.workdir, "b", "c"))

        targets = [
            os.path.join(self.workdir, "aaa.txt"),
            os.path.join(self.workdir, "b", "d.x"),
            os.path.join(self.workdir, "b", "c", "e"),
        ]

        for t in targets:
            open(t, "w").write("\n")

        open(self.listfile, "w").write("%s\n" % "\n".join(targets))

        TC.run_w_args(self.args, self.workdir)

        self.assertTrue(os.path.exists(self.pkgfile))

    def test_02_system_file(self):
        target = TC.get_random_system_files(1, "/etc/*")

        open(self.listfile, "w").write("%s\n" % target)

        TC.run_w_args(self.args, self.workdir)

        self.assertTrue(os.path.exists(self.pkgfile))

    def test_03_system_files(self):
        targets = TC.get_random_system_files(50, "/etc/*")

        open(self.listfile, "w").write("%s\n" % "\n".join(targets))

        TC.run_w_args(self.args, self.workdir)

        self.assertTrue(os.path.exists(self.pkgfile))


class Test_01_json(unittest.TestCase):

    def setUp(self):
        (self.workdir, self.args, self.listfile, self.pkgfile) = \
            bootstrap("files.json")

    def tearDown(self):
        C.cleanup_workdir(self.workdir)

    def test_00_generated_file(self):
        if E.json is None:
            return

        target = os.path.join(self.workdir, "aaa.txt")
        open(target, "w").write("\n")

        data = {"files": [{"path": target}]}
        E.json.dump(data, open(self.listfile, "w"))

        self.args += ["--input-type", "filelist.json"]
        TC.run_w_args(self.args, self.workdir)

        self.assertTrue(os.path.exists(self.pkgfile))


# vim:sw=4 ts=4 et:
