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

        return md5.hexdigest()


    def rebuild(self, hex, dir):
        meta = self.db[hex]
        build = meta['metadata']
        cells = [self.db[c]['cell'] for c in meta['cells']]
        # print(cells)
        build['cells'] = cells
        with open(dir,'wb') as f:
            f.write(json.dumps(build).encode('utf-8'))

