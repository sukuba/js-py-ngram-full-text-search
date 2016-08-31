#!/usr/bin/env python
# -*- coding: utf-8 -*-
# written for python 3 but also run on python 2
from __future__ import absolute_import, division, print_function, unicode_literals

import sys
if sys.version_info[0]  == 2:
    chr = unichr

"""
jsngram package:
  Simple N-gram full text search engine on JavaScript and Python.
  https://github.com/sukuba/js-py-ngram-full-text-search
jsngram.jsngram:
  Generates N-gram index as json files
"""

import re
import json
import os
import codecs
import shutil

from . import dir2
from . import json2

class JsNgram(object):
    """
    N-gram index storage
    """
    def __init__(self, n=2, shorter=True, src='.', dest='.', flat=False,
                 ignore=r'[\s,.，．、。]+'):
        self.db = {}
        self.n = n
        self.shorter = (shorter == True)
        self.src = os.path.realpath(src)
        self.dest = os.path.realpath(dest)
        self.flat = (flat == True)
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
            return
        nn = reversed(range(1, 1+self.n)) if self.shorter else [self.n]
        # larger n should be processed on ahead, let shorter one overwrite them.
        for n in nn:
            self.add_words_re(n, path, content, start)
        
    def add_words_re(self, n, path, content, start):
        if len(content) < n:
            self.add_index(content, path, start)
        else:
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
        
    def to_json(self, verbose=False):
        sep = '-' if self.flat else '/'
        for key in self.db.keys():
            hxs = []
            for c in key:
                h = ('%#06x' % ord(c))[2:]  # fixed length 2 bytes
                for i in range(0, len(h), 2):
                    hxs.append(h[i:i+2])
            file_name = os.path.join(self.dest, '%s.json' % sep.join(hxs))
            if verbose:
                print(file_name)
            dir2.ensure_dir(file_name)
            with codecs.open(file_name, 'w', 'utf-8') as outfile:
                json.dump(self.db[key], outfile, ensure_ascii=False)
        
    def add_files_to_json(self, paths, verbose):
        # json files will not have end tag.
        self.db = {}
        files = []
        for path in paths:
            self.add_file(path, verbose)
        
        sep = '-' if self.flat else '/'
        for key in self.db.keys():
            hxs = []
            for c in key:
                h = ('%#06x' % ord(c))[2:]  # fixed length 2 bytes
                for i in range(0, len(h), 2):
                    hxs.append(h[i:i+2])
            file_name = os.path.join(self.dest, '%s.json' % sep.join(hxs))
            if verbose:
                print(file_name)
            files.append(file_name)
            dir2.ensure_dir(file_name)
            json2.json_append(file_name, self.db[key], list=True)
        
        return(files)

class JsNgramReader(object):
    """
    N-gram index reader, for test purpose.
    """
    def __init__(self, src='.'):
        self.db = {}
        self.work = {}
        self.src = os.path.realpath(src)
        
    def read_files(self, verbose=False):
        self.db = {}
        self.work = {'files':[], 'keys':[], 'data':[]}
        trim_ext = re.compile(r'\.json')
        split_code = re.compile(r'[-/]')
        for entry in dir2.list_files(self.src):
            code = split_code.split(trim_ext.sub('', entry))
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
                        rev_key = val[1]
                        if not rev_key in bag.keys():
                            bag[rev_key] = []
                        bag[rev_key].append(key)
            self.work['reverse'][path] = bag
            
            if verbose:
                print(path)
                for key in sorted(bag.keys()):
                    print(sorted(bag[key]), end=' ')
                print('')
        

