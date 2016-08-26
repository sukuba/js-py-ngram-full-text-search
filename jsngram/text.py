#!/usr/bin/env python
# -*- coding: utf-8 -*-
# written for python 3 but also run on python 2
from __future__ import absolute_import, division, print_function, unicode_literals

import sys
if sys.version_info[0]  == 2:
    chr = unichr

import os
import unicodedata

def normalText(text):
    """
    normalize to Hanaku alphanum and Zenkaku kana.
    """
    return unicodedata.normalize('NFKC', text)

def normalizeTexts(src, dest=None):
    """
    normalize text files at src to dest.
    src will be overwritten when dest=None.
    """
    if os.path.isfile(src):
        # read from src, normalize and write to dest (or src when dest=None)
        
        
    else:
        for entry in os.listdir(src):
            if entry[0] == '.':
                continue  # skip dot files and directories
            nextpath = os.path.join(src, entry)
            nextdest = os.path.join(dest, entry) if dest else None
            normalizeTexts(nextpath, nextdest)
    
