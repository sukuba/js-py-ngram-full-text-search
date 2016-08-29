#!/usr/bin/env python
# -*- coding: utf-8 -*-
# written for python 3 but also run on python 2
from __future__ import absolute_import, division, print_function, unicode_literals

import os

def ensure_dir(path):
    """
    make parent directories of path recursively, when they do not exist.
    """
    parent = os.path.dirname(path)
    if not os.path.exists(parent):
        os.makedirs(parent)
    

def list_files(path, base=None):
    """
    list files in a directory recursively, excluding dot files and dot directories.
    return array of relative to path and alwasy use '/' even on Windows.
    """
    if not base:
        base = path
    bag = []
    for entry in os.listdir(path):
        if entry[0] == '.':
            continue  # skip dot files and directories
        fullpath = '/'.join([path, entry])  # not use os.path.join
        if os.path.isfile(fullpath):
            bag.append(fullpath[1+len(base):])  # not use os.path.relpath
        else:
            bag += list_files(fullpath, base)
    return bag;
    
