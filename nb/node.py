from copy import deepcopy
import json
from nb.config import base_node_json, InitError, cell_line


# def get_property

class MetaNode(object):

    def __init__(self):
        self._node=base_node_json.copy()

    @property
    def index(self, ):
        return self._node['index']

    @index.setter
    def index(self, value):
        self._node['index'] = value

    @property
    def lines(self, ):
        return self._node['lines']

    @lines.setter
    def lines(self, value):
        self._node['lines'] = value


    @property
    def commite(self, ):
        return self._node['commite']

    @commite.setter
    def commite(self, value):
        self._node['commite'] = value

    @property
    def parents(self, ):
        return self._node['parents']

    # @commite.setter
    # def parents(self, value):
    #     self._node['parents'] = value



class Cache(MetaNode):

    def __init__(self,db):

        self._db = db
        self.nodes = self._db.get_item('nodes')
        if self.nodes == []:
            raise InitError('empty root')
        self._node = self.nodes[-1]
        self.lock_branch = False

    def save_node(self):
        self.nodes.append(base_node_json)
        self._node = self.nodes[-1]
        self.lock_branch = False

    def set_parents(self, index):
        if index not in self.parents:
            self._node['parents'].append(index)

class Node(MetaNode):

    def __init__(self, db, index):
        self._db = db
        self.nodes = self._db.get_item('nodes')
        self.lines_db = self._db.get_item('lines')
        if self.nodes == []:
            raise InitError('empty nodes')
            # self.nodes.append(base_node_json)
        if index not in self.nodes.keys():
            raise ValueError('error index')
        self._node = self.nodes[index]


    def get_cells(self):
        #TODO inpl get cells
        cells = []
        for li in self.lines:
            cl = deepcopy(cell_line)
            cl['source']=self.lines_db[li]
            cells.append(cl)
        return cells
    # def __next__(self, ):
    #     p = self._node.parents 

    #     for i in p:

def resume_node(node, ipynb):
    # TODO inpl resum node
    with open(ipynb, 'rb') as f:
        js = json.loads(f.read().decode('utf-8'))
    # js['cells'] = node.cells
    # cells = []
    # for li in node.lines:
    #     pass
    js['cells'] = node.get_cells()
    with open(ipynb, 'wb') as f:
        f.write(json.dumps(js).encode('utf-8'))

    
