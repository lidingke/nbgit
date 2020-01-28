import json
import hashlib
from nb.db import  ShelveDB, get_db_dir
from nb.node import Cache        


def calc_ipynb(ipynb):
    with open(ipynb, 'rb') as f:
            js = json.loads(f.read().decode('utf-8'))
    cells = {}
    md5head = hashlib.new('md5')
    heads = []
    for c in js['cells']:
        md5 = hashlib.new('md5')
        source = c['source']
        [md5.update(s.encode('utf-8')) for s in source]
        digest = md5.hexdigest()
        cells[digest] = c
        heads.append(digest)
        md5head.update(digest.encode('utf-8'))
    return md5head.hexdigest(),heads,cells


class CurrentBranch(object):

    def __init__(self, ipynb_dir):
        db_dir = get_db_dir(ipynb_dir)
        self._db = ShelveDB(db_dir)
        self.ipynb = ipynb_dir
        self.lines_db = self._db.get_item('lines')
        self.cache = Cache(db=self._db)
        self.branch_refs = self._db.get_item('branche_refs')
        self.current_branch = self._db.get_item('current_branch')
        # self.cache = self._db.get_item('cache_node')

    def add_operate(self, ):
        head, head_cells, cells = calc_ipynb(self.ipynb)
        self.lines_db.update(cells)
        self.cache.index = head
        self.cache.lines = head_cells
        return head


    def commit_operate(self, commit):
        if self.cache.index == None:
            raise ValueError('emputy cache')
        self.cache.commit = commit
        index = self.cache.index
        self.cache.save_node()
        return index



        # self.cac = cell_heads# last node


    # def calc_ipynb(self, parameter_list):
        # pass        
