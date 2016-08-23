#!python3

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
        self.db[lowkey].append((path, start))
        
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
        
    def add_file(self, path):
        file_name = os.path.join(self.src, path)
        print(file_name)
        with codecs.open(file_name, 'r', 'utf-8') as infile:
            text = infile.read()
        self.add_document(path, text)
        
    def to_json(self, dest):
        for key in self.db.keys():
            hxs = []
            for c in key:
                h = ('%#06x' % ord(c))[2:]  # fixed length 2 bytes
                #h = hex(ord(c))[2:]
                #print(h)
                for i in range(0, len(h), 2):
                    #print(i, h[i:i+2])
                    hxs.append(h[i:i+2])
            file_name = os.path.join(dest, '%s.json' % '-'.join(hxs))
            print(file_name)
            with codecs.open(file_name, 'w', 'utf-8') as outfile:
                json.dump(self.db[key], outfile, ensure_ascii=False)
        

class JsNgramReader(object):
    """
    N-gram index reader, for test purpose.
    """
    


def test():
    ix = JsNgram(src=r'E:\bin\GRA-dev\scratch\txt')
    #ix.add_document(u'/a', u"私たちは、もっとも始めに、この文書 a を追加してみます。")
    #ix.add_document(u'/b', u'2つ目はもっともっとおもしろいよ、ね。')
    ix.add_file('a.txt')
    ix.add_file('b.txt')
    
    json_dir = r'E:\scratch\hoge'
    
    for entry in os.listdir(json_dir):
        os.remove(os.path.join(json_dir, entry))
    
    ix.to_json(json_dir)
    
    chk_db = {}
    trim_ext = re.compile(r'\.json')
    for entry in os.listdir(json_dir):
        print(entry)
        code = trim_ext.sub('', entry).split('-')
        code2 = [code[i] + code[i+1] for i in range(0, len(code), 2)]
        print(code, code2)
        keys = [chr(int(asc, 16)) for asc in code2]
        for k in keys:
            print(k)
        key = ''.join(keys)
        print(key)
        file_name = os.path.join(json_dir, entry)
        with codecs.open(file_name, 'r', 'utf-8') as infile:
            data = json.load(infile)
        print(data)
        chk_db[key] = data
    
    print(chk_db == ix.db)
    
    for path in (u'/a', u'/b'):
        bag = {}
        for key in chk_db.keys():
            vals = chk_db[key]
            for val in vals:
                if(val[0] == path):
                    bag[val[1]] = key
        print(path)
        for key in sorted(bag.keys()):
            print(bag[key], end=' ')
        print('')
    

if __name__ == '__main__':
    test()
