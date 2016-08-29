#!/usr/bin/env python
# -*- coding: utf-8 -*-
# written for python 3 but also run on python 2
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import codecs
import unicodedata

from . import dir

def normalText(text):
    """
    normalize to Hanaku alphanum and Zenkaku kana.
    """
    return unicodedata.normalize('NFKC', text)

def normalizeTexts(src, dest=None):
    """
    normalize text files at src to dest.
    dest must be a directory when src is a directory.
    dest means a file when src is a file.
    src will be overwritten when dest=None.
    """
    if os.path.isfile(src):
        # read from src, normalize and write to dest (or src when dest=None)
        with codecs.open(src, 'r', 'utf-8') as infile:
            src_text = infile.read()
        dest_text = normalText(src_text)
        if dest:
            dir.ensure_dir(dest)
        else:
            dest = src
        with codecs.open(dest, 'w', 'utf-8') as outfile:
            outfile.write(dest_text)
    else:
        for entry in os.listdir(src):
            if entry[0] == '.':
                continue  # skip dot files and directories
            nextpath = os.path.join(src, entry)
            nextdest = os.path.join(dest, entry) if dest else None
            normalizeTexts(nextpath, nextdest)
    
