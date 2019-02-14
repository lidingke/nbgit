import json
import pdb
import shelve
import uuid as UUID

import os
from collections import UserDict

from blob import Blob
from config import base_json


class Commit(object):
    """
    Commit.uuid-> hex:Blob(hexs:cells)
    """

    def __init__(self, parent, uuid, cell_list=(), children=None, merge_commit=None):
        if children:
            self.children = children
        self.children = []
        self.add_parent(parent)
        self.cell_list = cell_list
        self.uuid = uuid
        self.merge_commit = merge_commit

    # def add_cell(self):
    #     pass

    def add_parent(self, parent):
        self.parent = parent
        if parent in ('root', 'temp'):
            return parent

        self.parent.children.append(self)
        return parent

    def change_parent(self, parent):
        assert isinstance(parent, Commit)
        self.parent = parent

    def __repr__(self):
        if self.parent in ('root', 'temp'):
            return 'uuid-self:{}-root'.format(self.uuid)
        # print(type(self),self.uuid,self.parent,self.children)
        _ = "uuid-self:{}-parent:{}-child:{}:{}".format(
            self.uuid, self.parent.uuid, len(self.children),
            ",".join(c.uuid for c in self.children)
        )
        # print(_)
        return _

    # def __repr__(self):
    #     return self.__str__()


class Commits(UserDict):

    def build_from(self, lst):
        """
        1. rebuild temp commit
        2. rebuild these commit's parent and chirldren
        :param lst->[{"uuid": "abcd1234","parent": "root","children": ["abcd1235"]]:
        :return:
        """
        self.data = {l["uuid"]: Commit(uuid=l["uuid"], parent='temp') for l in lst}
        temp_data = {l["uuid"]: l for l in lst}
        for c in self.data.values():
            i = c.uuid
            parent = temp_data[i]["parent"]
            if parent in ('root',):
                c.parent = parent
            else:
                c.parent = self.data[parent]
            c.children = [self.data[ch] for ch in temp_data[i]["children"]]
        root_exited = None
        for p in lst:
            if p["parent"] == "root":
                root_exited = p["uuid"]
        if not root_exited:
            raise ValueError("commit tree must have a root")
        self.root = self.data[root_exited]
        return self.root

    def __contains__(self, item):
        return (item in self.data.keys()) or \
               (item in self.data.values())
    # def __repr__(self):
    #     return  "-".join(r.uuid for r in self.data.values())


class Commit_Tree():

    def __init__(self, ipynb, db=None, rebuild_dir=None, ):
        self.commits = Commits()
        if db:
            self.db = shelve.open(db, writeback=True)
        else:
            self.db = db
        self.ipynb = ipynb
        if not rebuild_dir:
            self.root = self._init_commit_tree()
        else:
            with open(rebuild_dir, 'rb') as f:
                datas = json.loads(f.read().decode('utf-8'))
                self.commits.build_from(datas['commits'])

    def _init_commit_tree(self):
        root = Commit('root', uuid='root')
        self.commits[root.uuid] = root
        return root

    def get_new_commit_on_ipynb(self, ipynb, db):
        bb = Blob(db, ipynb)
        uuid = bb.persistence()
        cell_list = bb.cells
        return uuid, cell_list

    def new_commit(self, parent):
        if isinstance(parent, str):
            parent = self.commits[parent]
        elif isinstance(parent, Commit):
            assert parent in self.commits.values()
        else:
            raise ValueError('parent type error')
        uuid, cells = self.get_new_commit_on_ipynb(self.ipynb, self.db)
        child = Commit(parent, uuid, cells)
        self.commits[child.uuid] = child
        return child

    def delete_commit(self):
        pass

    def change_commit_to(self, child, parent):
        # if child in parent.children:
        child.parent.children.remove(child)
        child.change_parent(parent)
        parent.children.append(child)
        return child

    def is_origin(self, origin, child):
        # todo:unit test
        if child.parent == 'root':
            return False

        p = child.parent
        while p != 'root':
            if p.uuid == origin.uuid:
                return True
            p = p.parent
        return False

    def __repr__(self):
        listtree = {}
        level_flag = 10

        def bfs(stack, level):
            if not stack:
                return
            if level > level_flag:
                return
            children = []
            listtree[level] = stack

            for n in stack:
                # pdb.set_trace()
                children.extend(n.children)

                bfs(children, level + 1)

        bfs(self.root.children, 0)
        _ = ["{}:{}".format(k, v) for k, v in listtree.items()]
        return "\n".join(_)


class Branch(object):

    def __init__(self, commit_tree, data_dir=None):
        if data_dir:
            if not os.path.exists(data_dir):
                with open(data_dir, 'wb') as f:
                    f.write(json.dumps(base_json).encode('utf-8'))

            with open(data_dir,'rb') as f:
                data = json.loads(f.read().decode('utf-8'))
        else:
            data = self.new_data()
        self.commit_tree = commit_tree

        self.current_branch = data['current']['branch']
        node_hex = data['current']['node']
        self.current_node = self.commit_tree.commits[node_hex]
        self.branch_list = data['branches']


    def new_data(self):
        raise NotImplementedError

    def new_commit(self):
        parent = self.current_node
        node = self.commit_tree.new_commit(parent)
        self.current_node =node

    def change_current_branch(self,flag):
        assert flag in self.branch_list.keys()
        self.current_branch = flag
        self.current_node = self.branch_list[flag][-1]

    def add_new_branch(self,flag):
        raise NotImplementedError

    def reset(self,hex):
        pass




