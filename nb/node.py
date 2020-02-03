from copy import deepcopy
import json
from nb.config import base_node_json, InitError, cell_line, NodeError, get_base_node_json


def get_node_property(name, type_):

    def get_(self,):
        return self._node[name]

    def set_(self, value):
        assert isinstance(value, type_)
        self._node[name] = value

    return get_, set_


class MetaNode(object):

    def __init__(self):
        self._node = base_node_json.copy()

    index = property(*get_node_property('index', str))

    lines = property(*get_node_property('lines', list))

    commite = property(*get_node_property('commite', str))

    parents = property(*get_node_property('parents', list))

    tags = property(*get_node_property('tags', list))


class Cache(MetaNode):

    def __init__(self, db):

        self._db = db
        self.nodes = self._db.get_item('nodes')
        if self.nodes == []:
            raise InitError('empty root')
        self._node = self._db.get_item('cache')
        # self.head = self.parents[0]
        self.lock_branch = False

    def save_node(self):
        # base = deepcopy(base_node_json)
        # index = self.index
        # self._node['parents'].append(self.head)
        # self.nodes.append(base)
        # self._node = self.nodes[-1]
        # self.head = index
        # self.index = ''
        # base = get_base_node_json()
        # base
        index = self.index
        self.nodes.append(self._node)
        self.reset()
        self.parents = [index,]
        # self.set_parents(index)
        self.lock_branch = False

    def reset(self, ):
        parents = self._node.parents
        self._node=get_base_node_json()
        self._node.parents = parents
        # self.head = self.

    # @property
    # def head(self):
        # return self.head

    # def set_parents(self, index):
    #     if index not in self.parents:
    #         self._node['parents'].append(index)


class Node(MetaNode):

    def __init__(self, db, index):
        self._db = db
        self.nodes = self._db.get_item('nodes')
        self.lines_db = self._db.get_item('lines')
        if self.nodes == []:
            raise InitError('empty nodes')
            # self.nodes.append(base_node_json)
        self._node = None
        # if index not in self.nodes.keys():
        # raise ValueError('error index')
        if index == 'root':
            self._node = get_base_node_json()
            self._node.index = 'root'
            return
        for n in self.nodes:
            if n['index'] == index:
                self._node = n
                return
        if not self._node:
            raise NodeError('can\'t find index in nodes')

    def get_cells(self):
        # TODO inpl get cells
        cells = [self.lines_db[li] for li in self.lines]
        return cells

    def is_root(self,):
        return self._node.index == 'root' or self._node.parents == []


class NodeDB(object):

    def __init__(self, db,):
        self._db = db
        self.nodes = self._db.get_item('nodes')

    def get_node(self, index):
        n = Node(self._db, index)
        return n


def resume_node(node, ipynb):
    # TODO impl resume node
    with open(ipynb, 'rb') as f:
        js = json.loads(f.read().decode('utf-8'))
    # js['cells'] = node.cells
    # cells = []
    # for li in node.lines:
    #     pass
    js['cells'] = node.get_cells()
    with open(ipynb, 'wb') as f:
        f.write(json.dumps(js).encode('utf-8'))
