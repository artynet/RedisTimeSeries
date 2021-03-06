#!/usr/bin/env python3

import sys
import os
import argparse

ROOT = HERE = os.path.abspath(os.path.dirname(__file__))
READIES = os.path.join(ROOT, "deps/readies")
sys.path.insert(0, READIES)
import paella

#----------------------------------------------------------------------------------------------

class RedisTimeSeriesSetup(paella.Setup):
    def __init__(self, nop=False):
        paella.Setup.__init__(self, nop)

    def common_first(self):
        self.pip_install("wheel")
        self.pip_install("setuptools --upgrade")

        self.install("git jq curl")
        self.run("%s/bin/getgcc" % READIES)

    def debian_compat(self):
        pass

    def redhat_compat(self):
        self.install("redhat-lsb-core")
        self.run("%s/bin/getepel" % READIES)

    def arch_compat(self):
        pass

    def fedora(self):
        self.install("python3-networkx")

    def macos(self):
        self.install_gnu_utils()

    def common_last(self):
        if self.dist == "centos" and self.ver == "8":
            self.install("https://pkgs.dyn.su/el8/base/x86_64/lcov-1.14-3.el8.noarch.rpm")
        elif self.dist == "arch":
            self.install("lcov-git", aur=True)
        else:
            self.install("lcov")
        self.run("{PYTHON} {READIES}/bin/getrmpytools".format(PYTHON=self.python, READIES=READIES))
        self.pip_install("-r tests/flow/requirements.txt")

#----------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser(description='Set up system for build.')
parser.add_argument('-n', '--nop', action="store_true", help='no operation')
args = parser.parse_args()

RedisTimeSeriesSetup(nop = args.nop).setup()
