from distutils.core import setup, Command

import datetime
import glob
import os
import sys

try:
    import nose
except ImportError:
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        raise ImportError("python-nose is must for testing.")


PACKAGE = "packagemaker"

VERSION = "0.2.99" + "." + datetime.datetime.now().strftime("%Y%m%d")


curdir = os.getcwd()


def list_basenames(d, gpat="*", pred=os.path.isfile):
    return [os.path.basename(f) for f in glob.glob(os.path.join(d, gpat)) if pred(f)]


pkgs = ["pmaker", ]

templates_topdir = "share/pmaker/templates"

data_files = [
# TODO:
#   ("share/man/man1", ["man/pmaker.1", ])
    (os.path.join(templates_topdir, "common"),
        list_basenames(os.path.join(curdir, "templates/common"))),
    (os.path.join(templates_topdir, "common/debian"),
        list_basenames(os.path.join(curdir, "templates/common/debian"))),
    (os.path.join(templates_topdir, "common/debian/source"),
        list_basenames(os.path.join(curdir, "templates/common/debian/source"))),
    (os.path.join(templates_topdir, "autotools"),
        list_basenames(os.path.join(curdir, "templates/autotools"))),
    (os.path.join(templates_topdir, "autotools/debian"),
        list_basenames(os.path.join(curdir, "autotools/debian"))),
    (os.path.join(templates_topdir, "share/templates/autotools/debian"),
        list_basenames(os.path.join(curdir, "autotools/debian"))),
]


test_targets = \
    glob.glob(os.path.join(curdir, "pmaker/tests/*.py")) + \
    glob.glob(os.path.join(curdir, "pmaker/*/tests/*.py"))



class TestCommand(Command):

    user_options = []
    test_driver = os.path.join(curdir, "runtest.sh")

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for f in test_targets:
            os.system("PYTHONPATH=%s %s %s" % (curdir, self.test_driver, f))



class SrpmCommand(Command):

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.run_command('sdist')
        self.build_rpm()

    def build_rpm(self):
        params = dict()

        topdir = params["topdir"] = os.path.abspath(os.curdir)
        rpmdir = params["rpmdir"] = os.path.join(topdir, "dist")
        rpmspec = params["rpmspec"] = os.path.join(topdir, "%s.spec" % PACKAGE)

        for subdir in ("RPMS", "BUILD", "BUILDROOT"):
            sdir = params[subdir] = os.path.join(rpmdir, subdir)

            if not os.path.exists(sdir):
                os.makedirs(sdir, 0755)

        open(rpmspec, "w").write(open(rpmspec + ".in").read().replace("@VERSION@", VERSION))

        cmd = """rpmbuild -bs \
            --define \"_topdir %(rpmdir)s\" --define \"_srcrpmdir %(rpmdir)s\" \
            --define \"_sourcedir %(topdir)s/dist\" --define \"_buildroot %(BUILDROOT)s\" \
            %(rpmspec)s
            """ % params

        os.system(cmd)



setup(name=PACKAGE,
      version=VERSION,
      description="",
      author="Satoru SATOH",
      author_email="satoru.satoh@gmail.com",
      license="GPLv3+",
      url="https://github.com/ssato/packagemaker",
      package_dir={"pmaker": "pmaker"},
      scripts=["tools/pmaker"],
      packages=pkgs,
      data_files=data_files,
      cmdclass={
          "test": TestCommand,
          "srpm": SrpmCommand,
      },
)

# vim: set sw=4 ts=4 et:
