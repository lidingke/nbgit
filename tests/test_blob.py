import json
import shelve
from hashlib import sha1, md5
import hashlib
from blob import Blob


def dfsprint(d):
    for k, v in d.items():
        print(type(v))
        if isinstance(v, str):
            print(k, ':', v)
            # print(type(v))
        elif isinstance(v, dict):
            dfsprint(v)
        else:
            print(k, ':', v)

def test_load_ipynb_to_json():
    with open('../data/Untitled.ipynb','rb') as f:

        j = json.loads(f.read().decode('utf-8'))
        hs1 = []
        for c in j['cells']:
            h = hashlib.new('md5')
            source = c['source']
            [h.update(s.encode('utf-8')) for s in source]
            hs1.append(h.hexdigest())
        hs2 = []
        for c in j['cells'][::-1]:
            h = hashlib.new('md5')
            source = c['source']
            [h.update(s.encode('utf-8')) for s in source]
            hs2.append(h.hexdigest())
        assert hs1 == hs2[::-1]
        # j = {}
        j.pop('cells')
        print("#"*20)

                    # print(type(v))
        dfsprint(j['metadata'])
        print("#"*20)
        # for jj in j['metadata'].items():

            # print(jj)
ipynb = '../data/Untitled.ipynb'

def test_persistence():
    db = shelve.open('../data/spam', writeback=True)
    bb = Blob(db,ipynb)
    bb.persistence()

    with shelve.open('../data/spam') as db:
        for k,v in db.items():
            if v['db_type']=='meta' and v.get('dir','') == '../data/Untitled.ipynb':
                print(k)
                dfsprint(v['metadata'])
    bb.ipynb = '../data/Untitled_diff.ipynb'
    bb.persistence()



def test_build():
    db = shelve.open('../data/spam', writeback=True)
    bb = Blob(db,ipynb)
    key = None
    with shelve.open('../data/spam') as db:
        for k,v in db.items():
            if v['db_type']=='meta' and v.get('dir','') == '../data/Untitled.ipynb':
                key = k
    if key == None:
        raise ValueError('none meta key')

    # with shelve.open('../data/spam') as db:
    bb.ipynb_write ='../data/Untitled_build.ipynb'
    bb.rebuild(key, )