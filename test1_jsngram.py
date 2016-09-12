#!/usr/bin/env python
# -*- coding: utf-8 -*-
# written for python 3 but also run on python 2
from __future__ import absolute_import, division, print_function, unicode_literals

import sys
if sys.version_info[0]  == 2:
    chr = unichr

import os
import shutil

import jsngram.jsngram
import jsngram.dir2
import jsngram.text2

def test():
    base_dir = os.path.realpath('/scratch') # may be './scratch', or others.
    ngram_size = 2
    ngram_shorter = True
    in_dir = os.path.join(base_dir, 'txt')
    out_dir = os.path.join(base_dir, 'idx')
    ch_ignore = r'[\s,.，．、。]+'
    flat_dir = False
    verbose_print = False
    term_colors = {'OK': '\033[92m', 'NG': '\033[91m', 'DONE': '\033[0m'}
    
    def make_index_by_strings(data, n=ngram_size, shorter=ngram_shorter,
          src=in_dir, dest=out_dir, flat=flat_dir, ignore=ch_ignore):
        """
        data example: array of [path, content]
            [
                [u'this/is/a.txt', u'This is a document.'],
                [u'that/may/be/too.txt', u'This is the next one.']
            ]
        """
        ix = jsngram.jsngram.JsNgram(n, shorter, src, dest, flat, ignore)
        for doc in data:
            path, content = doc
            ix.add_document(path, content)
        remove_entries(dest)
        ix.to_json(verbose=verbose_print)
        return ix
        
    def make_index_by_files(n=ngram_size, shorter=ngram_shorter,
          src=in_dir, dest=out_dir, flat=flat_dir, ignore=ch_ignore):
        """
        text files in src directory will be indexed.
        """
        ix = jsngram.jsngram.JsNgram(n, shorter, src, dest, flat, ignore)
        for entry in jsngram.dir2.list_files(src):
            ix.add_file(entry, verbose_print)
        remove_entries(dest)
        ix.to_json(verbose=verbose_print)
        return ix
        
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
        
    def read_index(src=out_dir):
        chk = jsngram.jsngram.JsNgramReader(src)
        chk.read_files(verbose_print)
        return chk
        
    def test_suite1():
        ix = make_index_by_strings(
            [
                [u'this/is/a.txt', u'This is a document.'],
                [u'that/may/be/too.txt', u'This is the next one.']
            ]
          )
        chk = read_index()
        chk.reverse([u'this/is/a.txt', u'that/may/be/too.txt'], verbose_print)
        res = 'OK' if chk.db == ix.db else 'NG'
        print('[%s]: db should match.  suite1' % res)
        
    def test_suite2():
        ix = make_index_by_strings(
            [
                [u'http://a.is.ja', u"私たちは、もっとも始めに、この文書 a を追加してみます。"],
                [u'http://b.is.ja/too', u'2つ目はもっともっとおもしろいよ、ね。']
            ]
          )
        chk = read_index()
        chk.reverse([u'http://a.is.ja', u'http://b.is.ja/too'], verbose_print)
        res = 'OK' if chk.db == ix.db else 'NG'
        print('[%s]: db should match.  suite2' % res)
        
    def test_suite3():
        ix = make_index_by_files()
        chk = read_index()
        #chk.reverse([u'this/is/a.txt', u'that/may/be/too.txt'], verbose_print)
        res = 'OK' if chk.db == ix.db else 'NG'
        print('[%s]: db should match.  suite3' % res)
        
    def test_suite4():
        src = os.path.join(base_dir, 'hoge1')
        dest = os.path.join(base_dir, 'hoge2')
        jsngram.text2.normalize_texts(src, dest)
        print('[]: normalized.  suite4')
        
    def test_suite5():
        src = os.path.join(base_dir, 'hoge2')
        dest = None
        jsngram.text2.normalize_texts(src, dest)
        print('[]: normalized.  suite5')
        
    def test_suite6():
        remove_entries(out_dir)
        ix = make_index_by_files_inc()
        for entry in jsngram.dir2.list_files(out_dir):
            fullpath = os.path.join(out_dir, entry)
            jsngram.json2.json_end(fullpath)
        chk = read_index()
        res = 'OK' if chk.db == ix.db else 'NG'
        print('[%s]: db should match.  suite6' % res)
        
    test_suite1()
    test_suite2()
    test_suite3()
    test_suite4()
    test_suite5()
    test_suite6()

if __name__ == '__main__':
    test()
