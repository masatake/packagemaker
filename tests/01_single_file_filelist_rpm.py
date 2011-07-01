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
from pmaker.cui import main as cui_main
from pmaker.utils import rm_rf

import glob
import logging
import os
import os.path
import random
import sys
import tempfile
import unittest



def helper_is_rpm_based_system():
    if os.path.exists("/var/lib/rpm"):
        return True
    else:
        print >> sys.stderr, "This system does not look a RPM-based system."
        return False



class Test_cui_main__single_file_rpm(unittest.TestCase):

    def setUp(self):
        self.workdir = tempfile.mkdtemp(dir="/tmp", prefix="pmaker-tests")
        self.pmworkdir = os.path.join(self.workdir, "pm")
        self.listfile = os.path.join(self.workdir, "files.list")
        self.template_path = os.path.join(os.getcwd(), "templates")

        logging.getLogger().setLevel(logging.WARNING) # suppress log messages

    def tearDown(self):
        rm_rf(self.workdir)

    def helper_run_with_args(self, args):
        try:
            cui_main(args.split())
        except SystemExit:
            pass

        #self.assertTrue(...something_to_confirm_access...)

    def test_00_generated_file__wo_mock(self):
        if not helper_is_rpm_based_system():
            return

        target = os.path.join(self.workdir, "aaa.txt")
        os.system("touch " + target)

        open(self.listfile, "w").write("%s\n" % target)

        args = "argv0 --name foobar --template-path %s -w %s --format %s --no-mock %s" % \
            (self.template_path, self.pmworkdir, "rpm", self.listfile)
        self.helper_run_with_args(args)

    def test_01_generated_file__w_mock(self):
        if not helper_is_rpm_based_system():
            return

        target = os.path.join(self.workdir, "aaa.txt")
        os.system("touch " + target)

        open(self.listfile, "w").write("%s\n" % target)

        args = "argv0 --name foobar --template-path %s -w %s --format %s %s" % \
            (self.template_path, self.pmworkdir, "rpm", self.listfile)
        self.helper_run_with_args(args)

    def test_02_system_file__no_conflicts__wo_mock(self):
        if not helper_is_rpm_based_system():
            return

        # These should be owned by no any other rpms:
        targets = [
            "/etc/aliases.db",
            "/etc/grub.conf",
            "/etc/mdadm.conf",
            "/etc/prelink.cache",
            "/etc/resolv.conf"
        ]

        target = random.choice([f for f in targets if os.path.exists(f)])

        open(self.listfile, "w").write("%s\n" % target)

        args = "argv0 --name foobar --template-path %s -w %s --format %s --no-mock %s" % \
            (self.template_path, self.pmworkdir, "rpm", self.listfile)
        self.helper_run_with_args(args)


    def test_03_system_file__conflicts__wo_mock(self):
        if not helper_is_rpm_based_system():
            return

        # These are owned by other rpms:
        targets = [
            "/etc/hosts",
            "/etc/sysctl.conf",
            "/etc/inittab",
            "/etc/bashrc",
            "/etc/sysconfig/network",
            "/etc/rc.d/rc.local",
        ]

        target = random.choice([f for f in targets if os.path.exists(f)])

        open(self.listfile, "w").write("%s\n" % target)

        args = "argv0 --name foobar --template-path %s -w %s --format %s --no-mock %s" % \
            (self.template_path, self.pmworkdir, "rpm", self.listfile)
        self.helper_run_with_args(args)


# vim: set sw=4 ts=4 expandtab: