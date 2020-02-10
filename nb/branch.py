import json
import hashlib

from nb.db import ShelveDB, get_db_dir
from nb.node import Cache, resume_node, Node, NodeDB, Branch
from nb.config import CacheLockError, InitError, BranchError
from nb.diff import Merger


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


def init_cmd(ipynb):
    # 1. init db node['root']
    # 2. init cache
    # 3. init master branch

    db_dir = get_db_dir(ipynb)
    _db = ShelveDB(db_dir)
    _db.create_bare_db()

    # _db.cache


def atom_op(fun):
    def inner(*args, **kwargs):
        ret = fun(*args, **kwargs)
        self = args[0]
        self._db.close()
        return ret
    return inner

class Repo(object):

    def __init__(self, ipynb_dir):
        db_dir = get_db_dir(ipynb_dir)
        self._db = ShelveDB(db_dir)
        self.ipynb = ipynb_dir
        # self.lines_db = self._db.get_item('lines')
        # print('befor cache init',self._db.get_item('cache'))
        self.cache = Cache(db=self._db)
        # print('init cache:',self.cache.index)
        # self.nodes = self._db.get_item('nodes')
        self.nodedb = NodeDB(db=self._db)
        # self.branch_refs = self._db.get_item('branche_refs')
        self.current = Branch(db=self._db)
        self.merger = Merger(db=self._db)
        # self.cache = self._db.get_item('cache_node')

    
    # def init_cmd(self):

        # self._db.create_bare_db()

    def add_cmd(self, ):
        head, head_cells, cells = calc_ipynb(self.ipynb)
        self.nodedb.save_lines(cells)
        self.cache.index = head
        self.cache.lines = head_cells
        self.cache.lock_branch = True
        return head

    # @atom_op
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
        if root == 'root':
            # print('root')
            return
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

    def checkout_cmd(self, name):
        # TODO ???implement checkout
        # checkout mv HEAD only. reset mv HEAD and REF
        if self.cache.lock_branch:
            raise CacheLockError()
        # self.cache.
        self.current.name = name

    def branch_cmd(self, name):
        # import pdb; pdb.set_trace()
        head = self.cache.parents[0]
        self.current.index = head
        self.current.add(name)

    def reset_hard_cmd(self, index=None):
        # TODO reset cmd need reimplement
        if self.cache.lock_branch:
            raise CacheLockError()
        # if index:
        # node = Node(db=self._db, index=index)
        node = self.nodedb.get_node(index)
        resume_node(node, self.ipynb)
        # self.cache.parents =
        self.current.index = index
        # self.current.
        # else:
        # parent = self.cache.parents[0]
        # resume_node(node, self.ipynb)
        # self.current.index = index

    def diff_cmd(self, index0, index1):
        self.merger.diff(index0, index1)

    def merge_cmd(self, current, other):
        """
        1. find common ancestor for both branch.
        2. diff lines on current node.
        3. diff lines on other node.
        4. three way merge for two diffs.
        """
        # lst = self.merger.trace_root([self.current.index])
        # ancestor = self.merger.find_ancestor(current,other)
        # import pdb; pdb.set_trace()
        self.merger.auto_merge(other)



