#!/usr/bin/env python
# -*- coding: utf-8 -*-
# written for python 3 but also run on python 2
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import shutil
import datetime

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
        
        def a_file_to_json(src, dest):
            ix.add_files_to_json([src], verbose_print)
            n = len(ix.db)
            print(src, n)
            return n
            
        result = jsngram.dir2.apply_files(src, None, a_file_to_json)
        """
        for r in result:
            file_name, dest_none, n_keys = r
            print(file_name, n_keys)
            
        """
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
        print('古いインデックスを削除中')
        remove_entries(out_dir)
        print('テキストを正規化中')
        jsngram.text2.normalize_texts(org_dir, in_dir)
        print('インデックス作成開始')
        ix = make_index_by_files_inc()
        print('インデックスを保存中')
        for entry in jsngram.dir2.list_files(out_dir):
            fullpath = os.path.join(out_dir, entry)
            jsngram.json2.json_end(fullpath)
        print('終わり.')
        
    start_time = datetime.datetime.now()
    print('Start: ', start_time)
    
    test_suite1()
    
    end_time = datetime.datetime.now()
    span = end_time - start_time
    sspan = '%d seconds' % span.seconds if span.seconds < 3600 else '%d hours' % (span.days * 24)
    print('End: ', end_time, ' / runtime: ', sspan)

if __name__ == '__main__':
    test()
