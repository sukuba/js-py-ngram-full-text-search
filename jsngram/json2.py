#!/usr/bin/env python
# -*- coding: utf-8 -*-
# written for python 3 but also run on python 2
from __future__ import absolute_import, division, print_function, unicode_literals

"""
jsngram package:
  Simple N-gram full text search engine on JavaScript and Python.
  https://github.com/sukuba/js-py-ngram-full-text-search
jsngram.json2:
  json array increment filer

json_append:
  append an object without an end bracket.
  if the file doesn't exist, make it to begin.

json_end:
  put an end bracket.

example:
  json_append('/tmp/out.json', ['a',0])
  json_append('/tmp/out.json', ['b',1])
  json_append('/tmp/out.json', ['c',2])
  json_end('/tmp/out.json')

output:
[
 ['a',0]
,['b',1]
,['c',2]
]

"""

import os
import codecs
import json
import re

start_tag = '['
end_tag = ']'
new_line = '\n'
delimiter1 = ' '
delimiter2 = ','

re_has_end = re.compile(r'^]$')

def json_append(file_name, x, list=False, end=False):
    """
    append an object to the json file.
    file should not have any end brackets. (append without looking)
    file_name: json file name
    x: object to append
    list: x is a list of objects to append
    end: with or without the end bracket
    """
    is_new = not os.path.exists(file_name)
    sep = new_line + delimiter2
    with codecs.open(file_name, 'a', 'utf-8') as outfile:
        if is_new:
            outfile.writelines((start_tag, new_line, delimiter1))
        else:
            outfile.write(sep)
        if list:
            dump = sep.join((json.dumps(xx, ensure_ascii=False) for xx in x))
        else:
            dump = json.dumps(x, ensure_ascii=False)
        outfile.write(dump)
        if end:
            outfile.writelines((new_line, end_tag))
    
def json_end(file_name):
    """
    put an end bracket.
    file should not have any end brackets. (append without looking)
    file_name: json file name
    """
    with codecs.open(file_name, 'a', 'utf-8') as outfile:
        outfile.writelines((new_line, end_tag))

def has_end(file_name):
    """
    True if the json file has an end bracket.
    do not perform entire grammer check.
    just watch if the end line is the end bracket only.
    """
    with codecs.open(file_name, 'r', 'utf-8') as infile:
        for line in infile:
            pass
    return(re_has_end.match(line))
    
def test():
    base_dir = os.path.realpath('/scratch') # may be './scratch', or others.
    data = [
            ['a',0]
           ,['b',1]
           ,['c',2]
           ]
    file = os.path.join(base_dir, 'out.txt')
    
    def test_json_append1():
        if os.path.exists(file):
            os.remove(file)
        for x in data:
            json_append(file, x, end=True)
        
    def test_json_append2():
        if os.path.exists(file):
            os.remove(file)
        for x in data:
            json_append(file, x)
        
    def test_json_end():
        json_end(file)
        
    def test_json_match(tag):
        with codecs.open(file, 'r', 'utf-8') as infile:
            x = json.load(infile)
        res = data == x
        print('[%s]: json object should match.  test_json_match(%s)' % ('OK' if res else 'NG', tag))
        
    def test_has_end():
        res = has_end(file)
        print('[%s]: json object should have end.  test_has_end' % 'OK' if res else 'NG')
        
    def test_has_no_end():
        res = not has_end(file)
        print('[%s]: json object should not have end.  test_has_no_end' % 'OK' if res else 'NG')
        
    def test_json_append3():
        if os.path.exists(file):
            os.remove(file)
        json_append(file, data, list=True, end=True)
        
    
    test_json_append1()
    test_json_append2()
    test_has_no_end()
    test_json_end()
    test_json_match('#1')
    test_has_end()
    test_json_append3()
    test_json_match('#2')

if __name__ == '__main__':
    test()
