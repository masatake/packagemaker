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
from pmaker.globals import PMAKER_TEMPLATE_VERSION as TVER

import pmaker.backend.buildrpm.tgz as T
import pmaker.rpmutils as R
import pmaker.utils as U

import logging
import os.path


class Backend(T.Backend):
    """
    FIXME: Extract common parts in backend classes:
    (pmaker.backend.{autotools.single,buildrpm}.rpm.Backend
    """

    _format = "rpm"

    # FIXME: Fix naming convention of relation keys.
    _relations = {
        "requires": "Requires",
        "requires.pre": "Requires(pre)",
        "requires.preun": "Requires(preun)",
        "requires.post": "Requires(post)",
        "requires.postun": "Requires(postun)",
        "requires.verify": "Requires(verify)",
        "conflicts": "Conflicts",
        "provides": "Provides",
        "obsoletes": "Obsoletes",
    }

    # Initialize this in __init__ method:
    #_templates = ...

    def __init__(self, pkgdata, **kwargs):
        super(Backend, self).__init__(pkgdata, **kwargs)

        self._templates += [
            (TVER + "/buildrpm/package.spec", self.pkgdata.name + ".spec"),
        ]

        self.on_debug_mode = U.on_debug_mode()

    def __build_srpm(self):
        cmd = "make srpm"

        if not self.on_debug_mode:
            cmd += " V=0 > " + self.logfile("make_srpm")

        return self.shell(cmd)

    def __build_rpm(self):
        use_mock = not self.pkgdata.no_mock

        if use_mock:
            try:
                self.shell("mock --version > /dev/null")

            except RuntimeError, e:
                logging.warn(
                    "Mock is not found. Fallback to plain rpmbuild..."
                )
                use_mock = False

        if use_mock:
            dist = self.pkgdata.dist
            srpm = R.srcrpm_name_by_rpmspec(
                os.path.join(self.workdir, self.pkgdata.name + ".spec")
            )
            cmd = "mock -r %s %s" % (dist, srpm)

            if not self.on_debug_mode:
                cmd += " --quiet"

            self.shell(cmd)
            print "  GEN    rpm"  # mimics the message of "make rpm"

            return self.shell(
                "mv /var/lib/mock/%s/result/*.rpm %s" % (dist, self.workdir)
            )
        else:
            cmd = "make rpm"

            if not self.on_debug_mode:
                cmd += " rpm V=0 > " + self.logfile("make_rpm")

            return self.shell(cmd)

    def sbuild(self):
        super(Backend, self).sbuild()
        self.__build_srpm()

    def build(self):
        super(Backend, self).build()
        self.__build_rpm()


# vim:sw=4 ts=4 et: