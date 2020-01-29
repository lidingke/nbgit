from nb.config import base_node_json


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
            raise ValueError('empty root')
        self._node = self.nodes[-1]
        self.lock = False

    def save_node(self):
        self.nodes.append(base_node_json)
        self._node = self.nodes[-1]
        self.lock = False
        # return self.current_node

    # @property
    # def is_changeable(self):
        # return self._node['lines'

    def set_parents(self, index):
        # import pdb; pdb.set_trace()
        if index not in self.parents:
            self._node['parents'].append(index)

class Node(MetaNode):

    def __init__(self, db, index):
        self._db = db
        self.nodes = self._db.get_item('nodes')
        if self.nodes == []:
            raise ValueError('empty nodes')
            # self.nodes.append(base_node_json)
        if index not in self.nodes.keys():
            raise ValueError('error index')
        self._node = self.nodes[index]


    # def __next__(self, ):
    #     p = self._node.parents 

    #     for i in p:


def checkout_node(self, node, ipynb):
    #TODO:checkout_node
    pass