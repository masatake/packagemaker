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
from pmaker.configurations import Config, _defaults
from pmaker.models.Bunch import Bunch
from pmaker.tests.common import setup_workdir, cleanup_workdir

import pmaker.environ as E

import os
import os.path
import unittest


class Test_01_functions(unittest.TestCase):

    def test_00__defaults(self):
        dfs = _defaults(E.Env())

        self.assertTrue(isinstance(dfs, Bunch))

    def test_01__defaults_w_modified_env(self):
        dfs_ref = _defaults(E.Env())

        env = E.Env()
        env.workdir = "/a/b/c"  # modified.

        dfs = _defaults(E.Env())

        self.assertNotEquals(dfs_ref, dfs)
        self.assertEquals(dfs.workdir, env.workdir)


class Test_02_Config(unittest.TestCase):

    def setUp(self):
        self.workdir = setup_workdir()
        self.config = os.path.join(self.workdir, "test_config.json")

    def tearDown(self):
        cleanup_workdir(self.workdir)

    def test_00__init__w_norc(self):
        cfg = Config(norc=True)
        dfs = _defaults(E.Env())  # reference of cfg.

        for k, v in dfs.iteritems():
            self.assertEquals(getattr(cfg, k), v)

        self.assertTrue(cfg.missing_files())

    def test_01__norc_and_load_json_config(self):
        cfg = Config(norc=True)
        dfs = _defaults(E.Env())

        content = """
{
    "verbosity": 1,
    "input_type": "filelist.json",
    "summary": "JSON Configuration test",
    "ignore_owner": true,
    "no_mock": true,
    "files": [
        {
            "path": "/a/b/c",
            "attrs" : {
                "create": true,
                "install_path": "/a/c",
                "uid": 100,
                "gid": 0,
                "rpmattr": "%config(noreplace)"
            }
        }
    ]
}
"""
        open(self.config, "w").write(content)
        cfg.load(self.config)

        self.assertEquals(cfg.verbosity, 1)
        self.assertEquals(cfg.input_type, "filelist.json")
        self.assertEquals(cfg.summary, "JSON Configuration test")
        self.assertEquals(cfg.ignore_owner, True)
        self.assertEquals(cfg.no_mock, True)

        self.assertNotEquals(cfg.files, None)
        self.assertFalse(cfg.missing_files())


# vim:sw=4 ts=4 et:
