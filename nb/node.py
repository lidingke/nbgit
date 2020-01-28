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
    def commites(self, ):
        return self._node['commites']

    @commites.setter
    def commites(self, value):
        self._node['commites'] = value



class Cache(MetaNode):

    def __init__(self,db):

        self._db = db
        self.nodes = self._db.get_item('nodes')
        if self.nodes == []:
            self.nodes.append(base_node_json)
        self._node = self.nodes[-1]

    def save_node(self):
        self.nodes.append(base_node_json)
        self._node = self.nodes[-1]
        # return self.current_node

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

def checkout_node(self, node, ipynb):
    #TODO:checkout_node
    pass