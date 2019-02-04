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

def test_persistence():
    bb = Blob('../data/spam')
    bb.persistence('../data/Untitled.ipynb')

    with shelve.open('../data/spam') as db:
        for k,v in db.items():
            if v['db_type']=='meta':
                print(k)
                dfsprint(v['metadata'])


def test_build():
    bb = Blob('../data/spam')
    key = None
    with shelve.open('../data/spam') as db:
        for k,v in db.items():
            if v['db_type']=='meta':
                key = k
    if key == None:
        raise ValueError('none meta key')

    # with shelve.open('../data/spam') as db:
    bb.build(key,'../data/Untitled_build.ipynb')