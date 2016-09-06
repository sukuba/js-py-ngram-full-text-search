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
    
def apply_files(path, dest, func, exclude_root_files=False):
    """
    scan files in a directory recursively, excluding dot files and dot directories.
    apply 'func' to each file.
    'func' is a function with two arguments (full path of source file, destination directory).
    return a file list with destination and return values of 'func'.
    create dest directory tree before calling func unless dest=None.
    """
    bag = []
    if dest and not os.path.exists(dest):
        os.makedirs(dest)
    for entry in os.listdir(path):
        if entry[0] == '.':
            continue  # skip dot files and directories
        fullpath = os.path.join(path, entry)
        if os.path.isfile(fullpath):
            if not exclude_root_files:
                bag += [(fullpath, dest, func(fullpath, dest))]
        else:
            next_dest = os.path.join(dest, entry) if dest else None
            bag += apply_files(fullpath, next_dest, func)
    return bag;
    
def test():
    base_dir = os.path.realpath('/scratch') # may be './scratch', or others.
    target = os.path.join(base_dir, 'hoge1')
    
    def myfunc(path, dest):
        return path
        
    ret = apply_files(target, None, myfunc)
    print(ret)
    
    out_dir = os.path.join(base_dir, 'hoge3')
    ret = apply_files(target, out_dir, myfunc)
    print(ret)
    
    ret = apply_files(target, None, myfunc, True)
    print(ret)
    

if __name__ == '__main__':
    test()
