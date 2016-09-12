#!/usr/bin/env python
# -*- coding: utf-8 -*-
# written for python 3 but also run on python 2
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import shutil

import jsngram.jsngram
import jsngram.dir2
import jsngram.text2

def test():
    base_dir = os.path.realpath('/scratch') # may be './scratch', or others.
    ngram_size = 2
    ngram_shorter = True
    org_dir = os.path.join(base_dir, 'org')
    in_dir = os.path.join(base_dir, 'txt')
    out_dir = os.path.join(base_dir, 'idx')
    ch_ignore = r'[\s,.，．、。]+'
    flat_dir = False
    verbose_print = False
    
    def make_index_by_files_inc(n=ngram_size, shorter=ngram_shorter,
          src=in_dir, dest=out_dir, flat=flat_dir, ignore=ch_ignore):
        """
        text files in src directory will be indexed.
        """
        ix = jsngram.jsngram.JsNgram(n, shorter, src, dest, flat, ignore)
        entries = jsngram.dir2.list_files(src)
        ix.add_files_to_json(entries, verbose_print)
        return ix
        
    def remove_entries(dest):
        """
        remove files and subdirectories at dest
        """
        for entry in os.listdir(dest):
            fullpath = os.path.join(dest, entry)
            if os.path.isfile(fullpath):
                os.remove(fullpath)
            else:
                shutil.rmtree(fullpath)
        
    def test_suite1():
        remove_entries(out_dir)
        jsngram.text2.normalize_texts(org_dir, in_dir)
        ix = make_index_by_files_inc()
        for entry in jsngram.dir2.list_files(out_dir):
            fullpath = os.path.join(out_dir, entry)
            jsngram.json2.json_end(fullpath)
        print('Done.')
        
    test_suite1()

if __name__ == '__main__':
    test()
