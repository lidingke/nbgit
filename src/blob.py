import difflib
import hashlib
import json
import pdb
import shelve


class Blob(object):
    def __init__(self,dir):
        # with shelve.open(dir) as db:
        self.db = shelve.open(dir,writeback=True)

    def persistence(self,ipynb):
        with open(ipynb, 'rb') as f:
            js = json.loads(f.read().decode('utf-8'))
        hs = []
        for c in js['cells']:
            md5 = hashlib.new('md5')
            source = c['source']
            [md5.update(s.encode('utf-8')) for s in source]
            # d =
            # pdb.set_trace()
            # d.update(source)

            self.db[md5.hexdigest()] = {'db_type':'cell','cell':c}
            hs.append(md5.hexdigest())
        js.pop('cells')
        # print('js',js)
        md5 = hashlib.new('md5')
        [md5.update(s.encode('utf-8')) for s in hs]
        d = {'db_type': 'meta','dir':ipynb,'cells':hs}
        d.update(js)
        self.db[md5.hexdigest()] = d


    def rebuild(self, hex, dir):
        meta = self.db[hex]
        build = meta['metadata']
        cells = [self.db[c]['cell'] for c in meta['cells']]
        # print(cells)
        build['cells'] = cells
        with open(dir,'wb') as f:
            f.write(json.dumps(build).encode('utf-8'))


def insert(a,a0,a1,seq):
    for s in seq:
        a.insert(a1,s)
    return a

def delete(a,a0,a1,seq):
    for i in range(a0,a1):
        a.pop(i)
    return a

def equal(a,a0,a1,seq):
    return a

def replace(a, a0, a1, seq):
    for i, v in zip(range(a0, a1), seq):
        a[i] = v
    return a


op_fun = {
    'insert':insert,
    'delete':delete,
    'equal':equal,
    'replace':replace
}

op_fun_back = {
    'insert':delete,
    'delete':insert,
    'equal':equal,
    'replace':replace
}

def get_reversed_opecodes(seq0,seq1):
    matcher = difflib.SequenceMatcher(None,seq0,seq1)
    _ = [(tag, i0,i1,seq1[j0:j0]) for tag, i0, i1, j0, j1 in reversed(matcher.get_opcodes())]
    return _

def constructer(seq,opcodes):
    for tag, i0,i1,seq1 in opcodes:
        assert tag in op_fun.keys()
        seq = op_fun[tag](seq,i0,i1,seq1)

    return seq


def back_constructer(seq, opcodes):
    for tag, i0, i1, seq1 in opcodes:
        assert tag in op_fun_back.keys()
        seq = op_fun_back[tag](seq, i0, i1, seq1)

    return seq