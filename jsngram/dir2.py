#!/usr/bin/env python
# -*- coding: utf-8 -*-
# written for python 3 but also run on python 2
from __future__ import absolute_import, division, print_function, unicode_literals

"""
jsngram package:
  Simple N-gram full text search engine on JavaScript and Python.
  https://github.com/sukuba/js-py-ngram-full-text-search
jsngram.dir2:
  file and directory tools
"""

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
    
def apply_files(path, func):
    """
    scan files in a directory recursively, excluding dot files and dot directories.
    apply 'func' to each file.
    'func' is a function with an argument of the file full path.
    return a file list with the return values of 'func'.
    """
    bag = []
    for entry in os.listdir(path):
        if entry[0] == '.':
            continue  # skip dot files and directories
        fullpath = os.path.join(path, entry)
        if os.path.isfile(fullpath):
            bag += [(fullpath, func(fullpath))]
        else:
            bag += apply_files(fullpath, func)
    return bag;
    
def test():
    base_dir = os.path.realpath('/scratch') # may be './scratch', or others.
    target = os.path.join(base_dir, 'hoge1')
    
    def myfunc(path):
        return path
        
    ret = apply_files(target, myfunc)
    print(ret)

if __name__ == '__main__':
    test()
