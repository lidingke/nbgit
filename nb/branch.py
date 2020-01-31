import json
import hashlib
from nb.db import  ShelveDB, get_db_dir
from nb.node import Cache, resume_node, Node
from nb.config import CacheLockError, InitError


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


class Branch(object):

    def __init__(self, ipynb_dir):
        db_dir = get_db_dir(ipynb_dir)
        self._db = ShelveDB(db_dir)
        self.ipynb = ipynb_dir
        self.lines_db = self._db.get_item('lines')
        self.cache = Cache(db=self._db)
        self.nodes = self._db.get_item('nodes')
        # self.branch_refs = self._db.get_item('branche_refs')
        self.current = CurrentBranch(db=self._db)
        # self.cache = self._db.get_item('cache_node')

    def init_cmd(self):
        # dir_= get_db_dir(current_ipynb)
        # sdb = ShelveDB(dir_=dir_)
        self._db.create_bare_db()


    def add_cmd(self, ):
        head, head_cells, cells = calc_ipynb(self.ipynb)
        self.lines_db.update(cells)
        self.cache.index = head
        self.cache.lines = head_cells
        self.cache.lock_branch = True
        return head


    def commit_cmd(self, commit):
        # TODO : auto merge commit
        if self.cache.index == None:
            raise InitError('emputy cache')
        index = self.cache.index
        self.cache.commit = commit
        self.cache.save_node()
        self.current.current_index = index
        self.cache.set_parents(self.current.current_index)
        self.cache.lock_branch = False
        return index

    def log_cmd(self, ):
        # import pdb; pdb.set_trace()
        for n in self.nodes:
            index = n['index']
            parents = n['parents']
            print(index,'=>',parents)
        # for i in self. 
        # self.cac = cell_heads# last node
    def checkout_cmd(self, name):
        # TODO implement checkout
        if self.cache.lock_branch:
            raise CacheLockError()
        self.current.current = name 

    def branch_cmd(self,name):
        pass


    def reset_cmd(self, index=None):
        # TODO implement reset
        # reset index=None 
        if self.cache.lock_branch:
            raise CacheLockError()
        if index:
        # self._resume_ipynb(index)
            node = Node(db=self._db, index=index)
            resume_node(node,self.ipynb)
            self.current.current_index = index
        else:
            parent = self.cache.parents[0]
            resume_node(node,self.ipynb)
            self.current.current_index = index
    # def _resume_ipynb(self, index):


    # def calc_ipynb(self, parameter_list):
        # pass        

class CurrentBranch(object):

    def __init__(self,db):
        self._db = db
        self.refs = self._db.get_item('branch_refs')
        self.current_branch = self._db.get_item('current_branch')


    def change_branch_safe(self,name):
        if self.current_branch == name:
            raise ValueError('current ref name as same as input:{}'.format(name))
        if not name in self.refs.keys():
            raise ValueError('error input ref name.')
        self._db["current_branch"] = name

    @property
    def current(self):
        return self.current_branch

    @current.setter
    def current(self,value):
        self.current_branch =value

    @property
    def current_index(self):
        return self.refs[self.current_branch]

    @current_index.setter
    def current_index(self,value):
        self.refs[self.current_branch] = value