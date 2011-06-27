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
from pmaker.makers.PackageMaker import *
from pmaker.models.FileInfoFactory import FileInfoFactory
from pmaker.utils import rm_rf
from pmaker.config import Config

import optparse
import os
import os.path
import sys
import tempfile
import unittest



class Test_to_srcdir(unittest.TestCase):

    def test_to_srcdir(self):
        srcdir = "/tmp/w/src"

        self.assertEquals(to_srcdir(srcdir, "/a/b/c"), "/tmp/w/src/a/b/c")
        self.assertEquals(to_srcdir(srcdir, "a/b"),    "/tmp/w/src/a/b")
        self.assertEquals(to_srcdir(srcdir, "/"),      "/tmp/w/src/")



class TestPackageMaker(unittest.TestCase):

    def setUp(self):
        self.workdir = tempfile.mkdtemp(dir="/tmp", prefix="pmaker-tests")
        self.package = dict(
            workdir = self.workdir,
            destdir = "",
            name = "foo",
        )
        self.target_path = os.path.join(self.workdir, "a.txt")
        open(self.target_path, "w").write("a\n")

        self.fileinfos = [FileInfoFactory().create(self.target_path)]
        self.options = optparse.Values(Config.defaults())

    def tearDown(self):
        rm_rf(self.workdir)

    def helper_run_upto_step(self, step):
        pmaker = PackageMaker(self.package, self.fileinfos, self.options)
        pmaker.upto = step

        try:
            pmaker.run()
        except SystemExit:
            pass

        self.assertTrue(os.path.exists(pmaker.touch_file(step)))

    def test__init__(self):
        pmaker = PackageMaker(self.package, self.fileinfos, self.options)

    def test_shell(self):
        pmaker = PackageMaker(self.package, self.fileinfos, self.options)

        self.assertEquals(pmaker.shell("true"), 0)

    def test_genfile(self):
        pmaker = PackageMaker(self.package, self.fileinfos, self.options)

        templatedir = os.path.join(self.workdir, "templates")
        os.makedirs(templatedir)

        tmpl = os.path.join(templatedir, "aaa")
        open(tmpl, "w").write("$name")
        outfile = "out.txt"

        pmaker.template_paths = [templatedir]

        pmaker.genfile("aaa", outfile)

        self.assertTrue(os.path.exists(os.path.join(self.workdir, outfile)))
        self.assertEquals(open(os.path.join(self.workdir, outfile)).read(),
            self.package["name"])

    def test_copyfiles(self):
        pmaker = PackageMaker(self.package, self.fileinfos, self.options)
        pmaker.copyfiles()

        self.assertTrue(os.path.exists(os.path.join(pmaker.srcdir, self.target_path)))

    def test_save__and__load(self):
        pmaker = PackageMaker(self.package, self.fileinfos, self.options)
        pmaker.save()
        pmaker.load()

    def test_run__setup(self):
        self.helper_run_upto_step(STEP_SETUP)

    def test_run__preconfigure(self):
        self.helper_run_upto_step(STEP_PRECONFIGURE)

    def test_run__configure(self):
        self.helper_run_upto_step(STEP_CONFIGURE)

    def test_run__sbuild(self):
        self.helper_run_upto_step(STEP_SBUILD)

    def test_run__build(self):
        self.helper_run_upto_step(STEP_BUILD)



class TestAutotoolsTgzPackageMaker__single(unittest.TestCase):

    def setUp(self):
        self.workdir = tempfile.mkdtemp(dir="/tmp", prefix="pmaker-tests")
        package = dict(
            workdir = self.workdir,
            destdir = "",
            name = "foo",
        )
        target_path = os.path.join(self.workdir, "a.txt")
        open(target_path, "w").write("a\n")

        fileinfos = [FileInfoFactory().create(target_path)]
        options = optparse.Values(Config.defaults())

        self.pmaker = AutotoolsTgzPackageMaker(package, fileinfos, options)
        self.pmaker.template_paths = [os.path.join(os.getcwd(), "templates")]

    def tearDown(self):
        rm_rf(self.workdir)

    def helper_run_upto_step(self, step):
        self.pmaker.upto = step

        try:
            self.pmaker.run()
        except SystemExit:
            pass

        self.assertTrue(os.path.exists(self.pmaker.touch_file(step)))

    def test_preconfigure(self):
        self.helper_run_upto_step(STEP_PRECONFIGURE)

    def test_configure(self):
        self.helper_run_upto_step(STEP_CONFIGURE)


# vim: set sw=4 ts=4 expandtab:
