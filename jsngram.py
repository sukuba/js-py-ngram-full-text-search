#!/usr/bin/env python
# -*- coding: utf-8 -*-
# written for python 3 but also run on python 2
from __future__ import absolute_import, division, print_function, unicode_literals

import sys
if sys.version_info[0]  == 2:
    chr = unichr

import re
import json
import os
import codecs

class JsNgram(object):
    """
    N-gram index storage
    """
    def __init__(self, n=2, shorter=True, src='.', ignore=r'[\s,.，．、。]+'):
        self.db = {}
        self.n = n
        self.shorter = (shorter == True)
        self.src = os.path.realpath(src)
        self.ignore = re.compile(ignore)
        
    def has_key(self, key):
        return key in self.db.keys()
        
    def append_key(self, key):
        if not self.has_key(key):
            self.db[key] = []
        
    def add_index(self, key, path, start):
        lowkey = key.lower()
        self.append_key(lowkey)
        self.db[lowkey].append([path, start])
        # using list instead of tuple,
        # making reverse check from json files easy in test.
        
    def add_words(self, path, content, start):
        if len(content) == 0:
            pass
        elif len(content) < self.n:
            self.add_index(content, path, start)
        else:
            n = self.n
            N = len(content)
            for i in range(n, N+1):
                pos = i - n
                self.add_index(content[pos:i], path, start + pos)
        
    def add_document(self, path, content):
        next_start = 0
        for words in self.ignore.finditer(content):
            start = next_start
            end = words.start()
            next_start = words.end()
            self.add_words(path, content[start:end], start)
        self.add_words(path, content[next_start:], next_start)
        
    def add_file(self, path, verbose):
        file_name = os.path.join(self.src, path)
        if verbose:
            print(file_name)
        with codecs.open(file_name, 'r', 'utf-8') as infile:
            text = infile.read()
        self.add_document(path, text)
        
    def to_json(self, dest, verbose=False):
        for key in self.db.keys():
            hxs = []
            for c in key:
                h = ('%#06x' % ord(c))[2:]  # fixed length 2 bytes
                for i in range(0, len(h), 2):
                    hxs.append(h[i:i+2])
            file_name = os.path.join(dest, '%s.json' % '-'.join(hxs))
            if verbose:
                print(file_name)
            with codecs.open(file_name, 'w', 'utf-8') as outfile:
                json.dump(self.db[key], outfile, ensure_ascii=False)
        

class JsNgramReader(object):
    """
    N-gram index reader, for test purpose.
    """
    def __init__(self, src='.'):
        self.db = {}
        self.work = {}
        self.src = os.path.realpath(src)
        
    def read_flatfiles(self, verbose=False):
        self.db = {}
        self.work = {'files':[], 'keys':[], 'data':[]}
        trim_ext = re.compile(r'\.json')
        for entry in os.listdir(self.src):
            code = trim_ext.sub('', entry).split('-')
            code2 = [code[i] + code[i+1] for i in range(0, len(code), 2)]
            keys = [chr(int(asc, 16)) for asc in code2]
            key = ''.join(keys)
            file_name = os.path.join(self.src, entry)
            with codecs.open(file_name, 'r', 'utf-8') as infile:
                data = json.load(infile)
            
            self.db[key] = data
            self.work['files'].append((entry, file_name))
            self.work['keys'].append((key, keys))
            self.work['data'].append(data)
            
            if verbose:
                print(entry, code, code2, key, data)
        
    def reverse(self, paths, verbose=False):
        self.work['reverse'] = {}
        for path in paths:
            bag = {}
            for key in self.db.keys():
                vals = self.db[key]
                for val in vals:
                    if(val[0] == path):
                        bag[val[1]] = key
            self.work['reverse'][path] = bag
            
            if verbose:
                print(path)
                for key in sorted(bag.keys()):
                    print(bag[key], end=' ')
                print('')
        


def test():
    base_dir = os.path.realpath('/scratch') # may be './scratch', or others.
    ngram_size = 2
    ngram_shorter = True
    in_dir = os.path.join(base_dir, 'txt')
    out_dir = os.path.join(base_dir, 'idx')
    ch_ignore = r'[\s,.，．、。]+'
    verbose_print = False
    term_colors = {'OK': '\033[92m', 'NG': '\033[91m', 'DONE': '\033[0m'}
    
    def make_index_by_strings(data, n=ngram_size, shorter=ngram_shorter,
          src=in_dir, ignore=ch_ignore, out=out_dir):
        """
        data example: array of [path, content]
            [
                [u'this/is/a.txt', u'This is a document.'],
                [u'that/may/be/too.txt', u'This is the next one.']
            ]
        """
        ix = JsNgram(n, shorter, src, ignore)
        for doc in data:
            path, content = doc
            ix.add_document(path, content)
        for entry in os.listdir(out):
            os.remove(os.path.join(out, entry))
        ix.to_json(out, verbose_print)
        return ix
        
    def make_index_by_files(n=ngram_size, shorter=ngram_shorter,
          src=in_dir, ignore=ch_ignore, out=out_dir):
        """
        text files in src directory will be indexed.
        """
        ix = JsNgram(n, shorter, src, ignore)
        for entry in os.listdir(src):
            ix.add_file(entry, verbose_print)
        for entry in os.listdir(out):
            os.remove(os.path.join(out, entry))
        ix.to_json(out, verbose_print)
        return ix
        
    def read_index(src=out_dir):
        chk = JsNgramReader(src)
        chk.read_flatfiles(verbose_print)
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
        
    test_suite1()
    test_suite2()
    test_suite3()

if __name__ == '__main__':
    test()
