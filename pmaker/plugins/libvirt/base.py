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
import libvirt
import libxml2
import re
import subprocess



VMM = "qemu:///system"



def xml_context(xmlfile):
    return libxml2.parseFile(xmlfile).xpathNewContext()


def xpath_eval(xpath, xmlfile=False, ctx=None):
    """Parse given XML and evaluate given XPath expression, then returns
    result[s].
    """
    assert xmlfile or ctx, "No sufficient arguements"

    if ctx is None:
        ctx = xml_context(xmlfile)

    return [r.content for r in ctx.xpathEval(xpath)]


def get_base_image_path(image_path):
    """Resolve the path of base image for given image path with using qemu-img.

    Returns None if given image is not a delta image.
    """
    try:
        out = subprocess.check_output("qemu-img info " + image_path, shell=True)
        m = re.match(r"^backing file: (.+) \(actual path: (.+)\)$", out.split("\n")[-2])
        if m:
            (delta, base) = m.groups()
            return base

    except Exception, e:
        logging.warn("get_delta_image_path: " + str(e))
        pass

    return None


# vim:sw=4:ts=4:et:
