#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Yuki Furuta <furushchev@jsk.imi.i.u-tokyo.ac.jp>

import os
import errno
from distutils.dir_util import copy_tree
import shutil


def generate_framework(name, version, headers_dir, lib_path, dest):
    fname = name + '.framework'
    dst_dir = os.path.join(dest, fname)
    __generate_skeleton(name, dst_dir)
    copy_tree(headers_dir, os.path.join(dst_dir, 'Headers'))
    shutil.copyfile(lib_path,
                    os.path.join(dst_dir, 'Versions', 'Current', name))


def __makedir(*dest):
    d = os.path.join(*dest)
    try:
        os.makedirs(d)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(d):
            pass
        else:
            raise e

def __generate_skeleton(name, dest):
    __makedir(dest)
    __makedir(dest, 'Versions', 'A', 'Resources')
    __makedir(dest, 'Versions', 'A', 'Headers')
    __makedir(dest, 'Versions', 'A', 'Documentation')
    os.symlink('A',
               os.path.join(dest, 'Versions', 'Current'))
    os.symlink(os.path.join('Versions', 'Current', 'Headers'),
               os.path.join(dest, 'Headers'))
    os.symlink(os.path.join('Versions', 'Current', 'Resources'),
               os.path.join(dest, 'Resources'))
    os.symlink(os.path.join('Versions', 'Current', 'Documentation'),
               os.path.join(dest, 'Documentation'))
    os.symlink(os.path.join('Versions', 'Current', name),
               os.path.join(dest, name))

if __name__ == '__main__':
    pass
