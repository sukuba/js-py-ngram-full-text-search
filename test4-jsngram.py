#!/usr/bin/env python
# -*- coding: utf-8 -*-
# written for python 3 but also run on python 2
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import shutil
import datetime

import jsngram.jsngram
import jsngram.dir2

def test():
    base_dir = os.path.realpath('/scratch') # may be './scratch', or others.
    ngram_size = 2
    ngram_shorter = True
    in_dir = os.path.join(base_dir, 'txt')
    out_dir = os.path.join(base_dir, 'idx')
    ch_ignore = r'[\s,.，．、。]+'
    flat_dir = False
    verbose_print = False
    files_at_once = 100
    
    def make_index_by_files_inc(n=ngram_size, shorter=ngram_shorter,
          src=in_dir, dest=out_dir, flat=flat_dir, ignore=ch_ignore):
        """
        text files in src directory will be indexed.
        """
        ix = jsngram.jsngram.JsNgram(n, shorter, src, dest, flat, ignore)
        entries = jsngram.dir2.list_files(src)
        n = len(entries)
        for files in (entries[i:i+files_at_once] for i in range(0, n, files_at_once)):
            ix.add_files_to_json(files, verbose_print)
            print('%d indexes in %d files' % (len(ix.db), len(files)))
            for f in files:
                print(' ' + f)
        print('%d files processed.' % len(entries))
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
        print('Removing current index files ...')
        remove_entries(out_dir)
        
        print('Building index files ...')
        ix = make_index_by_files_inc()
        
        print('Adjusting index files ...')
        entries = jsngram.dir2.list_files(out_dir)
        for entry in entries:
            fullpath = os.path.join(out_dir, entry)
            jsngram.json2.json_end(fullpath)
        print('%d indexes' % len(entries))
        
        print('Done.')
        
    start_time = datetime.datetime.now()
    print('Start: ', start_time)
    
    test_suite1()
    
    end_time = datetime.datetime.now()
    span = end_time - start_time
    sspan = '%d seconds' % span.seconds if span.seconds < 3600 else '%d hours' % (span.days * 24)
    print('End: ', end_time, ' / runtime: ', sspan)

if __name__ == '__main__':
    test()
