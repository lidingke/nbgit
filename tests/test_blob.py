import json
from hashlib import sha1, md5
import hashlib

def test_load_ipynb_to_json():
    with open('../data/Untitled.ipynb','rb') as f:

        j = json.loads(f.read().decode('utf-8'))
        # print()

        # h.update(b"Nobody inspects the spammish repetition")
        # h.hexdigest()
        hs1 = []
        for c in j['cells']:
            h = hashlib.new('md5')
            source = c['source']
            # sources = "".join(source).encode('utf-8')
            [h.update(s.encode('utf-8')) for s in source]
            # (sources)
            # print(sha1(sources))
            # print(md5(sources))
            hs1.append(h.hexdigest())
            # print(h.hexdigest())
        # print(j)
        hs2 = []
        for c in j['cells'][::-1]:
            h = hashlib.new('md5')
            source = c['source']
            # sources = "".join(source).encode('utf-8')
            [h.update(s.encode('utf-8')) for s in source]
            # print(sha1(sources))
            # print(md5(sources))
            hs2.append(h.hexdigest())
        assert hs1 == hs2[::-1]