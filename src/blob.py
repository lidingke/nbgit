import difflib
import hashlib
import json
import pdb
import shelve


class Blob(object):
    def __init__(self,db,ipynb):
        # with shelve.open(dir) as db:
        self.db = db
        self.ipynb = ipynb
        self.ipynb_write = ipynb
        self.cells = ()

    def persistence(self):

        with open(self.ipynb, 'rb') as f:
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
        self.cells = tuple(hs)
        js.pop('cells')
        # print('js',js)
        md5 = hashlib.new('md5')
        [md5.update(s.encode('utf-8')) for s in hs]
        d = {'db_type': 'meta','dir':self.ipynb,'cells':hs}
        d.update(js)
        self.db[md5.hexdigest()] = d

        return md5.hexdigest()


    def rebuild(self, hex):

        meta = self.db[hex]
        build = meta['metadata']
        cells = [self.db[c]['cell'] for c in meta['cells']]
        # print(cells)
        build['cells'] = cells
        with open(self.ipynb_write,'wb') as f:
            f.write(json.dumps(build).encode('utf-8'))

