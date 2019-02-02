import json
import pdb
import uuid as UUID

import os
from collections import UserDict


class Commit(object):
    """
    Commit-> N*Blob
    """

    def __init__(self, parent, uuid=None, children=None):
        if children:
            self.children = children
        self.children = []
        # self.children = []
        self.add_parent(parent)
        self.__cell_list = []
        if uuid:
            self.uuid = uuid
        else:
            self.uuid = str(UUID.uuid1())

    def add_cell(self):
        pass

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
        if self.parent in ('root','temp'):
            return 'uuid-self:{}-root'.format(self.uuid)
        # print(type(self),self.uuid,self.parent,self.children)
        _ =  "uuid-self:{}-parent:{}-child:{}:{}".format(
            self.uuid, self.parent.uuid, len(self.children),
            ",".join(c.uuid for c in self.children)
        )
        # print(_)
        return _

    # def __repr__(self):
    #     return self.__str__()
    # @classmethod


class Commits(UserDict):

    def build_from(self,lst):
        self.data = {l["uuid"]: Commit(uuid=l["uuid"], parent='temp')
                        for l in lst}
        temp_data = {l["uuid"]: l for l in lst}
        for c in self.data.values():
            i = c.uuid
            parent = temp_data[i]["parent"]
            if parent in  ('root',):
                c.parent = parent
            else:
                c.parent = self.data[parent]
            c.children = [self.data[ch] for ch in temp_data[i]["children"]]
        uuid = None
        for p in lst:
            if p["parent"] == "root":
                uuid = p["uuid"]
        if not uuid:
            raise ValueError("commit tree must have a root")
        self.root = self.data[uuid]
        return self.root

    # def __repr__(self):
    #     return  "-".join(r.uuid for r in self.data.values())

class Commit_Tree():

    def __init__(self, dir=None):
        if not dir:
            self.root = self._init_commit_tree()
            self.commits = {}
        else:
            with open(dir, 'rb') as f:

                self.datas = json.loads(f.read().decode('utf-8'))
                self.build_tree(self.datas['commits'])

    def build_tree(self, lst):
        self.commits = {l["uuid"]: Commit(uuid=l["uuid"], parent='temp')
                        for l in lst}
        temp_data = {l["uuid"]: l for l in lst}
        for c in self.commits.values():
            i = c.uuid
            c.parent = temp_data[i]["parent"]
            c.children = temp_data[i]["children"]
        uuid = None
        for p in lst:
            if p["parent"] == "root":
                uuid = p["uuid"]
        if not uuid:
            raise ValueError("commit tree must have a root")
        self.root = self.commits[uuid]
        return self.root
        # for c in self.commits:
        #     c.parent =

#todo: userdict commits
    # def save(self,dir=None):
    #     commits = [{''} for c in self.commits.values()]
    #     d = json.dumps(self.datas)
    #     with open(dir,'wb') as f:
    #         f.write(d.encode('utf-8'))


    def _init_commit_tree(self):
        root = Commit('root')
        return root

    def new_commit(self, parent):
        if isinstance(parent, str):
            parent = self.commits[parent]
        elif isinstance(parent, Commit):
            pass
        else:
            raise ValueError('parent type error')
        child = Commit(parent)
        # parent.chirlds.append(chirld)
        return child

    def change_commit_to(self, child, parent):
        # if child in parent.children:
        child.parent.children.remove(child)
        child.change_parent(parent)
        parent.children.append(child)
        return child

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


class Blob(object):
    def __init__(self):
        pass


class Branch(object):

    def __init__(self, head):
        self.head = head
        self.labels = set(self.head)
        self.current = head

    def new_label(self, label):
        if label in self.labels:
            self.labels.add(label)
        else:
            raise ValueError('Duplicate label.')
