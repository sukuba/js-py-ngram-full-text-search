#!/usr/bin/env python
# -*- coding: utf-8 -*-
# written for python 3 but also run on python 2
from __future__ import absolute_import, division, print_function, unicode_literals

"""
jsngram package:
  Simple N-gram full text search engine on JavaScript and Python.
  https://github.com/sukuba/js-py-ngram-full-text-search
jsngram.text2:
  utf-8 text tools
"""

import os
import codecs
import unicodedata

if __name__ == '__main__':
    import dir2
else:
    from . import dir2

def normal_text(text):
    """
    normalize to Hanaku alphanum and Zenkaku kana.
    """
    return unicodedata.normalize('NFKC', text)

def normalize_texts(src, dest=None):
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
        dest_text = normal_text(src_text)
        if dest:
            dir2.ensure_dir(dest)
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
            normalize_texts(nextpath, nextdest)
    

def test():
    base_dir = os.path.realpath('/scratch') # may be './scratch', or others.
    a = u'aｂ1２ｶキ'
    an = u'ab12カキ'
    file1 = os.path.join(base_dir, 'out1.txt')
    file2 = os.path.join(base_dir, 'out2.txt')
    
    def test_normal_text1():
        b = normal_text(a)
        res = b == an
        print('[%s]: text should be normalized.  normal_text1' % 'OK' if res else 'NG')
        
    def test_normalize_texts1():
        with codecs.open(file1, 'w', 'utf-8') as outfile:
            outfile.write(a)
        normalize_texts(file1, file2)
        with codecs.open(file2, 'r', 'utf-8') as infile:
            b = infile.read()
        res = b == an
        print('[%s]: text should be normalized.  normalize_texts1' % 'OK' if res else 'NG')
        
    def test_normalize_texts2():
        with codecs.open(file1, 'w', 'utf-8') as outfile:
            outfile.write(a)
        normalize_texts(file1)
        with codecs.open(file1, 'r', 'utf-8') as infile:
            b = infile.read()
        res = b == an
        print('[%s]: text should be normalized.  normalize_texts2' % 'OK' if res else 'NG')
        
    test_normal_text1()
    test_normalize_texts1()
    test_normalize_texts2()

if __name__ == '__main__':
    test()
