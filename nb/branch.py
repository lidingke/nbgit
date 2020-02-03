import json
import hashlib

from nb.db import ShelveDB, get_db_dir
from nb.node import Cache, resume_node, Node
from nb.config import CacheLockError, InitError, BranchError


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
    return md5head.hexdigest(), heads, cells


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
        # 1. init db node['root']
        # 2. init cache
        # 3. init master branch
        
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
        self.current.index = index
        # self.cache.set_parents(self.current.index)
        self.cache.lock_branch = False
        return index

    def log_cmd(self, ):
        root = self.cache.parents[0]
        root = Node(db=self._db, index=root)
        def get_parents(node):
            n = node.parents[0]
            print(node.index, '=>', n)
            if n == 'root':
                return
            else:
                node = Node(db=self._db, index=n)
                get_parents(node)
        get_parents(root)
                # print()
        # for n in self.nodes:
        #     index = n['index']
        #     parents = n['parents']
        #     print(index, '=>', parents)


    def checkout_cmd(self, name):
        # TODO ???implement checkout
        # checkout mv HEAD only. reset mv HEAD and REF
        if self.cache.lock_branch:
            raise CacheLockError()
        self.current.name = name

    def branch_cmd(self, name):
        head = self.cache.parents[0]
        self.current.index = head

    def reset_hard_cmd(self, index=None):
        # TODO reset cmd need reimplement
        if self.cache.lock_branch:
            raise CacheLockError()
        # if index:
        node = Node(db=self._db, index=index)
        resume_node(node, self.ipynb)
        # self.cache.parents = 
        self.current.index = index
        # self.current.
        # else:
            # parent = self.cache.parents[0]
            # resume_node(node, self.ipynb)
            # self.current.index = index


class CurrentBranch(object):

    def __init__(self, db):
        self._db = db
        self.refs = self._db.get_item('branch_refs')
        self.current_branch = self._db.get_item('current_branch')
        # self.branch_refs = self._db.get_item('branch_refs')


    @property
    def name(self):
        return self.current_branch

    @name.setter
    def name(self, value):
        if self.current_branch == value:
            raise ValueError(
                'current ref name as same as input:{}'.format(value))
        if value not in self.refs.keys():
            raise BranchError('branch-{} unexist.')
        self.current_branch = value

    @property
    def index(self):
        return self.refs[self.current_branch]

    @index.setter
    def index(self, value):
        self.refs[self.current_branch] = value
